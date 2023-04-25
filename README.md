# GluomYOLO
Для установки (желательно в виртуальную среду):
```
git clone https://github.com/reiho/GluomYOLO.git
cd GluomYOLO
git clone https://github.com/ultralytics/yolov5
pip install -qr YOLOrequirements.txt
pip install -qr requirements.txt
gdown --id 1-dS8PluXl441RiHuzuQyOza4vJ4ccbmW
python app.py
```
Будет выдано 2 адреса, второй доступен всем устройствам в той же сети:
```
 * Running on http://127.0.0.1:5000
 * Running on http://*.*.*.*:5000
```

## Пример использования (Python)
```ruby
import requests
import json
photo = {'file': open('./photos/960m.jpg', 'rb')}
response = requests.post("http://127.0.0.1:5000/nutrition", files=photo)
json.loads(response.text)
```
Вывод:
```ruby
{'Омлет': {'kcal': 9.6,
  'protein': 15.4,
  'fat': 1.9,
  'carbohydrate': 184.0,
  'label': 'omelet'},
 'Омлет из взбитых сливок': {'kcal': 6.4,
  'protein': 14.8,
  'fat': 26.2,
  'carbohydrate': 257.0,
  'label': 'omelet'},
 'Омлет из яичного порошка': {'kcal': 10.3,
  'protein': 17.0,
  'fat': 1.6,
  'carbohydrate': 200.0,
  'label': 'omelet'},
 'Омлет с сыром': {'kcal': 16.3,
  'protein': 29.7,
  'fat': 2.6,
  'carbohydrate': 342.0,
  'label': 'omelet'}}
  ```
