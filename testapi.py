import requests

url = "http://127.0.0.1:5000/product"
response = requests.request("GET", url)
result = response.json()
a = []
b = []
c = []
for i in result :
    if 0 <= i['id'] <= 24 :
        a.append(i)
    if 25 <= i['id'] <= 48 :
        b.append(i)
    if 49 <= i['id'] <= 72 :
        c.append(i)

for i in a :
    print(i['name'])