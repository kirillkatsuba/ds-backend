import requests
from requests.exceptions import Timeout, RequestException
import logging


class ImageReaderClient:
    def __init__(self, host: str, timeout: float = 2.5):
        self.host = host
        self.timeout = timeout

    def read_plate_one_number(self, im: int):
        try:
            res = requests.get(
                f'{self.host}/{im}',
                headers  = {'Content-Type': 'application/json'},
                timeout = self.timeout
            )
            res.raise_for_status()
        
        except requests.exceptions.HTTPError:
            logging.error('error while downloading image')

            return {
                'error': 'error while downloading image',
                'status_code': 404
                }

        except requests.exceptions.Timeout:
            logging.error(f'timeout error')

            return {
                'error': 'timeout error', 
                'status_code': 408
                }

        return {
            'image_data': res.content, 
            'status_code': 200
            }

    def read_plate_several_numbers(self, ims: str):
        result = {}
        ims_ids = list(map(int, im.split(',')))
        for im in ims_ids:
            result[im] = self.read_plate_one_number(im)

        return result


if __name__ == '__main__':
    client = ImageReaderClient(host='http://89.169.157.72:8080/images')
    res = client.read_plate_one_number(49965)
    print(res)