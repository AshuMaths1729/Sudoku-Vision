from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads,IMAGES
import re
import sys
import os
import digitRecog
import solver
import boardDetector
import getopt
import cv2 as cv
import numpy as np

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = '.'
configure_uploads(app, photos)

@app.route('/')
def index():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        os.rename(filename, 'output.jpg')
    rs = boardDetector.detector()
    os.remove('output.jpg')
    return render_template("result.html",res = rs.astype(int))


if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='127.0.0.1', port=port)