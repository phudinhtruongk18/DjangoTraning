from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 3
    # page_size_query_param = 'page_size'
    max_page_size = 5

    def get_paginated_response(self, data):
            return Response({
                'count': self.page.paginator.count,
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'results': data
            })
