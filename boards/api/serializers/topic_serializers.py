from rest_framework import serializers

from boards.models import Board, Topic, Post

from accounts.api.serializers import UserListSerializer
from .board_serializers import BoardSerializer, BoardTinySerializer


class TopicSerializer(serializers.ModelSerializer):
	#title = serializers.SerializerMethodField(source='name')
	starter = UserListSerializer()
	last_updated = serializers.SerializerMethodField()
	posts_url = serializers.HyperlinkedIdentityField(view_name='boards-api:topic_posts')
	reply_topic = serializers.HyperlinkedIdentityField(view_name='boards-api:topic_reply')

	class Meta:
		model = Topic
		fields = ['id', 'name', 'starter', 'views', 'last_updated', 'posts_url', 'reply_topic']
		read_only_fields = ('id', 'starter', 'views', 'last_updated', 'posts_url', 'reply_topic')

	def get_title(self, obj):
		return obj.name

	#def get_main_post(self, obj):
	#	return PostListSerializer(obj.get_main_post()).data

	def get_last_updated(self, obj):
		return obj.last_updated.strftime("%d.%m.%Y, %H:%M")

"""
class TopicListSerializer(TopicSerializer):
	detail_url = serializers.HyperlinkedIdentityField(view_name='boards-api:topic_detail')

	class Meta:
		model = Topic
		fields = TopicSerializer.Meta.fields + ['detail_url']
"""

class TopicExtendedSerializer(TopicSerializer):
	board = BoardSerializer()

	class Meta:
		model = Topic
		fields = TopicSerializer.Meta.fields + ['board']

"""
class TopicDetailSerializer(TopicSerializer):
	from .post_serializers import PostDetailSerializer
	from .board_serializers import BoardListSerializer

	posts = PostDetailSerializer(many=True)

	class Meta:
		model = Topic
		fields = TopicSerializer.Meta.fields + ['posts']
"""

class TopicCreateSerializer(serializers.Serializer):
	id = serializers.ModelField(model_field=Topic()._meta.get_field('id'), read_only=True)
	title = serializers.CharField(max_length=255, write_only=True)
	message = serializers.CharField(max_length=4000, write_only=True)	# write_only=True allows me to add non-model field to the serializer
	board = serializers.SerializerMethodField()
	starter = serializers.SerializerMethodField()

	def get_board(self, obj):
		return BoardTinySerializer(obj.board, context={'request': self.context.get('request')}).data

	def get_starter(self, obj):
		return UserListSerializer(obj.starter, context={'request': self.context.get('request')}).data

	def create(self, validated_data):
		board = Board.objects.get(pk=self.context.get('view').kwargs.get('pk'))
		user = self.context.get('request').user

		message = validated_data.pop('message')

		topic = Topic.objects.create(name=validated_data.get('title'), board=board, starter=user)

		Post.objects.create(message=message, topic=topic, created_by=user)

		return topic

	def to_representation(self, instance):
		return TopicExtendedSerializer(instance, context={'request': self.context.get('request')}).data