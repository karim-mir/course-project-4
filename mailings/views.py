from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from mailings.models import Mailing
from newsletters.models import Newsletter
from mailings.utils import send_mail
@login_required
def start_mailing(request, pk):
    # Проверка прав доступа
    send_mailing(pk)
    return HttpResponseRedirect(reverse('mailings:mailings_detail', args=[pk]))
def mailings_view(request):
    messages = Newsletter.objects.all()
    return render(request, 'mailings/mailings_page.html', {'messages': messages})
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailings_list.html"
    context_object_name = "mailings"
class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailings/mailings_detail.html"
class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = "mailings/mailings_form.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("mailings:mailings_list")
class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    template_name = "mailings/mailings_form.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("mailings:mailings_list")
class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailings_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailings_list")
