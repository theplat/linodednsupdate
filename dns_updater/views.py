from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import DNSRecord, Domain
from .services import LinodeAPIService
from django import forms

# Create your views here.

class APIKeyForm(forms.Form):
    api_key = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Linode API Key'
    )

class APIKeyView(LoginRequiredMixin, FormView):
    template_name = 'dns_updater/api_key.html'
    form_class = APIKeyForm
    success_url = reverse_lazy('domain-list')

    def form_valid(self, form):
        api_key = form.cleaned_data['api_key']
        linode_service = LinodeAPIService()
        
        if not linode_service.test_api_key(api_key):
            messages.error(self.request, 'Invalid API key. Please try again.')
            return self.form_invalid(form)

        # Store API key in session
        self.request.session['api_key'] = api_key
        messages.success(self.request, 'API key saved successfully!')
        return super().form_valid(form)

class DomainListView(LoginRequiredMixin, TemplateView):
    template_name = 'dns_updater/domain_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_key = self.request.session.get('api_key')
        
        if not api_key:
            messages.error(self.request, 'Please enter your API key first.')
            return context

        try:
            linode_service = LinodeAPIService(api_key=api_key)
            context['domains'] = linode_service.get_domains()
        except Exception as e:
            messages.error(self.request, str(e))
            context['domains'] = []
        return context

class RecordListView(LoginRequiredMixin, TemplateView):
    template_name = 'dns_updater/record_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_key = self.request.session.get('api_key')
        domain_id = self.kwargs.get('domain_id')

        if not api_key:
            messages.error(self.request, 'Please enter your API key first.')
            return context

        try:
            linode_service = LinodeAPIService(api_key=api_key)
            records = linode_service.get_domain_records(domain_id)
            context['records'] = [r for r in records if r['type'] == 'A']
            context['domain_id'] = domain_id
        except Exception as e:
            messages.error(self.request, str(e))
            context['records'] = []
        return context

class UpdateRecordView(LoginRequiredMixin, TemplateView):
    template_name = 'dns_updater/update_record.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_key = self.request.session.get('api_key')
        domain_id = self.kwargs.get('domain_id')
        record_id = self.kwargs.get('record_id')

        if not api_key:
            messages.error(self.request, 'Please enter your API key first.')
            return context

        try:
            linode_service = LinodeAPIService(api_key=api_key)
            records = linode_service.get_domain_records(domain_id)
            record = next((r for r in records if r['id'] == record_id), None)
            if record:
                context['record'] = record
                context['current_ip'] = linode_service.get_current_ip()
                context['domain_id'] = domain_id
        except Exception as e:
            messages.error(self.request, str(e))
        return context

    def post(self, request, *args, **kwargs):
        api_key = request.session.get('api_key')
        domain_id = kwargs.get('domain_id')
        record_id = kwargs.get('record_id')
        new_ip = request.POST.get('ip_address')
        
        if not api_key:
            messages.error(request, 'Please enter your API key first.')
            return redirect('api-key')

        try:
            linode_service = LinodeAPIService(api_key=api_key)
            linode_service.update_domain_record(domain_id, record_id, new_ip)
            messages.success(request, 'Record updated successfully!')
        except Exception as e:
            messages.error(request, f'Failed to update record: {str(e)}')
        
        return redirect('record-list', domain_id=domain_id)
