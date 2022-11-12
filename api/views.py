from datetime import datetime
from django.http import HttpRequest, JsonResponse
from django.views import View
from base64 import b64decode
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Task
from django.core.exceptions import ObjectDoesNotExist


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


class GetAllCompletedTasksView(View):
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
                tasks: list[Task] = Task.objects.filter(user=user).filter(is_completed=True).all()
                tasks_json = [task.to_json() for task in tasks]
                return JsonResponse({'tasks': tasks_json})
            return JsonResponse({'error': 'bad request'})


class GetAllInCompletedTasksView(View):
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
                tasks: list[Task] = Task.objects.filter(user=user).filter(is_completed=False).all()
                tasks_json = [task.to_json() for task in tasks]
                return JsonResponse({'tasks': tasks_json})
            return JsonResponse({'error': 'bad request'})



class GetTaskByIdView(View):
    '''get task by id'''

    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        '''GetTaskByIdView's get mathod, get task by id
        
        Agrs:
            request (HttpRequest): HttpRequest object
            id (int): task id
            
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
                tasks: list[Task] = Task.objects.filter(user=user).filter(id=id).all()
                tasks_json = [task.to_json() for task in tasks]
                return JsonResponse({'tasks': tasks_json})
            return JsonResponse({'error': 'bad request'})


class AddTaskView(View):
    '''create task'''

    def post(self, request: HttpRequest) -> JsonResponse:
        '''create task
        
        Agrs:
            request (HttpRequest): HttpRequest object
            id (int): task id
            
        Returns:
            JsonResponse: JsonResponse object
        '''
        auth_header = request.headers.get('Authorization')
        if auth_header:
            username, passwrod = decode_auth(auth_header)
            user = authenticate(username=username, password=passwrod)
            if user is not None:
                user = User.objects.get(username=username)
                title = request.POST.get('title')
                deudate = request.POST.get('duedate')
                if title and deudate:
                    task = Task.objects.create(
                        title=title,
                        description=request.POST.get('description', ''),
                        duedate=datetime.strptime(deudate, '%Y-%m-%dT%H:%M:%SZ'),
                        importance=request.POST.get('importance', 0),
                        user=user
                    )
                    task.save()
                    return JsonResponse({'task': task.to_json()})
                return JsonResponse({'error': 'title and duedate are required'})
            return JsonResponse({'error': 'user not registred'})
        return JsonResponse({'error': 'bad request'})


class EditTaskView(View):
    '''update task'''

    def post(self, request: HttpRequest, id: int) -> JsonResponse:
        '''create task
        
        Agrs:
            request (HttpRequest): HttpRequest object
            id (int): task id
            
        Returns:
            JsonResponse: JsonResponse object
        '''
        auth_header = request.headers.get('Authorization')
        if auth_header:
            username, passwrod = decode_auth(auth_header)
            user = authenticate(username=username, password=passwrod)
            if user is not None:
                try:
                    task: Task = Task.objects.get(id=id)
                    title = request.POST.get('title')
                    if title:
                        task.title = title
                    description = request.POST.get('description')
                    if description:
                        task.description = description
                    deudate = request.POST.get('duedate')
                    if deudate:
                        task.duedate = datetime.strptime(deudate, '%Y-%m-%dT%H:%M:%SZ')
                    importance = request.POST.get('importance')
                    if importance:
                        task.importance = importance
                    task.save()
                    return JsonResponse({'task': task.to_json()})
                except ObjectDoesNotExist:
                    return JsonResponse({'error': 'not available task'})
            return JsonResponse({'error': 'user not registred'})
        return JsonResponse({'error': 'bad request'})


class DoneTaskView(View):
    '''done task'''

    def post(self, request: HttpRequest, id: int) -> JsonResponse:
        '''done task
        
        Agrs:
            request (HttpRequest): HttpRequest object
            id (int): task id
            
        Returns:
            JsonResponse: JsonResponse object
        '''
        auth_header = request.headers.get('Authorization')
        if auth_header:
            username, passwrod = decode_auth(auth_header)
            user = authenticate(username=username, password=passwrod)
            if user is not None:
                try:
                    task: Task = Task.objects.get(id=id)
                    if task.is_completed: task.is_completed = False
                    else: task.is_completed = True
                    task.save()
                    return JsonResponse({'task': task.to_json()})
                except ObjectDoesNotExist:
                    return JsonResponse({'error': 'not available task'})
            return JsonResponse({'error': 'user not registred'})
        return JsonResponse({'error': 'bad request'})
