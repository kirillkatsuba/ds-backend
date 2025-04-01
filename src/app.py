from models.plate_reader import PlateReader, InvalidImage
from image_client import ImageReaderClient
from plate_reader_client import PlateReaderCLient
from flask import Flask, request
import logging
import io
import PIL

app = Flask(__name__)


plate_reader_model = PlateReader.load_from_file('/app/model_weights/plate_reader_model.pth')


@app.route('/plate_reader', methods=['POST'])
def plate_reader():
    data = request.get_data()
    im = io.BytesIO(data)
    try:
        result = plate_reader_model.read_text(im)
    except PIL.UnidentifiedImageError:
        logging.error('Invalid image')
        return {'error': 'Invalid image'}, 400
  
    return {'result': result}


@app.route('/get_image/<int:im>', methods=['GET'])
def get_image(im: int):
    client_image = ImageReaderClient(host='http://89.169.157.72:8080/images/')
    binary_image = client_image.read_plate_one_number(im)

    if binary_image['status_code'] != 200:
        return {'exepction': binary_image['error']}

    client = PlateReaderCLient(host='http://127.0.0.1:8080')
    result = client.read_plate_number(binary_image['image_data'])['result']

    return {'result': result}


@app.route('/get_image/<string:ims>', methods=['GET'])
def get_several_images(ims: str):
    result = {}
    ims_ids = list(map(int, ims.split(',')))
    for im in ims_ids:
        result[im] = get_image(im)

    return result



if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.run(host='0.0.0.0', port=8080, debug=True)
