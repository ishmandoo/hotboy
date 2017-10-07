from flask import Flask, request, send_from_directory
import os

app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return app.send_static_file('test.html')

@app.route('/img')
def img():
    return app.send_static_file('img.jpg')


@app.route('/update/<update>')
def update(update):
	print update

	conf = ""
	lines = update.split(",")
	conf += "r = %s" % lines[0]
	conf += "\ng = %s" % lines[1]
	conf += "\nb = %s" % lines[2]

	text_file = open("../hotbrain/config.py", "w")
	text_file.write(conf)
	text_file.close()
	return "Calibration updated"


if __name__ == '__main__':
    app.run( host="0.0.0.0")