from django.shortcuts import get_object_or_404
from django.shortcuts import render

from rest_framework.generics import (
	ListAPIView, 
	RetrieveAPIView, 
	UpdateAPIView, 
	RetrieveUpdateAPIView, 
	CreateAPIView
	)

from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from boards.models import Board, Topic, Post

from .serializers.board_serializers import BoardSerializer

from .serializers.topic_serializers import (
	TopicSerializer,
	TopicExtendedSerializer, 
	TopicCreateSerializer
	)

from .serializers.post_serializers import PostSerializer, PostListSerializer

from .pagination import (
	GeneralPageNumberPagination,
	ListPageNumberPagination
	)

from .permissions import IsOwner

from accounts.api.serializers import UserListSerializer, UserDetailSerializer


class BoardListAPIView(ListAPIView):
	queryset = Board.objects.all()
	serializer_class = BoardSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['id', 'name', 'description']


class BoardDetailAPIView(RetrieveAPIView):
	queryset = Board.objects.all()
	serializer_class = BoardSerializer
	lookup_url_kwarg = 'pk'


class BoardTopicsListAPIView(ListAPIView):
	serializer_class = TopicSerializer
	pagination_class = GeneralPageNumberPagination
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['id', 'name', 'starter__username']

	def get_queryset(self):
		board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
		return Topic.objects.filter(board=board).order_by('-last_updated')


class TopicCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = TopicCreateSerializer
	permission_classes = [IsAuthenticated]


class TopicListAPIView(ListAPIView):
	queryset = Topic.objects.order_by('-last_updated')
	serializer_class = TopicExtendedSerializer
	pagination_class = ListPageNumberPagination
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['id', 'name', 'starter__username']
	ordering_fields = ['id', 'name', 'views']


class TopicDetailAPIView(RetrieveAPIView):
	queryset = Topic.objects.all()
	serializer_class = TopicExtendedSerializer


class TopicPostsListAPIView(ListAPIView):
	serializer_class = PostSerializer
	pagination_class = GeneralPageNumberPagination

	def get_queryset(self):
		topic = get_object_or_404(Topic, pk=self.kwargs.get('pk'))
		return Post.objects.filter(topic=topic).order_by('created_at')


class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [IsAuthenticated]


class PostListAPIView(ListAPIView):
	queryset = Post.objects.order_by('created_at')
	serializer_class = PostListSerializer
	pagination_class = ListPageNumberPagination
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['topic__name', 'created_by__username', 'message']


class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer


class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [IsOwner]
"""
	def get_queryset(self):
		queryset = super().get_queryset().filter(created_by=self.request.user)
		return queryset
"""


def api_docs(request):
	return render(request, 'boards/api/api_docs.html')

def api_boards(request):
	return render(request, 'boards/api/api_boards.html')

def api_topics(request):
	return render(request, 'boards/api/api_topics.html')

def api_posts(request):
	return render(request, 'boards/api/api_posts.html')