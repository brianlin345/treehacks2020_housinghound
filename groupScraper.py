import requests
from requests_html import HTMLSession

url = 'https://m.facebook.com/groups/ucberkeleyoffcampushousing'
url2 = 'https://m.facebook.com/groups/1835635240040670/'



def filterPost(text):
    if len(text) <= 0:
        return False
    else:
        return True

def findNextPage(r):
    urlID = 'multi_permalinks'
    for url in r.html.absolute_links:
        if urlID in url:
            return url

def findGroupName(r):
    group_class = '._de1'
    group_name = r.html.find(group_class, first = True)
    return group_name.text


def scrapePage(r, posts):
    session = HTMLSession()
    group_name = findGroupName(r)
    post_class = '.story_body_container'
    for post in r.html.find(post_class):
        curr_poster = post.find('strong')[0].text
        curr_post = ''
        for para in post.find('p'):
            curr_post += para.text
        if filterPost(curr_post):
            posts[curr_poster]= curr_post


def scraperMain(start_url, pages = 2):
    session = HTMLSession()
    posts = {}

    for search in range(pages):
        req = session.get(start_url)
        print('Scraping page ' + start_url)
        scrapePage(req, posts)
        start_url = findNextPage(req)


    return posts



print(scraperMain(url2))


def parsePost(post):
    buyer_words = ['looking for', 'budget', 'searching']
    seller_words = ['lease', '$', 'resident']
    post_words = post.split()


class Housing:
    def __init__(self, bedrooms, bathrooms, price):
        self._bedrooms = bedrooms
        self._bathrooms = bathrooms
        self._price = price
