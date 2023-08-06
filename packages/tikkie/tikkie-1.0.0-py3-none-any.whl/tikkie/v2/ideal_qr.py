from datetime import datetime
from typing import Optional

from tikkie import session as s
from tikkie._util import format_datetime
from tikkie.v2.models import IdealQr, GetAllIdealQrResponse, GetAllIdealQrPaymentsResponse, IdealQrPayment


def create_non_changeable(
    *,
    description: str,
    expiry_date_time: datetime,
    amount_in_cents: int,
    reference_id: str = None,
    single_pay: bool = None,
    image_size: int = None,
) -> IdealQr:
    """
    https://developer.abnamro.com/api-products/tikkie/reference-documentation#tag/iDeal-QR

    :param description: Description of the iDeal QR request, which the payer or payers see.
    :param expiry_date_time: The date and time at which the iDeal QR expires and can no longer be paid. The expiration is accurate up to minutes.
    :param amount_in_cents: The amount to pay for the iDeal QR.
    :param reference_id: ID for the reference of the API consumer.
    :param single_pay: Indicates whether the iDeal QR can be paid once, or multiple times.
    :param image_size: Size of the QR code image in pixels. It can be between 100 and 2000 pixels inclusive.
    """
    payload = {
        "description": description,
        "amountInCents": amount_in_cents,
        "expiryDateTime": format_datetime(expiry_date_time),
        "amountChangeable": False,
    }
    if reference_id is not None:
        payload["referenceId"] = reference_id
    if single_pay is not None:
        payload["singlePay"] = single_pay
    if image_size is not None:
        payload["imageSize"] = image_size
    if expiry_date_time is not None:
        payload["expiryDateTime"] = format_datetime(expiry_date_time)

    response = s().post("idealqrs", json=payload)
    return IdealQr.parse_raw(response.content)


def create_changeable(
    *,
    description: str,
    expiry_date_time: datetime,
    max_amount_in_cents: int,
    reference_id: str = None,
    single_pay: bool = None,
    image_size: int = None,
    min_amount_in_cents: int = None,
) -> IdealQr:
    """
    https://developer.abnamro.com/api-products/tikkie/reference-documentation#tag/iDeal-QR

    :param description: Description of the iDeal QR request, which the payer or payers see.
    :param expiry_date_time: The date and time at which the iDeal QR expires and can no longer be paid. The expiration is accurate up to minutes.
    :param max_amount_in_cents: The maximum amount the user can enter for the iDeal QR.
    :param reference_id: ID for the reference of the API consumer.
    :param single_pay: Indicates whether the iDeal QR can be paid once, or multiple times.
    :param image_size: Size of the QR code image in pixels. It can be between 100 and 2000 pixels inclusive.
    :param min_amount_in_cents: The minimum amount the user can enter for the iDeal QR.
    """
    payload = {
        "description": description,
        "expiryDateTime": format_datetime(expiry_date_time),
        "amountChangeable": True,
        "maxAmountInCents": max_amount_in_cents
    }
    if reference_id is not None:
        payload["referenceId"] = reference_id
    if single_pay is not None:
        payload["singlePay"] = single_pay
    if image_size is not None:
        payload["imageSize"] = image_size
    if expiry_date_time is not None:
        payload["expiryDateTime"] = format_datetime(expiry_date_time)
    if min_amount_in_cents is not None:
        payload["minAmountInCents"] = min_amount_in_cents

    response = s().post("idealqrs", json=payload)
    return IdealQr.parse_raw(response.content)


def get(qr_id: str) -> IdealQr:
    """
    Retrieves a specific iDeal QR based on a token value. The
    application must have iDeal QR permission to complete this
    request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#operation/createPaymentRequest
    """
    response = s().get(f"idealqrs/{qr_id}")
    return IdealQr.parse_raw(response.content)


def get_all(
    *,
    page_size: int,
    page_number: int,
    from_date_time: Optional[datetime] = None,
    to_date_time: Optional[datetime] = None,
) -> GetAllIdealQrResponse:
    """
    Retrieves a list of iDeal QRs based on the parameters provided.
    The application must have iDeal QR permission to complete this
    request.

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

    response = s().get("idealqrs", params=params)
    return GetAllIdealQrResponse.parse_raw(response.content)


def get_all_payments(
    *,
    qr_id: str,
    page_size: int,
    page_number: int,
    from_date_time: Optional[datetime] = None,
    to_date_time: Optional[datetime] = None,
) -> GetAllIdealQrPaymentsResponse:
    """
    Retrieves payments made against a specific iDeal QR based on the
    parameters provided. The application must have iDeal QR
    permission to complete this request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#operation/getIDealQR

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

    response = s().get(f"idealqrs/{qr_id}/payments", params=params)
    return GetAllIdealQrPaymentsResponse.parse_raw(response.content)


def get_payment(
    *,
    qr_id: str,
    payment_token: str,
) -> IdealQrPayment:
    """
    Retrieves details of a specific payment made against a specific
    iDeal QR based on the token and ID value. The application must
    have iDeal QR permission to complete this request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#operation/getIDealQRPayment

    :param qr_id: Number of the page to be returned.
    :param payment_token: Number of items on a page.
    """

    response = s().get(f"idealqrs/{qr_id}/payments/{payment_token}")
    return IdealQrPayment.parse_raw(response.content)