from bs4 import BeautifulSoup
from pprint import pprint
import requests
import lxml

r = requests.get('http://boards.4chan.org/biz/thread/7608194/how-does-margin-trading-work')

soup = BeautifulSoup(r.text, 'lxml')
posts = soup.find_all('blockquote', attrs={'class': 'postMessage'})

post_list = []
for post in posts:
    post_list.append(post.text)

pprint(post_list)
