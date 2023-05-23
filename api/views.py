
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from api.serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User, Group
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
import json
# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    userSerialized = UserSerializer(user, many=False)
    return Response({'response':userSerialized.data}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#### Gestion de Usuarios #####
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer

@api_view(['GET'])
@permission_classes([IsAdminUser])
def listUsers(request):
    users = User.objects.all()
    usersSerializerds = UserSerializer(users, many=True)
    return Response({'response':usersSerializerds.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def delUser(request, pk):
    if pk:
        try:
            user = User.objects.get(id=pk)
            user.delete()
            return Response({'msg':'Done'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'msg': 'User not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def updUser(request):
    if request.POST.get('id'):
        try:
            user = User.objects.gte(id=request.POST.get('id'))
            user.username = request.POST.get('username')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.is_staff = request.POST.get('is_staff')
            user.is_active = request.POST.get('is_active')
            user.save()
            return Response({'msg':'Done'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'msg': 'User not exist'}, status=status.HTTP_404_NOT_FOUND)

class UpdUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    lookup_field = 'pk'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserGroups(request):
    queryset = request.user.groups.all()
    groups = GroupSerializer(queryset, many=True)
    return JsonResponse(data=groups.data, status=status.HTTP_200_OK, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def getUsersGroups(request,pk):
    if pk:
        user = User.objects.get(id=pk)
        groups = GroupSerializer(user.groups.all(), many=True)
        return JsonResponse(data=groups.data, status=status.HTTP_200_OK, safe=False)
    else:
        return JsonResponse(data={'msg':'No user has provided'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def setUserGroup(request):
    jsonData = json.loads(request.body)
    print(jsonData)
    # return JsonResponse(data={'msg':'done'}, status=status.HTTP_200_OK)
    if jsonData['userId']:
        user = User.objects.get(id=jsonData['userId'])
        if jsonData['groups']:
            for group in jsonData['groups']:
                if not user.groups.filter(name=[group]):
                    grp = Group.objects.get(name=group)
                    user.groups.add(grp)
            return JsonResponse(data={'msg':'done'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse(data={'msg':'No groups are specified'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data={'msg':'No user are specified'}, status=status.HTTP_400_BAD_REQUEST)




### Groups ###

class ListGroups(generics.ListAPIView):
    queryset = Group.objects.all()
    #permission_classes = (IsAdminUser,)
    serializer_class = GroupSerializer

class CreateGroup(generics.CreateAPIView):
    queryset = Group.objects.all()
    # permission_classes = (IsAdminUser,)
    serializer_class = GroupSerializer

class DetailGroup(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = GroupSerializer

class UpdateGroup(generics.UpdateAPIView):
    queryset = Group.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = GroupSerializer

class DeleteGroup(generics.DestroyAPIView):
    queryset = Group.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = GroupSerializer

### Permissions ###
class ListPermissions(generics.ListAPIView):
    queryset = Permission.objects.all()
    permission_classes(IsAdminUser,)
    serializer_class = PermissionSerializer

class DetailPermission(generics.RetrieveAPIView):
    queryset = Permission.objects.all()
    permission_classes(IsAdminUser,)
    serializer_class = PermissionSerializer
