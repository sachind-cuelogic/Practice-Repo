import json
from io import BytesIO


class FilterRequestMiddleware(object):
    """
    Middleware which process request and merge inner dictionary request_data
    into outer dictionary request.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):

        data = getattr(request, '_body', request.body)
        if data:
            datas = json.loads(data)
            if 'request_data' in datas:
                request_data = datas['request_data']
                datas.update(request_data)
                del datas['request_data']
                
            request_body = json.dumps(datas)
            request._body = request_body

            request._stream = BytesIO(request_body)
    
        return None
