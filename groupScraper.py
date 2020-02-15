import facebook
import urllib3
import requests

from requests_html import HTMLSession
from bs4 import BeautifulSoup

url = 'https://m.facebook.com/groups/ucberkeleyoffcampushousing'
url2 = 'https://m.facebook.com/groups/1835635240040670/'


def checkReaction(text):
    reactions = ['Likes', 'Like', 'Comments', 'Comment', 'Share', 'Shares']
    return any([reaction in text for reaction in reactions])

def checkExpand(text):
    expand_text = "More"
    return expand_text in text

def checkEnds(text):
    endText = '·'
    if text == endText:
        return True
    return False

def filterSpan(text):
    if len(text) <= 0:
        return False
    if checkReaction(text):
        return False
    if checkExpand(text):
        return False
    return True

def findNextPage(r):
    urlID = 'multi_permalinks'
    for url in r.html.absolute_links:
        if urlID in url:
            return url

profiles = {}

def scrapePage(r):
    separator = '\\'
    curr_post = ''
    posts = []
    last_token = ''
    for post in r.html.find('span'):
        curr_text = post.text
        if(filterSpan(curr_text)):
            if checkEnds(curr_text):
                curr_post = curr_post.replace(last_token, '')
                posts.append(curr_post)

                curr_name = print(last_token.split(separator))
                profiles[curr_name] = ''

                curr_post = ''
            curr_post += curr_text
            last_token = curr_text
    return posts

def scraperMain(start_url, pages = 1):
    session = HTMLSession()
    posts = []
    for search in range(pages):
        print('Scraping page ' + start_url)
        req = session.get(start_url)
        posts.extend(scrapePage(req))
        start_url = findNextPage(req)
    return posts

print(scraperMain(url2))
print(profiles)
