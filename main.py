import requests as rq
from url import base_url as bu

name = input("Enter name: ")
job = input("Enter job: ")

request_data = dict()
request_data['name'] = name
request_data['job'] = job

url = bu.call_post_api()
response = rq.post(url=url, data=request_data)
if response.status_code == 201:
    print(response.json())
else:
    print("Something went wrong!!")
