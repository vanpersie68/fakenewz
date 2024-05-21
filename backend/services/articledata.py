from bs4 import BeautifulSoup
import requests
import re


def extract_article_metadata(news_url):

    # dictionary to hold extracted data from article (url, headline, and article image)
    metadata = {"url":news_url, "urlShort": None, "title":None, "image":None, "description":None}

    # User agent to allow access to websites
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

    # Check validity of URL:
    try:
        response = requests.get(news_url, headers=headers)
    except requests.ConnectionError as connectionException:
        return metadata
    except requests.exceptions.MissingSchema as invalidURLException:
        return metadata

    # Add valid url to return data
    metadata["url"] = news_url

    # Clip to short URL

    # Regex patterns
    first_part_pattern = re.compile(r'http[s]?://')
    second_part_pattern = re.compile(r'/')

    # Start clipping away unnecessary parts of url with regex matches
    clipped_url = news_url

    match = re.search(first_part_pattern, clipped_url)

    idx = match.span()[1]
    clipped_url = clipped_url[idx:]
    
    match = re.search(second_part_pattern, clipped_url)
    idx = match.span()[0]

    clipped_url = clipped_url[:idx]
    metadata["urlShort"] = clipped_url

    # scrape html doc
    source = requests.get(news_url, headers=headers).text
    soup = BeautifulSoup(source, 'lxml')

    # Search meta properties as specified by facebook standards
    title = soup.find("meta", property="og:title")
    img = soup.find("meta", property="og:image")
    desc = soup.find("meta", property="og:description")

    # Fill dictionary with extracted data
    if title:
        metadata["title"] = title["content"]
    if img:
        metadata["image"] = img["content"]
    if desc:
        metadata["description"] = desc["content"]

    return metadata


