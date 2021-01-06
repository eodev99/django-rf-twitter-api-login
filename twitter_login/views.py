import oauth2 as oauth
import urllib.parse
import requests
import json

from django.shortcuts import redirect
from django.http import JsonResponse

from allauth.socialaccount.models import SocialApp
from rest_framework.views import APIView

class TwitterRequestToken(APIView):
    def post(self, request, *args, **kwargs):
        request_token_url = 'https://api.twitter.com/oauth/request_token'
        app = SocialApp.objects.filter(name='TwitterApplication').first()
        if app and app.client_id and app.secret:
            consumer = oauth.Consumer(app.key, app.secret)
            client = oauth.Client(consumer)

            resp, content = client.request(request_token_url, "GET")

            if resp['status'] != '200':
                raise Exception("Invalid response {}".format(resp['status']))
        
            request_token = dict(
                urllib.parse.parse_qsl(content.decode("utf-8")))
            return JsonResponse(request_token)
        raise Exception("Bad App")

class TwitterCompleteLogin(APIView):
    def post(self, request, *args, **kwargs):
        authorize_url = 'https://api.twitter.com/oauth/access_token'
        request_params = dict(request.query_params)
        app = SocialApp.objects.filter(name='TwitterApplication').first()

        if app and app.client_id and app.secret:
            data = {
                    "oauth_consumer_key": app.key,
                    "oauth_verifier": request_params["oauth_verifier"][0],
                    "oauth_token": request_params["oauth_token"][0]
            }

            response = requests.post(authorize_url, data=data)
            response = dict(urllib.parse.parse_qsl(response.text))

            return JsonResponse(response)
        raise Exception("Bad App")
        

