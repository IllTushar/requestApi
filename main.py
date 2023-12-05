import requests as rq
from url import config as cg

request_data = rq.get(cg.get_user_list())
if request_data.status_code == 200:
    print(request_data.json())
else:
    print("Something went wrong!!")
