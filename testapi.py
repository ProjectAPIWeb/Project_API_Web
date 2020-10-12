import requests

url = "https://edamam-edamam-nutrition-analysis.p.rapidapi.com/api/nutrition-data"

querystring = {"ingr":"1 large apple"}

headers = {
    'x-rapidapi-host': "edamam-edamam-nutrition-analysis.p.rapidapi.com",
    'x-rapidapi-key': "1c4f2121d7msh1922e0add153d9cp1a84eejsnb581979b3390"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)