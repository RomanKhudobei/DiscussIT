from django.contrib.auth.models import User

from rest_framework.generics import (
	ListAPIView, 
	RetrieveAPIView
	)

from .serializers import UserListSerializer, UserDetailSerializer


class UserListAPIView(ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserListSerializer


class UserDetailAPIView(RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserDetailSerializer