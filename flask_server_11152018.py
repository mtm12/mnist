from keras.models import load_model
import tensorflow as tf
import numpy as np
import pandas as pd
import ip_address
from flask import Flask, abort, jsonify, request
from PIL import Image, ImageFilter
import base64
import io

app = Flask(__name__)
mnistModel = None


def imageprepare(argv):
    """
    This function returns the pixel values.
    The imput is a png file location.
    """
    #im = Image.open(argv).convert('L')
    print("OK")
    im = Image.open(io.BytesIO(base64.b64decode(argv)))
    print("OK2")
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (28, 28), (255))  # creates white canvas of 28x28 pixels

    if width > height:  # check which dimension is bigger
        # Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width
        if (nheight == 0):  # rare case but minimum is 1 pixel
            nheight = 1
            # resize and sharpen
        img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight) / 2), 0))  # calculate horizontal position
        newImage.paste(img, (4, wtop))  # paste resized image on white canvas
    else:
        # Height is bigger. Heigth becomes 20 pixels.
        nwidth = int(round((20.0 / height * width), 0))  # resize width according to ratio height
        if (nwidth == 0):  # rare case but minimum is 1 pixel
            nwidth = 1
            # resize and sharpen
        img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth) / 2), 0))  # caculate vertical pozition
        newImage.paste(img, (wleft, 4))  # paste resized image on white canvas

    # newImage.save("sample.png

    tv = list(newImage.getdata())  # get pixel values
    #tv = newImage.getdata()
    tv1 = np.array(tv)
    #tv1 = np.array(newImage)
    
    #tv2 = tv1.astype('float32')
    
    #tv2 = tv1.reshape(28,28)
    # normalize pixels to 0 and 1. 0 is pure white, 1 is pure black.
    #tva = [(255 - x) * 1.0 / 255.0 for x in tv]
    #print(tva)
    #return tva
    #tv2 = abs(np.subtract(tv2, 255))
    
    #tv3 = np.array2string(tv2, separator=',')
    #print(tv)
    #print(tv2)

    return tv
	
def testFunc():
	z="1"
	return z
@app.route("/mnist/api", methods=['POST'])
def make_predict():
	data = request.get_json(force=True)
	predict_request = data['image']
	#print(predict_request)
	#b64data = base64.encodestring(open("mnist/digit2.png","rb").read())
	#print("predict request")
	#predict_request_split = predict_request.split(',')[1]
	#print(predict_request_split)
	decoded_image = Image.open(io.BytesIO(base64.b64decode(predict_request.split(',')[1])))
	#print("end predict request")
	#decoded_image.save("mnist/image.png")
	#print("b64data")
	#print(b64data)
	#print("end b64data")
	#print("decoded image")
	#print(decoded_image)
	#y_pred = testFunc()
	#data = imageprepare(decoded_image)
	#data = imageprepare(b64data)
	#data = imageprepare('./mnist/digit2.png')
    #print(data)
	tv = list(decoded_image.getdata())
	y = np.array(tv)
	z = y[:,3:]
	y = z.reshape(28, 28)
	y = np.expand_dims(y, axis=0)
	y = np.expand_dims(y, axis=3)
	#print(y.shape)
	#print(data)
	
	#predict_request = np.array([predict_request])
	predictions = mnistModel.predict(y)
	#print(predictions)
	predictions_class = np.argmax(predictions[0],axis=0)
	print(predictions_class)
	probability = predictions[0][predictions_class]
	print(probability)
	#predictions_class
	#data = imageprepare(predict_request)
	#y_pred = "OK"
	# return jsonify({'setosa': str(y_pred[0][0]),
		# 'versicolor': str(y_pred[0][1]),
		# 'virginica': str(y_pred[0][2])}), 201
	return jsonify({'digit': str(predictions_class),
			'probability': str(probability)}), 201

	
@app.route("/test/api")
def hello():
	a = "20"
	return jsonify({'value': a}), 201

if __name__=='__main__':
	#print("loading iris model")
	#irisModel = load_model('iris_model.h5')
	#print("iris model loaded")
	print("loading mnist model")
	mnistModel = load_model('./mnist/mnist_model.h5')
	print("mnist model loaded")
	app.run(host=ip_address.ip_address, port=5001)