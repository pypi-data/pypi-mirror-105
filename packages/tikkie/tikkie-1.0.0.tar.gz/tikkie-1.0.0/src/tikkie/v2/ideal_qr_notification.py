from tikkie import session as s
from tikkie.v2.models import SubscribeResponse


def subscribe(*, url: str) -> SubscribeResponse:
    """
    Subscribes to iDeal QR notifications. One iDeal QR subscription can
    be active at a time only. When this request is repeated, the
    existing iDeal QR subscription is overwritten. The application must
    have iDeal QR permission to complete this request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#tag/iDeal-QR-notification

    :param url: URL where notifications must be sent using a webhook or callback.
    """
    payload = {"url": url}

    response = s().post("idealqrssubscription", json=payload)
    breakpoint()
    return SubscribeResponse.parse_raw(response.content)


def delete() -> None:
    """
    Deletes a subscription. The application must have iDeal QR
    permission to complete this request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#operation/deleteIDealQRNotifications
    """
    s().delete(f"idealqrssubscription")
