import os
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import shutil

app = Flask(__name__)
#app._static_folder = './templates/'
DOWNLOAD_DIRECTORY = "./photos"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = DOWNLOAD_DIRECTORY
app.secret_key = "ksljgkldgjlk"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict/<filename>')
def predict(filename):
    nutr = pd.read_excel('products.xlsx', header=0).set_index('Unnamed: 0')
    nutr.columns = ['name', 'kcal', 'protein', 'fat', 'carbohydrate', 'label']
    labels = pd.read_excel('products.xlsx', header=None, sheet_name='Лист1').to_dict()[0]
    os.system("python yolov5/detect.py --weights epoch62.pt --conf 0.05 --source ./photos/photo.jpg --save-txt --save-conf --name food")
    #shutil.move('./yolov5/runs/detect/food/photo.jpg', 'static/photo.jpg')
    try:
        output = pd.read_csv('./yolov5/runs/detect/food/labels/photo.txt', sep=' ', header=None)
    except:
        return None
    output.columns = ['label', 'coord1', 'coord2', 'coord3', 'coord4', 'conf']
    output.sort_values('conf', ascending=False)
    output.label = output.label.replace(labels)
    df=nutr[nutr.label.isin(output.label)].set_index('name')#.drop('Unnamed: 0', axis=1)
    results=df.T.to_json(force_ascii=False)#.encode('utf-8')
    shutil.rmtree("./yolov5/runs/detect/food")
    return results


@app.route('/nutrition',methods = ['POST'])
def getphoto():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return('No file part')

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'photo.jpg'))
            return redirect(url_for('predict', filename=filename))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')