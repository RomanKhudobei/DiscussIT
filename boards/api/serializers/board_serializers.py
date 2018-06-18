from django.core.paginator import Paginator
from django.urls import reverse

from rest_framework import serializers

from boards.models import Board


class BoardSerializer(serializers.ModelSerializer):
	posts_count = serializers.SerializerMethodField()
	topics_count = serializers.SerializerMethodField()
	last_post_datetime = serializers.SerializerMethodField()
	topics_url = serializers.HyperlinkedIdentityField(view_name='boards-api:board_topics')

	class Meta:
		model = Board
		fields = ['id', 'name', 'description', 'posts_count', 'topics_count', 'last_post_datetime', 'topics_url']

	def get_posts_count(self, obj):
		return obj.get_posts_count()

	def get_topics_count(self, obj):
		return obj.topics.count()

	def get_last_post_datetime(self, obj):
		last_post = obj.get_last_post()
		if last_post:
			return obj.get_last_post().created_at.strftime("%d.%m.%Y, %H:%M")

"""
class BoardListSerializer(BoardSerializer):
	detail_url = serializers.HyperlinkedIdentityField(view_name='boards-api:board_detail')

	class Meta:
		model = Board
		fields = BoardSerializer.Meta.fields + ['detail_url']


class BoardDetailSerializer(BoardSerializer):
	from .topic_serializers import TopicListSerializer

	topics = serializers.HyperlinkedIdentityField(view_name='boards-api:board_topics')

	class Meta:
		model = Board
		fields = BoardSerializer.Meta.fields + ['topics']
"""

"""
class BoardDetailSerializer(BoardSerializer):
	#from .topic_serializers import TopicListSerializer

	topics = serializers.SerializerMethodField(method_name='get_paginated_topics')

	class Meta:
		model = Board
		fields = BoardSerializer.Meta.fields + ['topics']

	def get_paginated_topics(self, obj):
		from .topic_serializers import TopicListSerializer

		request = self.context.get('request')
		page_size = request.GET.get('page_size') or 20
		page_number = request.GET.get('page') or 1

		paginator = Paginator(obj.topics.order_by('last_updated'), page_size)

		if page_number == 'all':
			return TopicListSerializer(obj.topics.order_by('last_updated'), many=True, context={'request': request}).data		# maybe change to order through GET param

		try:
			page_number = int(page_number)
		except:
			page_number = 1

		try:
			page = paginator.page(page_number)
		except:
			page = paginator.page(paginator.num_pages)

		data = {}

		data['total_pages'] = paginator.num_pages
		data['current_page'] = page_number
		data['total_items'] = paginator.count

		restrict = ('page',)

		if page.has_next():
			data['next'] = reverse('boards-api:board_detail', kwargs={'pk': obj.pk}) + f'?page={page_number+1}' + ''.join([f'&{param}={value}' for param, value in request.GET.items() if param not in restrict])
		else:
			data['next'] = None

		if page.has_previous():
			data['previous'] = reverse('boards-api:board_detail', kwargs={'pk': obj.pk}) + f'?page={page_number-1}' + ''.join([f'&{param}={value}' for param, value in request.GET.items() if param not in restrict])
		else:
			data['previous'] = None

		data['topics'] = TopicListSerializer(page.object_list, many=True, context={'request': request}).data

		return data
"""

class BoardTinySerializer(serializers.ModelSerializer):
	topics_url = serializers.HyperlinkedIdentityField(view_name='boards-api:board_topics')

	class Meta:
		model = Board
		fields = ('id', 'name', 'topics_url')
