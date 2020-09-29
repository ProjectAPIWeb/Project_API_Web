import requests

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/479101/information"

headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': "f73997d380mshee76f75bdc3642ap12d0b8jsna5c16ec05bbf"
    }

response = requests.request("GET", url, headers=headers)

for i in response.json() :
    print(i)
    for j in i :
        print('\t',j)