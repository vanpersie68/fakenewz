import json
from pytube import YouTube
import ssl
import requests
from lxml import etree

ssl._create_default_https_context = ssl._create_unverified_context


def extra_video_data(video_url):
    if 'tiktok' in video_url:
        print(video_url)
        page = requests.get(url='https://www.tiktok.com/oembed?url=' + video_url)
        data = json.loads(page.text)
        video_data = {"embed_url": video_url, "video_title": data['title'], "video_id": data['provider_url'],
                      'articleImageLink': data['thumbnail_url'], 'articleUser': data['author_name']}
        return video_data
        # html = etree.HTML(page)
    else:
        embed_url, video_title, video_id = get_youtube_video_info(video_url)
        video_data = {"embed_url": embed_url, "video_title": video_title, "video_id": video_id}
        return video_data


def get_youtube_video_info(video_url):
    # get ID
    video_id = video_url.split("v=")[1]

    # Request to YouTube API
    api_key = "AIzaSyAcSrMwF6KK3AGFrirOVwg7OH5aZsPvriE"
    api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={api_key}"
    response = requests.get(api_url)
    data = json.loads(response.text)

    # Get infos
    if 'items' in data and len(data['items']) > 0:
        video_info = data['items'][0]
        title = video_info['snippet']['title']
        embed_url = f"https://www.youtube.com/embed/{video_id}"
        return embed_url, title, video_id

    return None, None, None
