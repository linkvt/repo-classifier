from base64 import b64encode

from django import template

register = template.Library()


@register.filter
def data_uri(string: str, mime: str = None):
    encoded_data = b64encode(string.encode())
    base64_string = encoded_data.decode('utf-8')

    mime = mime + ';' if mime else ';'
    return 'data:%sbase64,%s' % (mime, base64_string)
