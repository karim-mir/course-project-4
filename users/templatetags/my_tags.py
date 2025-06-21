from django import template

from newsletters.models import Mailing

register = template.Library()


@register.simple_tag
def get_mailings():
    return Mailing.objects.all()
