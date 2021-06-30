from django.core.paginator import Paginator

from Apps.qb_app import models


def get_header():
    header = {
        'Authorization': models.Token.objects.all()[0].bearer,
        'Accept': 'application/json'
    }
    return header


def set_pagination(request, model_data):
    paginator = Paginator(model_data, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
