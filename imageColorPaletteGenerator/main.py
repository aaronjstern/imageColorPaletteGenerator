import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = 'static'
        UPLOAD_FOLDER = path
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        my_img = Image.open(f'static/{filename}')
        img_array = np.array(my_img)
        pixel_list = img_array.reshape(-1, 3)
        unique, counts = np.unique(pixel_list, axis=0, return_counts=True)
        counts_sorted = np.sort(counts)[-10:]
        unique = unique.tolist()
        counts_sorted = counts_sorted.tolist()
        counts = counts.tolist()
        top_10 = [unique[counts.index(count)] for count in counts_sorted]

        return render_template('imagePalette.html', filename=filename, top_10=top_10)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename), code=301)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
