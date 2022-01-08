from django.core.exceptions import PermissionDenied


def validate_permissions(*decs):
    def wrap(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return wrap


def dashboard_admin_request(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap