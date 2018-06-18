import requests
import json
import sys

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
#from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

from .models import Board, Topic, Post
from .forms import NewTopicForm, NewPostForm


class BoardListView(ListView):
	model = Board
	context_object_name = 'boards'
	template_name = 'boards/home.html'


class TopicListView(ListView):
	model = Topic
	context_object_name = 'topics'
	template_name = 'boards/board_topics.html'
	paginate_by = 20

	def get_context_data(self, **kwargs):
		kwargs['board'] = self.board
		#kwargs['user_tz'] = self.get_timezone() or timezone.get_default_timezone()
		return super().get_context_data(**kwargs)

	def paginate_queryset(self, queryset, page_size):
		paginator = self.get_paginator(
			queryset, page_size, orphans=self.get_paginate_orphans(),
			allow_empty_first_page=self.get_allow_empty())
		page_kwarg = self.page_kwarg
		page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1

		try:
			page_number = int(page)
		except:
			page_number = 1

		try:
			page = paginator.page(page_number)
		except:
			page = paginator.page(paginator.num_pages)

		return (paginator, page, page.object_list, page.has_other_pages())

	def get_queryset(self):
		self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
		query = self.request.GET.get('q')

		if query:
			queryset = self.board.topics.filter(name__icontains=query)
		else:
			queryset = self.board.topics

		queryset = queryset.order_by('-last_updated').annotate(replies=Count('posts') - 1)
		return queryset

	def get_timezone(self):
		user_ip = self.request.META.get('REMOTE_ADDR')

		if user_ip == '127.0.0.1':	# temporarily, while developing
			return 'Europe/Kiev'

		data = requests.get(f'https://timezoneapi.io/api/ip/?ip={user_ip}')
		data = json.loads(data.text)

		if data['meta']['code'] == '200':
			return data.get('data').get('timezone').get('id')

"""		OR this instead TopicListView
def board_topics(request, pk):
	board = get_object_or_404(Board, pk=pk)
	topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
	page_number = request.GET.get('page', 1)

	paginator = Paginator(topics, 20)

	try:
		topics = paginator.page(page_number)

	except PageNotAnInteger:
		topics = paginator.page(1)

	except EmptyPage:
		topics = paginator.page(paginator.num_pages)

	return render(request, 'boards/board_topics.html', {'board': board, 'topics': topics})
"""

@login_required
def new_topic(request, pk):
	board = get_object_or_404(Board, pk=pk)

	if request.method == 'POST':
		form = NewTopicForm(request.POST)

		if form.is_valid():
			topic = form.save(commit=False)

			topic.board = board
			topic.starter = request.user
			topic.save()

			Post.objects.create(message=form.cleaned_data.get('message'), topic=topic, created_by=request.user)
			messages.success(request, '<strong>Success!</strong> New topic created!')
			return redirect('topic_posts', pk=board.pk, topic_pk=topic.pk)
	else:
		form = NewTopicForm()

	return render(request, 'boards/new_topic.html', {'board': board, 'form': form})


class PostListView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'boards/topic_posts.html'
	paginate_by = 20

	def get_context_data(self, **kwargs):
		session_key = f'viewed_topic_{self.topic.pk}'
		
		if not self.request.session.get(session_key, False):
			self.topic.views += 1
			self.topic.save()
			self.request.session[session_key] = True

		kwargs['topic'] = self.topic
		# initial topic post. In order to fix it as first and paginate rest
		kwargs['main_post'] = self.main_post
		return super().get_context_data(**kwargs)

	def paginate_queryset(self, queryset, page_size):
		paginator = self.get_paginator(
			queryset, page_size, orphans=self.get_paginate_orphans(),
			allow_empty_first_page=self.get_allow_empty())
		page_kwarg = self.page_kwarg
		page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1

		try:
			page_number = int(page)
		except:
			page_number = 1

		try:
			page = paginator.page(page_number)
		except:
			page = paginator.page(paginator.num_pages)

		return (paginator, page, page.object_list, page.has_other_pages())

	def get_queryset(self):
		self.topic = get_object_or_404(Topic, pk=self.kwargs.get('topic_pk'))
		queryset = self.topic.posts.order_by('created_at')[1:]	# exclude main_post to avoid duplication
		self.main_post = self.topic.get_main_post()
		return queryset

""" OR this instead PostListView
def topic_posts(request, pk, topic_pk):
	topic = get_object_or_404(Topic, pk=topic_pk)
	topic.views += 1
	topic.save()
	return render(request, 'boards/topic_posts.html', {'topic': topic})
"""

@login_required
def reply_topic(request, pk, topic_pk):
	topic = get_object_or_404(Topic, pk=topic_pk)

	if request.method == 'POST':
		form = NewPostForm(request.POST)

		if form.is_valid():
			post = form.save(commit=False)

			post.topic = topic
			post.created_by = request.user
			post.save()

			topic.last_updated = timezone.now()
			topic.save()
			messages.success(request, '<strong>Success!</strong> New post added!')
			return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
	else:
		form = NewPostForm()

	return render(request, 'boards/reply_topic.html', {'form': form, 'topic': topic})


#@method_decorator(login_required, name='dispatch')
class PostUpdateView(LoginRequiredMixin, UpdateView):
	model = Post
	template_name = 'boards/edit_post.html'
	pk_url_kwarg = 'post_pk'
	context_object_name = 'post'
	form_class = NewPostForm

	def from_valid(self, form):
		post = form.save(commit=False)
		post.updated_by = self.request.user
		post.updated_at = timezone.now()
		post.save()
		return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(created_by=self.request.user)

	def get_success_url(self):
		messages.success(self.request, 'Post edited successfully!')
		success_url = self.request.GET.get('next')
		if success_url:
			return success_url
		return reverse('home')