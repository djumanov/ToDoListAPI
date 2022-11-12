from django.http import HttpRequest, JsonResponse
from django.views import View
from base64 import b64decode
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Task


def decode_auth(auth_h: str) -> tuple[str]:
    '''decode authtozition
    
    Args:
        auth_h (str): authtozation
        
    Returns:
        tuple: username, password
    '''
    #get token
    token = auth_h.split(' ')[-1]
    #decode the token
    decoded_token = b64decode(token).decode('utf-8')
    #get username and password
    username, password = decoded_token.split(':')

    return username, password


class GetAllTasksView(View):
    '''Get all tasks View'''

    def get(self, request: HttpRequest) -> JsonResponse:
        '''GetAllTasksView's get mathod, get all tasks
        
        Agrs:
            request (HttpRequest): HttpRequest object
            
        Returns:
            JsonResponse: JsonResponse object
        '''
        # get authorization
        auth_header = request.headers.get('Authorization')
        #check auth
        if auth_header:
            #decode auth
            username, password = decode_auth(auth_header)
            # authenticate
            user = authenticate(username=username, password=password)
            #check authenticate
            if user is not None:
                #get user
                user: User = User.objects.get(username=username)
                tasks: list[Task] = Task.objects.filter(user=user).all()
                tasks_json = [task.to_json() for task in tasks]
                return JsonResponse({'tasks': tasks_json})
            return JsonResponse({'error': 'bad request'})


