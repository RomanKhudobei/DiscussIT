from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User

from ..views import PostListView
from ..models import Board, Topic, Post


class TopicPostsTests(TestCase):

	def setUp(self):
		board = Board.objects.create(name='Django', description='Django board')
		user = User.objects.create_user(username='john', email='john@doe.com', password='123456test')
		topic = Topic.objects.create(name='Hello, world!', board=board, starter=user)

		Post.objects.create(message='Some test post message', topic=topic, created_by=user)

		url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve(reverse('topic_posts', kwargs={'pk': 1, 'topic_pk': 1}))
		self.assertEquals(view.func.view_class, PostListView)