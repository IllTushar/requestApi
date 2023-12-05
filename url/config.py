from url import end_point as ep

BASE_URL = 'https://reqres.in/'

endpoint = ep.get_user_end_point()


def get_user_list():
    return BASE_URL + endpoint
