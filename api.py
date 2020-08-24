import os
from flask import Flask, flash, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from forecast import forecast

app = Flask(__name__)

UPLOAD_FOLDER = './file'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/test', methods=['GET'])
def test():
	return jsonify({'message' : 'Service is up and running fine.'})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/forecast', methods=['POST'])
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
            date_column = request.form.get('date_column_name',None)
            n_days = request.form.get('n_days',"15")

            return forecast(
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename),
                n_days = int(n_days),
                date_column = date_column
                )
            

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=3001, debug=True)