from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Board, Topic, Post


class PostInline(admin.TabularInline):
	model = Post
	fields = ('id', 'message', 'created_by', 'created_at', 'updated_by', 'updated_at')
	readonly_fields = ('id', 'message', 'created_by', 'created_at', 'updated_by', 'updated_at')
	show_change_link = True
	extra = 0


class TopicInline(admin.TabularInline):
	model = Topic
	fields = ('id', 'name', 'starter', 'last_updated', 'views', 'board')
	readonly_fields = ('id', 'last_updated', 'starter', 'views')
	show_change_link = True
	extra = 0


class BoardModelAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	search_fields = ('id', 'name', 'description')
	fields = ('id', 'name', 'description')
	readonly_fields = ('id',)
	#inlines = (TopicInline,)

	class Meta:
		model = Board


class TopicModelAdmin(admin.ModelAdmin):
	list_display = ('name', 'last_updated', 'get_board', 'get_starter', 'views')
	search_fields = ('id', 'name', 'board__name', 'starter__username')
	list_filter = ('last_updated', 'board')
	fields = ('id', 'name', 'starter', 'last_updated', 'views', 'board')
	readonly_fields = ('id', 'last_updated', 'starter', 'views')
	raw_id_fields = ('board',)
	#inlines = (PostInline,)

	def get_board(self, obj):
		url = reverse('admin:boards_board_change', args=[obj.board.id])
		return mark_safe('<a href="{url}">{name} ({id})</a>'.format(url=url, name=obj.board.name, id=obj.board.id))

	def get_starter(self, obj):
		url = reverse('admin:auth_user_change', args=[obj.starter.id])
		return mark_safe('<a href="{url}">{username} ({id})</a>'.format(url=url, username=obj.starter.username, id=obj.starter.id))

	class Meta:
		model = Topic

	get_board.short_description = 'board'
	get_starter.short_description = 'starter'

class PostModelAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'get_created_by', 'created_at', 'get_topic')
	search_fields = ('id', 'message', 'created_by', 'topic__name')
	list_filter = ('created_at',)
	fields = ('id', 'message', 'created_by', 'created_at', 'topic', 'updated_by', 'updated_at')
	readonly_fields = ('id', 'created_by', 'created_at', 'updated_by', 'updated_at')
	raw_id_fields = ('topic',)

	def get_topic(self, obj):
		url = reverse('admin:boards_topic_change', args=[obj.topic.id])
		return mark_safe('<a href="{url}">{name} ({id})</a>'.format(url=url, name=obj.topic.name, id=obj.topic.id))

	def get_created_by(self, obj):
		url = reverse('admin:auth_user_change', args=[obj.created_by.id])
		return mark_safe('<a href="{url}">{username} ({id})</a>'.format(url=url, username=obj.created_by.username, id=obj.created_by.id))

	get_topic.short_description = 'topic'
	get_created_by.short_description = 'created_by'

	class Meta:
		model = Post


admin.site.register(Board, BoardModelAdmin)
admin.site.register(Topic, TopicModelAdmin)
admin.site.register(Post, PostModelAdmin)

admin.site.site_header = 'DiscussIT Administration'