import requests


class PlateReaderCLient:
    def __init__(self, host: str):
        self.host = host

    def read_plate_number(self, im):
        res = requests.post(
            f'{self.host}/plate_reader', 
            headers= {'Content-Type': 'application/json'}, 
            data=im,
        )
        
        return res.json()


if __name__ == '__main__':
    client = PlateReaderCLient(host='http://127.0.0.1:8080')
    with open('./images/9965.jpg', 'rb') as im:
        res = client.read_plate_number(im)
        print(res)