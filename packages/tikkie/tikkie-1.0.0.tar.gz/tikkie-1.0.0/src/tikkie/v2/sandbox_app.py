from tikkie import session as s
from tikkie.v2.models import CreateSandboxApplicationResponse


def create_application() -> CreateSandboxApplicationResponse:
    """
    Creates an app in the sandbox for you to use with this API. This
    operation does not work in the production environment.

    https://developer.abnamro.com/api-products/tikkie/reference-documentation#tag/Sandbox-app

    :param app_token: Description of the payment request, which the payer or payers see.
    """
    response = s().post("sandboxapps")
    return CreateSandboxApplicationResponse.parse_raw(response.content)
