import os
import base64
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

UPLOAD_FOLDER = './'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

upload_url = "https://api.imgbb.com/1/upload"
url        = 'https://yandex.ru/images/search?source=collections&rpt=imageview&url={}'

@app.route('/', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'there is no image in form!'
        image = request.files['image']
        bytes = image.stream.read(-1)
        path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(path)
        return bytes

        return 'ok'
    return '''
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="image">
      <input type="submit">
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/image', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            response = jsonify({'message': 'No image in the request'})
            response.status_code = 400
            return response

        image = request.files['image']
        if image and allowed_file(image.filename):
            bytes = image.stream.read(-1)
            upload_payload = {
                "key": "a1056afe4fc43e55f96035117bafb14f",
                "image": base64.b64encode(bytes),
            }
            upload_response = requests.post(upload_url, upload_payload).json()
            image_url = upload_response["data"]["display_url"]
            print(image_url)
            soup = BeautifulSoup(requests.get(url.format(image_url)).text, 'lxml')
            similar = soup.find_all('div', class_='CbirSites-ItemTitle')
            links = []
            for i in similar:
                print(i.find('a').get('href') + "\n")
                links.append(i.find('a').get('href'))

            response = jsonify({'links': links})
            response.status_code = 200
            return response
        else:
            response = jsonify({'message': 'File type is not allowed'})
            response.status_code = 400
            return response


if __name__ == '__main__':
    app.run()
