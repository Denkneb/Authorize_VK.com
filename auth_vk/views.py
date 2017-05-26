import requests
from django.shortcuts import render, redirect
import webbrowser

# https://vk.com/dev
VK_CLIENT_ID = '6043918'
VK_CLIENT_SECRET = 'dVWjoKT3W2taZ1AoS6dH'
# https://vk.com/dev/access_token
REDIRECT_URL = 'http://127.0.0.1:8005/authorize/'


# Show page authorization
def viewLogin(request):
    return render(request, 'login.html')


# Get code, access_token then user info and user friends info
def authorizeVK(request):
    if not request.GET:
        # Open new tab, get code for getting access_token
        # example answer server Vk.com: REDIRECT_URI?code=41b93f4831f1466548
        # user will have to authorize in and allow the application
        webbrowser.open('https://oauth.vk.com/authorize?'
                        'client_id=' + VK_CLIENT_ID +
                        '&display=mobile'
                        '&redirect_uri=' + REDIRECT_URL +
                        '&scope=friends'
                        '&response_type=code'
                        '&v=5.64',
                        new=0, autoraise=True)
        exit()
    else:
        # get code of answer server Vk.com
        code = request.GET['code']

        # get access_token
        # example answer server Vk.com:
        # {"access_token":"533bacf01e11f55b536a565b57531ac114461ae8736d6506a3",
        # "expires_in":43200, "user_id":66748}
        get_token = requests.get('https://oauth.vk.com/access_token?'
                                 'client_id=' + VK_CLIENT_ID +
                                 '&client_secret=' + VK_CLIENT_SECRET +
                                 '&redirect_uri=' + REDIRECT_URL +
                                 '&code=' + code).json()
        access_token = get_token['access_token']
        user_id = str(get_token['user_id'])

        # get user info
        user_get = requests.get('https://api.vk.com/method/users.get?'
                                'user_ids=' + user_id +
                                '&fields=photo_200,bdate,country,city'
                                '&v=5.64').json()
        # get info about user friends
        users_get = requests.get('https://api.vk.com/method/friends.get?'
                                 'order=random'
                                 '&count=5'
                                 '&fields=nickname,photo_50'
                                 '&access_token=' + access_token +
                                 '&v=5.62').json()
        user = {
            'id': user_get['response'][0]['id'],
            'first_name': user_get['response'][0]['first_name'],
            'last_name': user_get['response'][0]['last_name'],
            'bdate': user_get['response'][0]['bdate'],
            'photo_200': user_get['response'][0]['photo_200'],
            'country': user_get['response'][0]['country']['title'],
            'city': user_get['response'][0]['city']['title'],
            'users_count': users_get['response']['count']
        }
        # Send user info to the session
        request.session['user'] = user

        users = {}
        for i in users_get['response']['items']:
            _id = i['id']
            users[_id] = {
                'id': _id,
                'first_name': i['first_name'],
                'last_name': i['last_name'],
                'photo_50': i['photo_50'],
            }
            # Send users info to the session
        request.session['users'] = users

    return redirect('/profile/')


# Show page profile
def showVK(request):
    context = {
        'user': request.session['user'],
        'users': request.session['users']
    }
    return render(request, 'profile.html', context)
