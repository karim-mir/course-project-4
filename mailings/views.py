from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from mailings.forms import MailingRecipientForm
from mailings.models import Mailing, MailingRecipient
from mailings.utils import send_mailing
from newsletters.models import Newsletter

from django.db.models import Count, Q

# Получение статистики по пользователю
@login_required
def recipients_stats_view(request):
    recipients_stats = MailingRecipient.objects.annotate(
        total_messages=Count("messages_sent"),
        success_count=Count("messages_sent", filter=Q(messages_sent__status="success")),
        failed_count=Count("messages_sent", filter=Q(messages_sent__status="failed"))
    )
    return render(request, "mailings/recipients_stats.html", {"recipients_stats": recipients_stats})


class MailingAccessMixin:
    def get_queryset(self):
        user = self.request.user
        if user.role == "manager":
            return self.model.objects.all()
        return self.model.objects.filter(owner=user)


class MailingOwnerPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.role != "manager" and obj.owner != request.user:
            raise PermissionDenied("Вы не можете удалять чужие рассылки")
        return super().dispatch(request, *args, **kwargs)


@login_required
def disable_mailing(request, pk):
    """Отключение рассылки"""
    mailing = get_object_or_404(Mailing, pk=pk)
    if not request.user.has_perm("mailings.can_disable_mailing"):
        raise PermissionDenied("У вас нет прав отключать рассылки")
    mailing.is_active = False
    mailing.save()
    return redirect("mailings:mailings_list")


@login_required
def start_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    user = request.user
    if user.role != "manager" and mailing.owner != user:
        raise PermissionDenied("У вас нет прав запускать эту рассылку")
    send_mailing(pk)
    return HttpResponseRedirect(reverse("mailings:mailings_detail", args=[pk]))


def mailings_view(request):
    messages = Newsletter.objects.all()
    return render(request, "mailings/mailings_page.html", {"messages": messages})


class MailingListView(LoginRequiredMixin, MailingAccessMixin, ListView):
    model = Mailing
    template_name = "mailings/mailings_list.html"
    context_object_name = "mailings"


class MailingDetailView(LoginRequiredMixin, MailingAccessMixin, DetailView):
    model = Mailing
    template_name = "mailings/mailings_detail.html"


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = "mailings/mailings_form.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("mailings:mailings_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, MailingAccessMixin, MailingOwnerPermissionMixin, UpdateView):
    model = Mailing
    template_name = "mailings/mailings_form.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("mailings:mailings_list")


class MailingDeleteView(LoginRequiredMixin, MailingAccessMixin, MailingOwnerPermissionMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailings_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailings_list")


class MailingRecipientListView(LoginRequiredMixin, ListView):
    model = MailingRecipient
    template_name = "mailings/recipients_list.html"
    context_object_name = "recipients"


class MailingRecipientDetailView(LoginRequiredMixin, DetailView):
    model = MailingRecipient
    template_name = "mailings/recipients_detail.html"

    def get_queryset(self):
        return get_users_from_cache()


class MailingRecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    template_name = "mailings/recipients_form.html"
    form_class = MailingRecipientForm
    success_url = reverse_lazy("mailings:recipients_list")


class MailingRecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingRecipient
    template_name = "mailings/recipients_form.html"
    form_class = MailingRecipientForm
    success_url = reverse_lazy("mailings:recipients_list")


class MailingRecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    template_name = "mailings/recipients_confirm_delete.html"
    success_url = reverse_lazy("mailings:recipients_list")
