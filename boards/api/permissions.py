from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
	message = 'You are not allowed to change post, that you didn\'t write'

	def has_object_permission(self, request, view, obj):
		return obj.created_by == request.user