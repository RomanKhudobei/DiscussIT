from django.conf.urls import url

from .views import (
	UserListAPIView,
	UserDetailAPIView
	)


urlpatterns = [
	url(r'^users/$', UserListAPIView.as_view(), name='users_list'),
	url(r'^users/(?P<pk>\d+)/$', UserDetailAPIView.as_view(), name='user_detail')
]