from tikkie import session as s
from tikkie.v2.models import SubscribeResponse


def subscribe(*, url: str) -> SubscribeResponse:
    """
    Subscribes to payment request related notifications. One payment
    request subscription can be active at a time. When this request
    is repeated, the existing payment request subscription is
    overwritten. The application must have payment request permission
    to complete this request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#tag/Payment-request-notification

    :param url: URL where notifications must be sent using a webhook or callback.
    """
    payload = {"url": url}

    response = s().post("paymentrequestssubscription", json=payload)
    return SubscribeResponse.parse_raw(response.content)


def delete() -> None:
    """
    Deletes a subscription. The application must have payment request
    permission to complete this request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#operation/deletePaymentRequestNotifications
    """
    s().delete(f"paymentrequestssubscription")
