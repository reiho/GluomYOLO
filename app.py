import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import pandas as pd
import shutil

app = Flask(__name__)
#app._static_folder = './templates/'
DOWNLOAD_DIRECTORY = "./photos"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = DOWNLOAD_DIRECTORY

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict(filename):
    nutr = pd.read_excel('products.xlsx', header=0).set_index('Unnamed: 0')
    nutr.columns = ['name', 'kcal', 'protein', 'fat', 'carbohydrate', 'label']
    labels = pd.read_excel('products.xlsx', header=None, sheet_name='Лист1').to_dict()[0]
    os.system("python yolov5/detect.py --weights best.pt --conf 0.05 --source ./photos --save-txt --save-conf --name food")
    shutil.move('./yolov5/runs/detect/food/photo.'+filename.rsplit('.', 1)[1], 'static/photo.jpg')
    output = pd.read_csv('./yolov5/runs/detect/food/labels/photo.txt', sep=' ', header=None)
    output.columns = ['label', 'coord1', 'coord2', 'coord3', 'coord4', 'conf']
    output.label = output.label.replace(labels)
    df=nutr[nutr.label.isin(output.label)]
    df.to_html('static/table.html')
    shutil.rmtree("./yolov5/runs/detect/food")

@app.route('/results',methods = ['GET','POST'])
def show_results():
    return render_template('results.html')

@app.route('/',methods = ['GET','POST'])
def getphoto():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'photo.'+filename.rsplit('.', 1)[1]))
            predict(filename)
            return redirect('/results')
            #redirect(url_for('download_file', name=filename))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
