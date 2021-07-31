# -*- coding: utf-8 -*-

from django.views.generic.edit import FormView
from localstack_dashboard.core.forms.settings import SettingsForm
from localstack_dashboard.config.parser import get_configurations_values


class SettingsView(FormView):
    form_class = SettingsForm
    template_name = "dashboard/settings.html"
    success_url = "/settings/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config = get_configurations_values()
        context.update(config)
        return context

    def form_valid(self, form):
        hostname = self.request.POST.get("hostname")
        edge_port = self.request.POST.get("edge_port")
        region = self.request.POST.get("region")
        form.save_configurations(hostname, edge_port, region)
        return super().form_valid(form)
