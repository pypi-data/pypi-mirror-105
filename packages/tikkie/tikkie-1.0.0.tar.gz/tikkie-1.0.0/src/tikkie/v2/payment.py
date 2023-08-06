from datetime import datetime
from typing import Optional

from tikkie import session as s
from tikkie.v2.models import GetAllPaymentsResponse, Payment


def get(payment_request_token: str, payment_token: str) -> Payment:
    """
    Retrieves details of a specific payment made against a specific payment request based on the value of the tokens.
    The application must have payment request permission to complete this request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#operation/getPayment

    :param payment_request_token: Token identifying the payment request.
    :param payment_token: Token identifying one payment of a payment request
    """
    response = s().get(f"paymentrequests/{payment_request_token}/payments/{payment_token}")
    return Payment.parse_raw(response.content)


def get_all(
    *,
    payment_request_token: str,
    page_size: int,
    page_number: int,
    from_date_time: Optional[datetime] = None,
    to_date_time: Optional[datetime] = None,
) -> GetAllPaymentsResponse:
    """
    Retrieves payments made against a specific payment request based on the parameters provided.
    The application must have payment request permission to complete this request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#tag/Payment

    :param payment_request_token: Token identifying the payment request.
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

    response = s().get(f"paymentrequests/{payment_request_token}/payments", params=params)
    breakpoint()
    return GetAllPaymentsResponse.parse_raw(response.content)
