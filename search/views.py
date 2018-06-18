from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.db.models import Count

#from search.documents import TopicDocument
from boards.models import Topic


def search(request):
	q = request.GET.get('q')
	is_paginated = False
	paginator = None

	if q:
		#topics = TopicDocument.search().query('match', name=q)
		topics = Topic.objects.filter(name__icontains=q).annotate(replies=Count('posts') - 1)
		if topics.count() > 20 :
			is_paginated = True
			page_number = request.GET.get('page',)
			paginator = Paginator(topics, 20)

			try:
				topics = paginator.page(page_number)

			except PageNotAnInteger:
				topics = paginator.page(1)

			except EmptyPage:
				topics = paginator.page(paginator.num_pages)
	else:
		topics = []

	return render(request, 'search/search.html', {'topics': topics, 'page_obj': topics, 'is_paginated': is_paginated, 'paginator': paginator})

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