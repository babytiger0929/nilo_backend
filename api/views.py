from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article

import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyAIAXzSik1K75v1yhB9MEx0hl6xpqYmSvM",
  "authDomain": "nilo-f8b40.firebaseapp.com",
  "databaseURL": "https://nilo-f8b40.firebaseio.com",
  "projectId": "nilo-f8b40",
  "storageBucket": "nilo-f8b40.appspot.com",
  "messagingSenderId": "840005357071",
  "appId": "1:840005357071:web:9c47d5321c3fdad1aa1d7a",
  "measurementId": "G-49VVG5C9RS"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


class AuthView(APIView):
    def post(self, request):
        response = {
            'access_token': '',
            'refresh_token': '',
            'debug': ''
        }
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    firebase_user = auth.sign_in_with_email_and_password(user.email, password)
                    response['access_token'] = firebase_user['idToken']
                    response['refresh_token'] = firebase_user['refreshToken']
                except Exception as e:
                    print(e)
                    response['debug'] = 'Invalid credentials'
            else:
                response['debug'] = 'Invalid credentials'
        else:
            response['debug'] = 'Missing Argument'
        return Response(response)


class HelloView(APIView):
    def get(self, request):
        response = {
            'article': [],
            'debug': ''
        }
        try:
            token = str(request.META['HTTP_AUTHORIZATION']).split(' ')[1]
            firebase_user = auth.get_account_info(token)
            if firebase_user:
                articles = Article.objects.all().order_by('id')
                for item in articles:
                    articleObj = {
                        'id': item.id,
                        'title': item.title,
                        'content': item.content
                    }
                    response['article'].append(articleObj)
            return Response(response)
        except Exception as e:
            print(e)
            response['debug'] = 'Unauthorized'
            return Response(response, status=401)
