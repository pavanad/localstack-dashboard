# -*- coding: utf-8 -*-

import requests
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from localstack_dashboard.config.parser import get_endpoint_url


class LocalStackServiceMixin:
    """
    Redirect to redirect_url if the localstack service is not working.
    """

    redirect_url = None

    def get_redirect_url(self):
        """
        Override this method to override the redirect_url attribute.
        """
        redirect_url = self.redirect_url
        if not redirect_url:
            raise ImproperlyConfigured(
                "{0} is missing the redirect_url attribute. Define {0}.redirect_url or override "
                "{0}.get_redirect_url().".format(self.__class__.__name__)
            )
        return str(redirect_url)

    def dispatch(self, request, *args, **kwargs):
        try:
            endpoint_url = get_endpoint_url()
            requests.get(f"{endpoint_url}/health")
        except Exception:
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)
