from django.conf.urls import url

from boards.api import views


urlpatterns = [
    url(r'^docs/$', views.api_docs, name='docs'),
    url(r'^docs/boards/$', views.api_boards, name='docs_boards'),
    url(r'^docs/topics/$', views.api_topics, name='docs_topics'),
    url(r'^docs/posts/$', views.api_posts, name='docs_posts'),

    url(r'^boards/$', views.BoardListAPIView.as_view(), name='boards_list'),
    url(r'^boards/(?P<pk>\d+)/$', views.BoardDetailAPIView.as_view(), name='board_detail'),
    url(r'^boards/(?P<pk>\d+)/topics/$', views.BoardTopicsListAPIView.as_view(), name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/topics/new/$', views.TopicCreateAPIView.as_view(), name='topic_create'),


    url(r'^topics/(?P<pk>\d+)/reply/$', views.PostCreateAPIView.as_view(), name='topic_reply'),
    url(r'^topics/$', views.TopicListAPIView.as_view(), name='topics_list'),
    url(r'^topics/(?P<pk>\d+)/$', views.TopicDetailAPIView.as_view(), name='topic_detail'),
    url(r'^topics/(?P<pk>\d+)/posts/$', views.TopicPostsListAPIView.as_view(), name='topic_posts'),

    url(r'^posts/$', views.PostListAPIView.as_view(), name='posts_list'),
    url(r'^posts/(?P<pk>\d+)/$', views.PostDetailAPIView.as_view(), name='post_detail'),
    url(r'^posts/(?P<pk>\d+)/edit/$', views.PostUpdateAPIView.as_view(), name='post_edit')
]