import os
import config, utils
import model.label_image as model
import model.classes as classes
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = config.uploads
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.errorhandler(404)


@app.route('/')
def index():
    return render_template('index.html', email=config.email, github=config.github)


@app.route('/about/')
def about():
    return render_template('about.html', email=config.email, github=config.github)


@app.route('/classify/', methods=['GET', 'POST'])
def classify():
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
        if file and utils.allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('results',
                                    filename=file.filename))
    return render_template('classify.html', email=config.email, github=config.github)


@app.route('/results/<filename>')
def results(filename):
    duration, results = model.predict(url_for('uploads', filename=filename))
    results = utils.addClassNames(classes.classNames, results)
    return render_template('results.html', filename=filename, duration=duration, results=results, email=config.email, github=config.github)
    

@app.route('/uploads/<path:filename>')
def uploads(filename):
    return send_from_directory(app.root_path + '/' + config.uploads, filename)


@app.route('/links/')
def links():
    return render_template('links.html', email=config.email, github=config.github)


def not_found(e):
  return render_template('404.html', email=config.email, github=config.github)


if __name__ == '__main__':
    app.run(host=config.host, port=8080)
