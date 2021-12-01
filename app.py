import os
from flask import Flask, request, jsonify

UPLOAD_FOLDER = './'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

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
        app.logger.info(request.files)
        app.logger.info(request.data)
        app.logger.info(request)
        if 'image' not in request.files:
            response = jsonify({'message': 'No image in the request'})
            response.status_code = 400
            return response

        image = request.files['image']
        if image and allowed_file(image.filename):
            bytes = image.stream.read(-1)
            #path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            #image.save(path)
            return 'ok'
        else:
            response = jsonify({'message': 'File type is not allowed'})
            response.status_code = 400
            return response


if __name__ == '__main__':
    app.run()
