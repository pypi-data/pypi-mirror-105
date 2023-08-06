from datetime import date, datetime
from typing import Optional

from tikkie import session as s
from tikkie._util import format_date
from tikkie.v2.models import GetAllPaymentRequestsResponse, PaymentRequest


def create(
    *,
    description: str,
    amount_in_cents: Optional[int] = None,
    expiry_date: Optional[date] = None,
    reference_id: Optional[str] = None,
) -> PaymentRequest:
    """
    https://developer.abnamro.com/api-products/tikkie/reference-documentation#tag/Payment-request

    :param description: Description of the payment request, which the payer or payers see.
    :param amount_in_cents: Amount in cents of the payment request (euros). If this value is not specified, an open payment request is created.
    :param expiry_date: Date after the payment request expires and cannot be paid
    :param reference_id: ID for the reference of the API consumer.
    """
    payload = {"description": description}
    if amount_in_cents is not None:
        payload["amountInCents"] = amount_in_cents
    if expiry_date is not None:
        payload["expiryDate"] = format_date(expiry_date)
    if reference_id is not None:
        payload["referenceId"] = reference_id

    response = s().post("paymentrequests", json=payload)
    return PaymentRequest.parse_raw(response.content)


def get(payment_request_token: str) -> PaymentRequest:
    """
    https://developer.abnamro.com/api-products/tikkie/reference-documentation#operation/createPaymentRequest
    """
    response = s().get(f"paymentrequests/{payment_request_token}")
    return PaymentRequest.parse_raw(response.content)


def get_all(
    *,
    page_size: int,
    page_number: int,
    from_date_time: Optional[datetime] = None,
    to_date_time: Optional[datetime] = None,
) -> GetAllPaymentRequestsResponse:
    """
    https://developer.abnamro.com/api-products/tikkie/reference-documentation#operation/getPaymentRequest

    :param page_size: Number of the page to be returned.
    :param page_number: Number of items on a page.
    :param from_date_time:The time you start searching for items. Refers to the creation date for payment requests and iDeal QRs, and refers to the bundle date for transaction bundles.
    :param to_date_time: The time you stop searching for items. Refers to the creation date for payment requests and iDeal QRs, and refers to the bundle date for transaction bundles.
    """
    params = {
        "pageSize": page_size,
        "pageNumber": page_number,
    }
    if from_date_time is not None:
        params["fromDateTime"] = from_date_time
    if to_date_time is not None:
        params["toDateTime"] = to_date_time

    response = s().get("paymentrequests", params=params)
    return GetAllPaymentRequestsResponse.parse_raw(response.content)
