from urllib.parse import urljoin
import requests
import json

from django.conf import settings

from dnoticias_services.utils.request import get_headers
from .base import BasePaymentRequest


class GetUserOrderDatatable(BasePaymentRequest):
    def __call__(self, request, user_id, api_key=None):
        _api_key = api_key or self.api_key

        request = json.dumps(request.POST)

        response = requests.post(
            settings.ORDER_USER_DATATABLE_LIST_API_URL.format(user_id),
            headers=get_headers(_api_key),
            json=request,
        )

        response.raise_for_status()

        return response

get_user_order_datatable = GetUserOrderDatatable()


__all__ = ("get_user_order_datatable")
