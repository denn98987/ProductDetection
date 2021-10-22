import os
from flask import Flask, request

UPLOAD_FOLDER = './'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

if __name__ == '__main__':
    app.run()
