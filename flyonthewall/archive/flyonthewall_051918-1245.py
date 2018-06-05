import argparse
from bs4 import BeautifulSoup
import json
import logging
#import lxml
import os
from pprint import pprint
import requests
import sys
import time
import wget

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--board', type=str, default='biz', help='Choose 4chan board to monitor [Default = biz]')
parser.add_argument('-l', '--loop', type=int, default=60, help='Delay between checks (seconds) [Default = 60]')
parser.add_argument('-m', '--limit', default=99, type=int, help='Limit to number of threads instead of analyzing full first page.')
parser.add_argument('-o', '--output', type=str, default='downloads', help='Download to alternate directory [Default = downloads/]')
parser.add_argument('-k', '--keyword', type=str, default='keywords.txt', help='Use alternate keyword file [Default = keywords.txt]')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='Include debug output')
args = parser.parse_args()

debug_mode = args.debug
board = args.board.strip('/')
loop_time = args.loop
thread_limit = args.limit
download_dir = args.output
keyword_file = args.keyword

if debug_mode:
    logger.setLevel(logging.DEBUG)

url_base = 'https://boards.4chan.org/'
url_board = board + '/'
url_thread_base = 'thread/'
url_prefix = url_base + url_board + url_thread_base
logger.debug('url_prefix: ' + url_prefix)

excluded_threads = ['4884770', '904256']

thread_archive_file = 'thread_archive.json'


def get_threads(url='https://boards.4chan.org/biz/', pages=1):
    try:
        logger.debug('Retrieving thread list.')

        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')# 'lxml')
        threads = soup.find_all('a', attrs={'class': 'replylink'})
        #print(threads)

        thread_list = []
        for thread in threads:
            thread_num = thread['href'].split('/')[1]
            thread_list.append(thread_num)

        return thread_list

    except Exception:
        logger.exception('Exception while getting threads.')
        raise


def get_posts(thread_num):
    try:
        logger.debug('Retrieving posts.')

        url = url_prefix + thread_num
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')#'lxml')
        #posts = soup.find_all('blockquote', attrs={'class': 'postMessage'})
        data = soup.find_all('div', attrs={'class': ['post op', 'post reply']})

        post_list = []
        for post in data:
            post_data = {}
            post_data['post'] = post.text
            attachments = post.find_all('a', attrs={'class': 'fileThumb'})
            # ONLY GETS LAST FILE (MULTIPLE POSSIBLE?)
            for file in attachments:
                file_url = 'https:' + file['href']
                logger.debug('file_url: ' + file_url)
                post_data['file'] = file_url
            post_list.append(post_data)
            logger.debug('post_data: ' + str(post_data))

        #pprint(post_list)
        logger.debug('post_list: ' + str(post_list))

        return post_list


    except Exception:
        logger.exception('Exception while getting posts.')
        raise


def filter_threads(threads, keywords):
    try:
        logger.debug('Filtering threads.')

        logger.info('threads: ' + str(threads))

        threads_filtered = {}

        thread_count = len(threads)
        thread_loops = 0
        for key in threads:
            thread_loops += 1
            logger.debug('key: ' + key)
            logger.info('Thread #' + str(thread_loops) + ' of ' + str(thread_count))
            posts = threads[key]
            logger.debug('posts: ' + str(posts))

            found_list = []
            post_count = len(posts)
            post_loops = 0
            for post in posts:
                post_loops += 1
                logger.info('Post #' + str(post_loops) + ' of ' + str(post_count))
                logger.debug('post: ' + str(post))

                word_count = len(keywords)
                word_loops = 0
                for word in keywords:
                    word_loops += 1
                    logger.debug('Word #' + str(word_loops) + ' of ' + str(word_count))
                    #logger.debug('word: ' + word)
                    #logger.debug('post.lower(): ' + post.lower())

                    logger.debug('post: ' + str(post))
                    if word in post['post'].lower():
                        #logger.debug('FOUND: ' + word)
                        passed_excluded = True
                        for excluded in excluded_list:
                            if excluded in post['post'].lower():
                                passed_excluded = False
                                logger.debug('Found excluded word: ' + excluded)
                                logger.debug('Excluding post: ' + str(post))
                        if passed_excluded == True:
                            entry = word + '|' + post['post'].lower()
                            if 'file' in post:
                                entry = entry + '|' + post['file']
                                logger.info('Downloading attachment.')
                                file_name = wget.detect_filename(url=post['file'])
                                logger.debug('file_name: ' + file_name)
                                if not os.path.isfile(download_dir + file_name):
                                    dl_file = wget.download(post['file'], out=download_dir.rstrip('/'))
                                    logger.info('Successful download: ' + dl_file)
                            found_list.append(entry)

            if len(found_list) > 0:
                threads_filtered[key] = found_list

        return threads_filtered


    except Exception:
        logger.exception('Exception while filtering threads.')
        raise


if __name__ == '__main__':
    try:
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)

        logger.debug('Loading keyword file.')
        with open(keyword_file, 'r') as kw:
            keyword_list_read = kw.read().split()
        keyword_list = []
        excluded_list = []
        for keyword in keyword_list_read:
            if '|' in keyword:
                keyword_split = keyword.split('|')
                keyword_list.append(keyword_split[0])
                if ',' in keyword_split[1]:
                    excluded_split = keyword_split[1].split(',')
                    for word in excluded_split:
                        if word != '' and word != '\n' and word != '\r':
                            excluded_list.append(word)
                else:
                    excluded_list.append(keyword_split[1])
            else:
                if keyword != '' and keyword != '\n' and keyword != '\r':
                    keyword_list.append(keyword)

        logger.debug('keyword_list: ' + str(keyword_list))
        logger.debug('excluded_list: ' + str(excluded_list))

        logger.info('----- KEYWORDS -----')
        for word in keyword_list:
            logger.info(word.upper())
        logger.info('-- EXCLUDED WORDS --')
        for word in excluded_list:
            logger.info(word.upper())
        time.sleep(3)

        # 1 - Get all threads on main page
        # 2 - Save thread numbers to list
        # 3 - For each:
        #       a) get_posts()
        #       b) Search posts for keywords
        #           i. If found, save text (and media) to directory

        thread_archive = {}

        loop_count = 0
        while (True):
            loop_count += 1
            logger.debug('loop_count: ' + str(loop_count))

            logger.info('Retrieving threads.')

            thread_list = get_threads(url=(url_base + url_board))
            for thread in excluded_threads:
                if thread in thread_list:
                    logger.debug('Removing excluded thread: ' + thread)
                    thread_list.remove(thread)

            logger.info('Gathering posts from threads.')

            thread_count = len(thread_list)
            thread_loops = 0
            for thread in thread_list:
                thread_loops += 1
                logger.info('Thread #' + str(thread_loops) + ' of ' + str(thread_count))

                if thread not in thread_archive:
                    thread_archive[thread] = []

                post_list = get_posts(thread)
                logger.debug('post_list: ' + str(post_list))
                #thread_archive[thread] = post_list
                for post in post_list:
                    if post not in thread_archive[thread]:
                        logger.debug('Appending post: ' + str(post))
                        thread_archive[thread].append(post)

                    else:
                        logger.debug('Skipping post. Already in archive.')

                if thread_loops == thread_limit:
                    logger.debug('BREAKING EARLY')
                    #time.sleep(3)
                    break

            #print()
            #print('THREAD ARCHIVE:')
            #print('Length: ', len(thread_archive))
            #print()
            #pprint(thread_archive)

            logger.info('Filtering threads for relevant content.')
            relevant_threads = filter_threads(thread_archive, keyword_list)

            if os.path.isfile(thread_archive_file):
                with open(thread_archive_file, 'r') as file:
                    thread_data = json.load(file)
            else:
                thread_data = {}

            for thread in relevant_threads:
                logger.info('Relevant thread: ' + str(thread))
                if thread not in thread_data:
                    thread_data[thread] = []
                for post in relevant_threads[thread]:
                    logger.info('Relevant post: ' + post)
                    if post not in thread_data[thread]:
                        thread_data[thread].append(post)

            logger.info('Writing relevant posts to json archive.')
            with open(thread_archive_file, 'w') as file:
                json.dump(thread_data, file, sort_keys=True, indent=4, ensure_ascii=False)

            logger.info('Sleeping ' + str(loop_time) + ' seconds.')
            time.sleep(loop_time)

    except Exception as e:
        logger.exception('Exception raised.')
        logger.exception(e)

    except KeyboardInterrupt:
        logger.info('Exit signal received.')
        sys.exit()
