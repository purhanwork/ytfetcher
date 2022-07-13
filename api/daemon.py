import asyncio
import logging
import os
from aiohttp import ClientSession
from asgiref.sync import sync_to_async
from datetime import datetime, timedelta, timezone
from django.db import Error
from django.utils.dateparse import parse_datetime
from .models import VideoMeta, ApiSettings

GOOGLE_API_KEYS = os.environ.get('GOOGLE_API_KEYS', '').split()
INTERVAL = 10

def fetchVideoData():
    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        baseTime = ApiSettings.objects.last().baseTime
    except:
        baseTime = datetime(year=2022, month=7, day=1, tzinfo=timezone.utc)
        ApiSettings.objects.create(baseTime=baseTime)

    loop.run_until_complete(fetchStoreVideosAsync(baseTime))


async def fetchStoreVideosAsync(baseTime):
    CUR_KEY = 0
    TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    session = ClientSession()

    try:
        latestVideoObject = await sync_to_async(VideoMeta.objects.latest)()
        latestPublishedAt = latestVideoObject.publishedAt
        oldestVideoObject = await sync_to_async(VideoMeta.objects.filter(publishedAt__gte=baseTime).earliest)()
        earliestPublishedAt = oldestVideoObject.publishedAt
    except:
        latestPublishedAt = datetime.now(timezone.utc)
        earliestPublishedAt = latestPublishedAt

    publishedAfter = baseTime.strftime(TIME_FORMAT)
    lastPagePublishedAt = earliestPublishedAt
    lastPagePublishedAt += timedelta(seconds=10) if earliestPublishedAt == baseTime else timedelta()
    publishedBefore = lastPagePublishedAt.strftime(TIME_FORMAT)
    nextPageToken = ""

    while(1):
        await asyncio.sleep(INTERVAL)

        url = 'https://youtube.googleapis.com/youtube/v3/search?part=snippet&order=date&q=cricket&type=video&eventType=completed' + \
            f'&pageToken={nextPageToken}&maxResults=100&publishedBefore={publishedBefore}&publishedAfter={publishedAfter}&key={GOOGLE_API_KEYS[CUR_KEY]}'

        cur_oldest = datetime.now(timezone.utc)
        cur_latest = datetime.min.replace(tzinfo=timezone.utc)

        try:
            async with session.get(url) as response:
                res = await response.json()
        except:
            logging.warning("Could not get a response from server")
            continue

        if 'error' in res:
            if res['error']['errors'][0]['reason'] == 'quotaExceeded':
                CUR_KEY += 1

                if CUR_KEY  == len(GOOGLE_API_KEYS):
                    logging.warning("Ran out of keys!")
                    CUR_KEY = 0
                    await session.close()
                    asyncio.sleep(3600)
                    session = ClientSession()
            continue

        objects = []
        for video in res.get('items', []):
            videoPublishedAt = parse_datetime(video['snippet']['publishedAt'])

            if videoPublishedAt <= lastPagePublishedAt and videoPublishedAt >= parse_datetime(publishedAfter):
                if videoPublishedAt < cur_oldest:
                    cur_oldest = videoPublishedAt
                if videoPublishedAt > cur_latest:
                    cur_latest = videoPublishedAt

                objects.append(
                    VideoMeta(
                        title=video['snippet']['title'],
                        description=video['snippet']['description'],
                        publishedAt=videoPublishedAt,
                        videoId=video['id']['videoId'],
                        thumbnailURL=video['snippet']['thumbnails']['high']['url']
                    )
                )

        await sync_to_async(VideoMeta.objects.bulk_create)(objects, ignore_conflicts=True)

        if res['items']:
            if not nextPageToken and latestPublishedAt < cur_latest:
                latestPublishedAt = cur_latest

        if 'nextPageToken' in res:
            nextPageToken = res['nextPageToken']
        else:
            nextPageToken = ""
            publishedAfter = (latestPublishedAt + timedelta(seconds=1)).strftime(TIME_FORMAT)
            obj = await sync_to_async(ApiSettings.objects.last)()
            obj.baseTime = publishedAfter
            await sync_to_async(obj.save)()
            publishedBefore = datetime.utcnow().strftime(TIME_FORMAT)
            if publishedAfter == publishedBefore:
                publishedBefore = (
                    datetime.utcnow() + timedelta(seconds=10)).strftime(TIME_FORMAT)
