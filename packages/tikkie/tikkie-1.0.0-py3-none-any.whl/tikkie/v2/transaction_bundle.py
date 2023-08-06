from datetime import datetime
from typing import Optional

from tikkie import session as s
from tikkie.v2.models import Bundle, GetAllBundlesResponse


def get(bundle_id: str) -> Bundle:
    """
    Retrieves a specific bundle based on a bundle identifier. The
    application must have transactions permission to complete this
    request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#operation/getBundle
    """
    response = s().get(f"transactionbundles/{bundle_id}")
    return Bundle.parse_raw(response.content)


def get_all(
    *,
    page_size: int,
    page_number: int,
    from_date_time: Optional[datetime] = None,
    to_date_time: Optional[datetime] = None,
) -> GetAllBundlesResponse:
    """
    Retrieves a list of bundles based on the parameters provided. The
    application must have transactions permission to complete this request.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#operation/getBundleList

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

    response = s().get("transactionbundles", params=params)
    return GetAllBundlesResponse.parse_raw(response.content)
