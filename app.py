from flask import Flask, render_template, request
import os
import pydicom
import numpy as np
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/dcm_upload')
def dcm_upload():
    return render_template("upload.html")

@app.route('/upload', methods=["POST"])
def upload_dic():
    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    if not file.filename:
        return "No file selected"

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        ds = pydicom.dcmread(filepath)
        
        img = ds.pixel_array.astype(float)

        img -= np.min(img)
        img /= np.max(img)
        
        img = (img*255).astype(np.uint8)

        img = Image.fromarray(img)

        # img_file = f"{file.filename}.png"
        # img_path = os.path.join(IMAGE_FOLDER, img_file)
        # img.save(img_path)

    # placeholders we need to send the image to the model for prediction later when we have the model
        return "saved"
    else:
        return "file not found"


if __name__ == "__main__":
    app.run(debug=True)
