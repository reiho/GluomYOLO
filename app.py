import os
from flask import Flask, request, redirect, url_for
import pandas as pd
import shutil
import uuid


app = Flask(__name__)
#app._static_folder = './templates/'
DOWNLOAD_DIRECTORY = "./photos"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = DOWNLOAD_DIRECTORY
app.secret_key = "ksljgkldgjlk"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict/<filename>')
def predict(filename):
    if os.path.exists('./yolov5/runs/detect/'):shutil.rmtree("./yolov5/runs/detect/")
    nutr = pd.read_excel('products.xlsx', header=0).set_index('Unnamed: 0')
    nutr.columns = ['name', 'protein', 'fat', 'carbohydrate', 'kcal', 'label', 'priority', 'short_name']
    labels = {}
    with open('food.yaml', 'r') as f:
        start = False
        for line in f:
            if start:
                num, name = line.strip().split(': ')
                labels[int(num)] = name
            if 'names:' in line:
                start = True
    os.system("python yolov5/detect.py --weights best.pt --conf 0.005 --source ./photos/{0}.jpg --save-txt --save-conf --name food".format(filename))
    os.remove("./photos/{}.jpg".format(filename))
    try:
        output = pd.read_csv('./yolov5/runs/detect/food/labels/{}.txt'.format(filename), sep=' ', header=None)
    except:
        return {}
    output.columns = ['label', 'coord1', 'coord2', 'coord3', 'coord4', 'conf']

    output=output.sort_values('conf', ascending=False).reset_index(drop=True)

    output.label = output.label.replace(labels)
    #print(output)
    sort = output.label.to_dict()
    inv_sort = {v: k for k, v in sort.items()}
    #print(inv_sort)
    df=nutr[nutr.label.isin(output.label)].sort_values(by='label', key=lambda x: x.replace(inv_sort))
    df.loc[~df.short_name.isna(), 'name']=df.loc[~df.short_name.isna(), 'short_name']
    df = df.set_index('name').drop('short_name', axis=1)
    results=df.T.to_json(force_ascii=False)#.encode('utf-8')
    return results
