from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import DNSRecord, UpdateLog, APIKey, Domain
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

        # Save the API key
        api_key_obj, created = APIKey.objects.get_or_create(user=self.request.user)
        api_key_obj.set_key(api_key)
        api_key_obj.is_valid = True
        api_key_obj.save()

        messages.success(self.request, 'API key saved successfully!')
        return super().form_valid(form)

class DomainListView(LoginRequiredMixin, TemplateView):
    template_name = 'dns_updater/domain_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            linode_service = LinodeAPIService(user=self.request.user)
            context['domains'] = linode_service.get_domains()
        except ValueError as e:
            messages.error(self.request, str(e))
            context['domains'] = []
        return context

class RecordListView(LoginRequiredMixin, TemplateView):
    template_name = 'dns_updater/record_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domain_id = self.kwargs.get('domain_id')
        try:
            linode_service = LinodeAPIService(user=self.request.user)
            records = linode_service.get_domain_records(domain_id)
            context['records'] = [r for r in records if r['type'] == 'A']
            context['domain_id'] = domain_id
        except ValueError as e:
            messages.error(self.request, str(e))
            context['records'] = []
        return context

class UpdateRecordView(LoginRequiredMixin, TemplateView):
    template_name = 'dns_updater/update_record.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domain_id = self.kwargs.get('domain_id')
        record_id = self.kwargs.get('record_id')
        try:
            linode_service = LinodeAPIService(user=self.request.user)
            records = linode_service.get_domain_records(domain_id)
            record = next((r for r in records if r['id'] == record_id), None)
            if record:
                context['record'] = record
                context['current_ip'] = linode_service.get_current_ip()
        except ValueError as e:
            messages.error(self.request, str(e))
        return context

    def post(self, request, *args, **kwargs):
        domain_id = kwargs.get('domain_id')
        record_id = kwargs.get('record_id')
        new_ip = request.POST.get('ip_address')
        
        try:
            linode_service = LinodeAPIService(user=request.user)
            linode_service.update_domain_record(domain_id, record_id, new_ip)
            messages.success(request, 'Record updated successfully!')
        except Exception as e:
            messages.error(request, f'Failed to update record: {str(e)}')
        
        return redirect('record-list', domain_id=domain_id)
