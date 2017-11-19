from web_rekollect import app

import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = set(['vmem', 'dd'])
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return "Welcome to Rekollect!"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # check if the post request has the file part
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if use does not select file, browser should return to request url
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Insert database function to create row in "files" table
            return redirect(url_for('index'))

    return '''
    <! doctype html>
    <title>Upload new file</title>
    <h1>Upload new file</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
        <input type=submit value=Upload>
    </form>
    '''
