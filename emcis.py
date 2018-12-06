import os
from flask import Flask, flash, request, redirect, url_for,jsonify
from werkzeug.utils import secure_filename
import createGraph
import createRelayGraph
import wc

UPLOAD_FOLDER = 'up'
ALLOWED_EXTENSIONS = set(['mbox'])

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_page ():
    return '''<form id='picture-file-input-button' action='/upload' method='post' enctype='multipart/form-data' encoding='multipart/form-data'>
    <input  type='file' name='file' />
    <input type = "submit"/>
</form>'''


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'no file path'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        data = createGraph.run(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data['relayGraph'] = createRelayGraph.run(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = wc.run(os.path.join(app.config['UPLOAD_FOLDER'], filename),data)

    return jsonify(data)
