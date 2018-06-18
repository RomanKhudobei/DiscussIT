from django.contrib.auth.models import User

from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
	detail_url = serializers.HyperlinkedIdentityField(view_name='accounts-api:user_detail')

	class Meta:
		model = User
		fields = ('id', 'username', 'detail_url')
		read_only_fields = ('id', 'username', 'detail_url')


class UserDetailSerializer(serializers.ModelSerializer):	# add user_posts, posts_count
	date_joined = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'is_staff')

	def get_date_joined(self, obj):
		return obj.date_joined.strftime("%d.%m.%Y, %H:%M")