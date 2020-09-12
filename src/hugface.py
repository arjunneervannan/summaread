# import requests;
# import json
#
# API_URL = "https://api-inference.huggingface.co/models/t5-base"
# payload = json.dumps("This is a sample input")
# headers = {"Content-Type": "application/json", "Authorization": "Bearer <YOUR_API_KEY>"}
# response = requests.post(API_URL, payload, headers=headers)
# a = response.json()
# print(a)


import hfapi
client = hfapi.Client()

text = ""
a = client.summarization(text)


print(a)