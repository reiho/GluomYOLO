# GluomYOLO
Для установки (желательно в виртуальную среду):
```
git clone https://github.com/reiho/GluomYOLO.git
cd GluomYOLO
git clone https://github.com/ultralytics/yolov5
pip install -qr YOLOrequirements.txt
pip install -qr requirements.txt
gdown --id 1njY8uXfLnGnv9gt775tYUjXAxKUJ9NiH
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
{'Омлет с кетчупом': {'protein': 9.6,
  'fat': 10.5,
  'carbohydrate': 3.2,
  'kcal': 145.2,
  'label': 'omelet',
  'priority': None},
 'Омлет с грибами': {'protein': 5.6,
  'fat': 4.9,
  'carbohydrate': 1.9,
  'kcal': 75.5,
  'label': 'omelet',
  'priority': None},
 'Омлет': {'protein': 9.6,
  'fat': 15.4,
  'carbohydrate': 1.9,
  'kcal': 184,
  'label': 'omelet',
  'priority': 1.0},
...
  ```
Добавлено поле priority, которое идентифицирует приоритетность блюда в категории. Если в поле указано 1.0, значит это блюдо является обобщением всей категории и можно отобразить только его.
