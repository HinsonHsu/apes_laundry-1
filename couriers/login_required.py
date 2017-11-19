# -*- coding: utf-8 -*-
from urlparse import urlparse
from django.shortcuts import resolve_url

LOGIN_URL = "/courier/login"
def login_required_courier(function=None,redirect_field_name=LOGIN_URL):
    def _decorate(view_fun):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated() and request.user.username.split('_')[0] == 'courier':
                return view_fun(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(LOGIN_URL)
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    if function is None:
        return _decorate
    else:
        return _decorate(function)