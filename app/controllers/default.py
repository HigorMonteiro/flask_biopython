import os
from flask import (url_for, redirect, render_template,
                   request, send_from_directory)
from werkzeug import secure_filename
from Bio import SeqIO
from app import app

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'fasta']
)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route("/index")
# @app.route("/")
# def index():
#     return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    for i in SeqIO.parse(('uploads/%s' % filename), 'fasta'):
        print(i.id, i.seq)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('index.html')
