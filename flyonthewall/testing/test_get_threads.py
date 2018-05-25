from bs4 import BeautifulSoup
from pprint import pprint
import requests
import lxml

r = requests.get('http://boards.4chan.org/biz/')

soup = BeautifulSoup(r.text, 'lxml')
threads = soup.find_all('a', attrs={'class': 'replylink'})
#print(threads)

thread_list = []
for thread in threads:
    thread_num = thread['href'].split('/')[1]
    print(thread_num)
    thread_list.append(thread_num)

pprint(thread_list)
print(len(thread_list))
