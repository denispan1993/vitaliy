# -*- coding: utf-8 -*-
#!/usr/bin/env python

""" spaceless middleware
MIDDLEWARE_CLASSES += ('core_utils.middleware.SpacelessMiddleware',)
"""

# Aliasing it for the sake of page size.
import re
#from django.utils.html import strip_spaces_between_tags
from django.utils.encoding import force_text

__author__ = 'AlexStarov'

#RE_MULTISPACE = re.compile(r"\s{2,}")
#RE_NEWLINE = re.compile(r"\n")


class SpacelessMiddleware(object, ):
    """ trim spaces between tags """
    def process_response(self, request, response, ):

        if 'Content-Type'.lower() in response and 'text/html' in response['Content-Type']:

            # response.content = strip_spaces_between_tags(response.content.strip(), )
            # print response.__class__.__name__
            if response.__class__.__name__ is not 'FileResponse':
                response.content = re.sub(r'>\s+<', '><', force_text(response.content, ), )
                response.content = re.sub(r'^\s+<', '<', response.content, )
            else:
                pass
                # response.content = re.sub(r'>\s+<', '><', force_text(response.streaming_content, ), )
                # response.content = re.sub(r'^\s+<', '<', response.streaming_content, )
#            response.content = RE_MULTISPACE.sub(" ", response.content, )
#            response.content = RE_NEWLINE.sub("", response.content, )

        return response
