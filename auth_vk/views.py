import requests
from django.shortcuts import render, redirect


# https://vk.com/dev
VK_CLIENT_ID = '6043918'
VK_CLIENT_SECRET = 'dVWjoKT3W2taZ1AoS6dH'
# https://vk.com/dev/access_token
REDIRECT_URL = 'http://127.0.0.1:8005/authorize/'


# Show page authorization
def viewLogin(request):
    result = None
    if 'access_token_user' in request.session:
        result = redirect('/profile/')
    else:
        result = render(request, 'login.html')
    return result


# Get code, access_token then user info and user friends info
def authorizeVK(request):
    result = None
    if not request.GET:
        # try:
        #     if not request.GET:
        # Open new tab, get code for getting access_token
        # example answer server vk.com: REDIRECT_URI?code=41b93f4831f1466548
        # user will have to authorize in and allow the application
        result = redirect('https://oauth.vk.com/authorize?'
                          'client_id=' + VK_CLIENT_ID +
                          '&display=mobile'
                          '&redirect_uri=' + REDIRECT_URL +
                          '&scope=friends,offline'
                          '&response_type=code'
                          '&v=5.64')
    elif 'error' not in request.GET:
        # get code of answer server Vk.com
        code = request.GET['code']

        # get access_token, user_id, expires_in
        # example answer server Vk.com:
        # {"access_token":"533bacf01e11f55b536a565b57531ac114461ae8736d6506a3",
        # "expires_in":43200, "user_id":66748}
        request.session['access_token_user'] = requests.get('https://oauth.vk.com/access_token?'
                                                            'client_id=' + VK_CLIENT_ID +
                                                            '&client_secret=' + VK_CLIENT_SECRET +
                                                            '&redirect_uri=' + REDIRECT_URL +
                                                            '&code=' + code).json()
        result = redirect('/profile/')
    else:
        result = redirect('/')

    return result


# Show page profile
def showVK(request):
    result = None
    if 'access_token_user' in request.session:
        # get user info
        user_get = requests.get('https://api.vk.com/method/users.get?'
                                'user_ids=' + str(request.session['access_token_user']['user_id']) +
                                '&fields=photo_200,bdate,country,city'
                                '&lang=ru'
                                '&v=5.64').json()
        # get info about user friends
        users_get = requests.get('https://api.vk.com/method/friends.get?'
                                 'order=random'
                                 '&count=5'
                                 '&fields=nickname,photo_50'
                                 '&access_token=' + request.session['access_token_user']['access_token'] +
                                 '&lang=ru'
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

        users = {}
        for i in users_get['response']['items']:
            _id = i['id']
            users[_id] = {
                'id': _id,
                'first_name': i['first_name'],
                'last_name': i['last_name'],
                'photo_50': i['photo_50'],
            }

        context = {
            'user': user,
            'users': users,
        }
        result = render(request, 'profile.html', context)
    else:
        result = redirect('/')
    return result


# Logout user
def userLogout(request):
    del request.session['access_token_user']
    return redirect('/')
