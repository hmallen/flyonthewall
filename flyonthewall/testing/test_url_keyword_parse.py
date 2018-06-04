import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    cmc_json_file = 'test_cmc_data.json'

    with open(cmc_json_file, 'r', encoding='utf-8') as file:
        cmc_data = json.load(file)

    for key in cmc_data:
        if isinstance(cmc_data[key], list):
            print(key, type(cmc_data[key]), len(cmc_data[key]), cmc_data[key])

        else:
            print(key, type(cmc_data[key]), cmc_data[key])
