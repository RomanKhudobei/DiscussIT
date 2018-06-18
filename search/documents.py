from django_elasticsearch_dsl import DocType, Index, fields

from boards.models import Topic


topics = Index('topics')

@topics.doc_type
class TopicDocument(DocType):
	id = fields.IntegerField()
	name = fields.StringField()
	last_updated = fields.DateField()
	views = fields.IntegerField()

	board = fields.ObjectField(
		properties={
			'id': fields.IntegerField(),
			'name': fields.StringField(),
			'description': fields.StringField()
		}
	)

	class Meta:
		model = Topic
		#fields = ('id', 'name', 'last_updated', 'views')