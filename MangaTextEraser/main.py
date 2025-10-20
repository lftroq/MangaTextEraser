import os
import logging
import sys
from flask import Flask, render_template, request, flash, jsonify, current_app, url_for, send_from_directory, redirect
import torch
from PIL import Image
import cv2
import numpy as np
import io
import base64
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bimatbenhocuachungta'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

model = torch.hub.load("ultralytics/yolov5","custom",path='models/best.pt')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST" and "images[]" in request.files:
        files = request.files.getlist("images[]")
        image_pairs = []
        for file in files:
            if file.filename == '':
                continue
            # Process all files
            original_image = Image.open(file.stream)
            processed_image = process_image(original_image)
            original_b64 = convert_image_to_base64(original_image)
            processed_b64 = convert_image_to_base64(processed_image)
            
            image_pairs.append((original_b64, processed_b64))

        return render_template("final.html", image_pairs=image_pairs)
    return render_template("index.html")

@app.route('/final', methods=['GET', 'POST'])
def final():
    if request.method == "POST" and "images[]" in request.files:
        files = request.files.getlist("images[]")
        image_pairs = []
        for file in files:
            if file.filename == '':
                continue
            # Process all files
            original_image = Image.open(file.stream)
            processed_image = process_image(original_image)
            original_b64 = convert_image_to_base64(original_image)
            processed_b64 = convert_image_to_base64(processed_image)

            image_pairs.append((original_b64, processed_b64))

        return render_template("final.html", image_pairs=image_pairs)
    return render_template("index.html")

@app.route('/introduce')
def introduce():
    return render_template('introduce.html')

def process_image(image):
    global model  # Use the pre-loaded model
    results = model(image)

    # Delete text in image
    temp = results.pandas().xyxy[0]

    npimg = np.array(image)
    cnt_rectangle = temp.size
    if(cnt_rectangle > 0): 
        cnt_rectangle = cnt_rectangle // temp.iloc[0].size
    for rec_index in range(cnt_rectangle):
        xmin = int(temp.iloc[rec_index].xmin)
        xmax = int(temp.iloc[rec_index].xmax)
        ymin = int(temp.iloc[rec_index].ymin)
        ymax = int(temp.iloc[rec_index].ymax)
        confidence = temp.iloc[rec_index].confidence
        if (confidence > 0.5):
            # print(xmin, ymin, ": ", npimg[ymin, xmin])
            # print(xmin, ymin, ": ", npimg[ymin, xmin, 0])
            xx = int((xmin + xmax) / 2)
            yy = ymin
            fill_color = (int(npimg[yy, xx, 0]), int(npimg[yy, xx, 1]), int(npimg[yy, xx, 2]))
            # fill_color=(255, 255, 255)
            cv2.rectangle(img=npimg,
                          pt1=(xmin, ymin),
                          pt2=(xmax, ymax),
                          color=(fill_color[0], fill_color[1], fill_color[2]),
                          thickness=-1)

    return Image.fromarray(npimg)  # Convert to PIL Image


def convert_image_to_base64(image):
    """Converts a PIL Image to a Base64 string."""
    img_io = io.BytesIO()
    image.save(img_io, format="JPEG")  # Save image to memory as JPG
    img_io.seek(0)
    return base64.b64encode(
        img_io.getvalue()).decode()  # Convert to Base64 string


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
