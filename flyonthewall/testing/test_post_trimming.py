import json
import logging
from pprint import pprint

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

test_file = '../json/testexchange_testmarket/05192018_134940/thread_archive.json'


if __name__ == '__main__':
    with open(test_file, 'r') as file:
        data = json.load(file)

    for thread in data:
        for post in data[thread]:
            post_truncated = post
            while (True):
                post_num_index = post_truncated.find('no.')

                if post_num_index == -1:
                    break

                else:
                    post_truncated = post_truncated[(post_num_index + 3):]

            for x in range(0, len(post_truncated)):
                if post_truncated[x].isalpha():
                    first_letter_index = x

                    break
            
            post_truncated = post_truncated[first_letter_index:]
            logger.debug('post_truncated: ' + post_truncated)
