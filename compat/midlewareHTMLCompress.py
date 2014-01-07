__author__ = 'user'

# Aliasing it for the sake of page size.
from django.utils.html import strip_spaces_between_tags as short


class SpacelessMiddleware(object, ):
    def process_response(self, request, response, ):
        response_KEY = response.get('Content-Type', None, )
        if response_KEY and 'text/html' in response_KEY:  # 'text/html' in response['Content-Type']:
                                                          # response_content_type == 'text/html':
            response.content = short(response.content, )
        return response
