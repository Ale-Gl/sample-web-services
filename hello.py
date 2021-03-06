from flask import Flask, request, jsonify, redirect, url_for, abort, render_template, send_file
from joblib import load
import numpy as np
import pandas as pd

from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

import os

knn = load('knn_model.pkl')

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


@app.route('/')
def hello_world():
    # print('hi')
    return '<h1>Hello, Flask</h>'

@app.route('/iris/<params>')
def iris(params):

    params = params.split(',')
    params = [float(param) for param in params]
    params = np.array(params).reshape(1, -1)
    predict = knn.predict(params)
    
    return str(predict)

@app.route('/show_image')
def show_image():
    return '<img src="/static/setosa.jpg" alt="Setosa">'

@app.route('/badrequest400')
def bad_request():
    abort(400)

@app.route('/iris_post', methods=['POST'])
def add_message():

    try:
        content = request.get_json()

        param = content['flower'].split(',')
        param = [float(num) for num in param]
    
        param = np.array(param).reshape(1, -1)
        predict = knn.predict(param)

        predict = {'class':str(predict[0])}
    except:
        return redirect(url_for('bad_request'))

    return jsonify(predict)

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():

        f = form.file.data

        filename = form.name.data + '.csv'
        # f.save(os.path.join('uploads_files/' + filename))

        df = pd.read_csv(f, header=None)
        # print(df.head())

        predict = knn.predict(df)

        result = pd.DataFrame(predict)
        result_path = 'predicts/' + filename
        result.to_csv(result_path, index=False)   

        return send_file(result_path,
                     mimetype='text/csv',
                     attachment_filename=filename,
                     as_attachment=True)
        
    return render_template('submit.html', form=form)


import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads_files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '<h1>File was uploaded</h>'
            
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''