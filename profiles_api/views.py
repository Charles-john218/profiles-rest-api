from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework import viewsets
from . import models
from . import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken  
from rest_framework.authtoken.models import Token

# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handles creating, creating and updating profiles """
    
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)
    
class LoginViewSet(viewsets.ViewSet):
        """Checks email and password and returns an auth token"""
        
    
        serializer_class = AuthTokenSerializer
        
        def create(self, request):
            """Use the ObtainAuthToken APIView to validate and create a token"""
            
            # Use the custom method to handle login logic
            return self.login(request)
        
        def login(self, request):
            """Handle login logic and return auth token"""
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})