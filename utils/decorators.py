from functools import wraps
from rest_framework import decorators, status
from rest_framework.response import Response


def required_params(request_attr='query_params', params=None):
    """
    当我们使用@required_params(params=['some_params])的时候
    这个required_params 函数应该需要返回一个decorator 函数，
    这个decorator 函数的参数就是被@required_params 包裹起来的函数view_func
    """

    # 从效果上来说，参数中写params=[] 很多时候也没有太大问题
    # 但是从好的编程习惯上来说，函数的参数列表中的值不能是一个mutable 的参数
    if params is None:
        params = []
    
    def decorator(view_func):
        """
        decorator 函数通过wraps 来将view_func 里的参数解析出来传递给_wrapped_view
        这里的instance 参数其实就是在view_func 里的self
        """
        @wraps(view_func)
        def _warpped_view(instance, request, *args, **kwargs):
            data = getattr(request, request_attr)
            missing_params = [
                param
                for param in params
                if param not in data
            ]
            if missing_params:
                params_str = ','.join(missing_params)
                return Response({
                    'message': u'missing {} in request'.format(params_str),
                    'success': False,
                }, status=status.HTTP_400_BAD_REQUEST)
            # 做完检测之后，再去调用被@required_params 包裹起来的view_func
            return view_func(instance, request, *args, **kwargs)
        return _warpped_view
    return decorator
