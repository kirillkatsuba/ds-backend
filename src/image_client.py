import requests
from requests.exceptions import Timeout, RequestException
import logging


class ImageReaderClient:
    def __init__(self, host: str, timeout: float = 2.5):
        self.host = host
        self.timeout = timeout

    def read_plate_one_number(self, image_id: int):
        try:
            res = requests.get(
                f'{self.host}/{image_id}',
                headers  = {'Accept': 'image/*'},
                timeout = self.timeout
            )

            res.raise_for_status()

            if 'image' not in res.headers['Content-Type']:
                logging.error('image not found')
                return {'error': 'image not found'}, 404

            return {'image_data': res.content}, 200

        except Timeout:
            logging.error(f'timeout {image_id}')
            return {'error': f'timeout {image_id}'}, 408
        except RequestException as reqerror:
            logging.error('image not found')
            return {'error': 'image not found'}, 404

    # def read_plate_several_numbers(self, im: list(int)):
    #     try:
    #         res = requests.get(
    #             f'{self.host}/{im}', 
    #             headers= {'Accept': 'image/*'},
    #             timeout=self.timeout,
    #         )
    #         res.raise_for_status()

    #     except requests.exceptions.HTTPError:  
    #         logging.error('error while doownloading image')
    #         return {'error': 'image not found'}, 400

    #     except Timeout: 
    #         logging.error(f'timeout error')
    #         return {'error': f'timeout error'}, 400

    #     return res.content, 200


if __name__ == '__main__':
    client = ImageReaderClient(host='http://89.169.157.72:8080/images')
    res = client.read_plate_one_number(49965)
    print(res)