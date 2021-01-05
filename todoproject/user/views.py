import json
from django.core.checks import messages
from django.urls.conf import path
from django.http import HttpResponse, response

# Create your views here.

from todoproject.response import Response
from todoproject.jwt import JWTAuth
from todoproject.middleware import jwtRequired
from . import serializer
from .models import Users
from django.views.decorators.csrf import csrf_exempt

from . import views

# @jwtRequired
def index(request):
    # return HttpResponse("ini index User")
    user = Users.objects.all()
    print(user)
    user = serializer.serializer(user)
    return Response.ok(values=user)

@jwtRequired
def show(request, id):
    print(request.META['DATA'])
    user = Users.objects.filter(id=id).first()
    if not user:
        return Response.badRequest(message="pengguna tidak ditemukan")
    
    user = serializer.singleTransform(user)
    
    return Response.ok(values=user)

@csrf_exempt
def auth(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        email = json_data['email']

        user = Users.objects.filter(email=email).first()

        if not user:
            return Response.badRequest(message='Pengguna tidak ditemukan!')

        if not json_data['password'] == user.password:
            return Response.badRequest(message="Password atau email yang kamu masukkan salah!")

        user = serializer.singleTransform(user)

        jwt = JWTAuth()
        user['token'] = jwt.encode({"user_email": user['email']})
        return Response.ok(values=user, message="Berhasil masuk!")

@csrf_exempt
def data(request, id):
    print(request.method)
    if request.method == 'GET':
        if id == 0:
            user = Users.objects.all()
            user = serializer.serializer(user)
            return Response.ok(values=user)
        else:
            user = Users.objects.filter(id=id).first()
            if not user:
                return Response.badRequest(message="pengguna tidak ditemukan")
            user = serializer.singleTransform(user)
            
            return Response.ok(values=user)
    elif request.method == 'PUT':
        json_data = json.loads(request.body)

        user = Users.objects.filter(id=id).first()
        if not user:
            return Response.badRequest(message="Pengguna tidak ditemukan")
        user.name = json_data['name']
        user.email = json_data['email']
        user.password = password=json_data['password']
        user.save()

        return Response.ok(
            values=serializer.singleTransform(user),
            message="Updated!"
        )
    elif request.method == 'POST':
        json_data = json.loads(request.body)
        
        user = Users()
        user.name = json_data['name']
        user.email = json_data['email']
        user.password = json_data['password']
        user.save()
        
        return Response.ok(values=serializer.singleTransform(user), message="added successfully")
    elif request.method == 'DELETE':
        user = Users.objects.filter(id=id).first()
        if not user:
            return Response.badRequest(message="Pengguna tidak ditemukan")
        
        user.delete()
        return Response.ok(message="Deleted!")
    else:
        return Response.badRequest(message="Invalid method!")