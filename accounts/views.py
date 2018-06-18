from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import UpdateView, DetailView, ListView
from django.urls import reverse

from .forms import SignUpForm
from boards.models import Post


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			auth_login(request, user)
			messages.success(request, 'Account created succesfully!')
			return redirect('home')
	else:		
		form = SignUpForm()
	return render(request, 'accounts/signup.html', {'form': form})


class CustomLoginView(LoginView):
	template_name = 'accounts/login.html'

	def get_success_url(self):
		messages.success(self.request, f'Welcome, <strong>{self.request.user}</strong>!')
		return super().get_success_url()


class CustomLogoutView(LogoutView):

	def get_next_page(self):
		messages.success(self.request, 'Logged out successfully!')
		return super().get_next_page()


class UserUpdateView(LoginRequiredMixin, UpdateView):
	model = User
	fields = ('username', 'email')
	template_name = 'accounts/edit_account.html'

	def dispatch(self, request, *args, **kwargs):
		self.user_id = int(self.kwargs['user_id'])

		if self.user_id != self.request.user.id:
			return redirect(reverse('user_info', kwargs={'user_id': self.user_id}))

		if request.method.lower() in self.http_method_names:
		    handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
		else:
		    handler = self.http_method_not_allowed
		return handler(request, *args, **kwargs)

	def get_object(self):
		return self.request.user

	def get_success_url(self):
		messages.success(self.request, 'Account updated succesfully!')
		return reverse('user_info', kwargs={'user_id': self.user_id})


class UserInfoView(DetailView):
	model = User
	context_object_name = 'user'
	template_name = 'accounts/user_info.html'
	lastest_posts_quantity = 5

	def get_object(self):
		return User.objects.get(pk=self.kwargs['user_id'])

	def get_context_data(self, **kwargs):
		user_id = int(self.kwargs['user_id'])
		kwargs['last_posts'] = self.get_last_posts()
		kwargs['owner'] = user_id == self.request.user.id
		kwargs['user_id'] = user_id
		return super().get_context_data(**kwargs)

	def get_last_posts(self):
		return Post.objects.filter(created_by=self.get_object()).order_by('-created_at')[:self.lastest_posts_quantity]


class UserPostsView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'accounts/user_posts.html'
	paginate_by = 20

	def get_user(self):
		return User.objects.get(pk=self.kwargs['user_id'])

	def get_queryset(self):
		return Post.objects.filter(created_by=self.get_user()).order_by('-created_at')

	def get_context_data(self, **kwargs):
		user_id = int(self.kwargs['user_id'])
		kwargs['owner'] = user_id == self.request.user.id
		kwargs['user_id'] = user_id
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