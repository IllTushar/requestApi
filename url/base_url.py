from url import end_point as ep

BASE_URL = 'https://reqres.in'


def call_post_api():
    return BASE_URL + ep.post_user()
