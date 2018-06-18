from django.shortcuts import get_object_or_404

from rest_framework import serializers

from boards.models import Topic, Post

from accounts.api.serializers import UserListSerializer


class PostListSerializer(serializers.ModelSerializer):
	from .topic_serializers import TopicSerializer

	created_by = serializers.SerializerMethodField()
	created_at = serializers.SerializerMethodField()
	html_message = serializers.SerializerMethodField()
	#markdown_message = serializers.CharField(source='message')
	edit_post_url = serializers.HyperlinkedIdentityField(view_name='boards-api:post_edit')
	topic = TopicSerializer()

	class Meta:
		model = Post
		fields = ['id', 'html_message', 'message', 'created_by', 'created_at', 'edit_post_url', 'topic']
		read_only_fields = ('id', 'html_message', 'created_by', 'created_at', 'edit_post_url', 'topic')

	def get_created_by(self, obj):
		return UserListSerializer(obj.created_by, context={'request': self.context.get('request')}).data

	def get_created_at(self, obj):
		return obj.created_at.strftime("%d.%m.%Y, %H:%M")

	def get_html_message(self, obj):
		return obj.get_message_as_markdown()


class PostSerializer(serializers.ModelSerializer):
	created_by = serializers.SerializerMethodField()
	created_at = serializers.SerializerMethodField()
	html_message = serializers.SerializerMethodField()
	#markdown_message = serializers.CharField(source='message')
	edit_post_url = serializers.HyperlinkedIdentityField(view_name='boards-api:post_edit')

	class Meta:
		model = Post
		fields = ['id', 'html_message', 'message', 'created_by', 'created_at', 'edit_post_url']
		read_only_fields = ('id', 'html_message', 'created_by', 'created_at', 'edit_post_url')

	def get_created_by(self, obj):
		return UserListSerializer(obj.created_by, context={'request': self.context.get('request')}).data

	def get_created_at(self, obj):
		return obj.created_at.strftime("%d.%m.%Y, %H:%M")

	def get_html_message(self, obj):
		return obj.get_message_as_markdown()

	def create(self, validated_data):
		topic = get_object_or_404(Topic, pk=self.context.get('view').kwargs.get('pk'))
		user = self.context.get('request').user
		post = Post.objects.create(message=validated_data.get('message'), topic=topic, created_by=user)
		return post

	def to_representation(self, instance):
		return PostListSerializer(instance, context={'request': self.context.get('request')}).data

"""
class PostDetailSerializer(PostSerializer):

	class Meta:
		model = Post
		fields = PostSerializer.Meta.fields
"""