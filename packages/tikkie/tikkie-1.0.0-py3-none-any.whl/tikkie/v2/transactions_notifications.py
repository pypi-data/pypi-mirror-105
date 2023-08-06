from tikkie import session as s
from tikkie.v2.models import SubscribeResponse


def subscribe(*, url: str) -> SubscribeResponse:
    """
    Subscribes to transactions related notifications. One transaction
    subscription can be active at a time. When this request is
    repeated, the existing transaction subscription is overwritten.
    The application must have transactions permission to complete
    this request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#tag/Transactions-notification

    :param url: URL where notifications must be sent using a webhook or callback.
    """
    payload = {"url": url}

    response = s().post("transactionssubscription", json=payload)
    return SubscribeResponse.parse_raw(response.content)


def delete() -> None:
    """
    Deletes a subscription. The application must have transactions
    permission to complete this request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#operation/subscribeTransactionsNotifications
    """
    s().delete(f"transactionssubscription")
