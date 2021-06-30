BASE_URI = " http://192.168.0.115:5000/api/people"
COVID_TRACKER_HOST = "http://127.0.0.1:3000/"


def get_user_url(id):
    url = f'{BASE_URI}/{id}'
    return url