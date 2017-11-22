from web_rekollect import app, db
import models

import os
from flask import Flask, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = set(['vmem', 'dd'])
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

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
            # TODO: Check if filename already exists
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Insert database function to create row in "files" table
            file_db = models.Files(file_name=filename)
            db.session.add(file_db)
            db.session.commit()

            return redirect(url_for('upload'))

    # If a GET request, pull all current files
    results = models.Files.query.all()
    #return str(results)
    return render_template('upload.html', results=results)

@app.route('/file/<file_name>')
def file_info(file_name):
    '''Displays basic information about the memory image upload'''
    file_dbresult = models.Files.query.filter_by(file_name=file_name).first()
    file_id = file_dbresult.id
    plugin_result = models.Results.query.filter_by(file_id=file_id).all()

    if not plugin_result:
        print("Debug did not find results")
        file_path = os.path.join("uploads", file_name)
        file_object = rekollect.Rekollect(file_path)

        imageinfo = models.Results(file_id=file_id, plugin="imageinfo",
                                   result=file_object.imageinfo)
        pslist = models.Results(file_id=file_id, plugin="pslist",
                                result=file_object.pslist)
        networkconns = models.Results(file_id=file_id, plugin="networkconns",
                                      result=file_object.networkconns)
        filescan = models.Results(file_id=file_id, plugin="filescan",
                                  result=file_object.filescan)
        shimcache = models.Results(file_id=file_id, plugin="shimcache",
                                result=file_object.shimcache)

        db.session.add_all([imageinfo, pslist, networkconns,
                            filescan, shimcache])
        db.session.commit()

        plugin_result = models.Results.query.filter_by(file_id=file_id).all()

    results={}
    for result in plugin_result:
        results[result.plugin] = result.result

    return render_template("file_info.html", file_name=file_name,
                           results=results)
