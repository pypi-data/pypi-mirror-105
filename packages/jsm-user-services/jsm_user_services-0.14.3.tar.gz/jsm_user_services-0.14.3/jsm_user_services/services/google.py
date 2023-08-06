import logging

from jsm_user_services.support.http_utils import request
from jsm_user_services.support.settings_utils import get_from_settings_or_raise_missing_config

logger = logging.getLogger(__name__)


def perform_recaptcha_validation(g_recaptcha_response: str) -> bool:
    """
    Performs a request to Google in order to validate the reCAPTCHA.
    For more details, check: https://developers.google.com/recaptcha/docs/verify
    """

    google_recaptcha_url = get_from_settings_or_raise_missing_config(
        "GOOGLE_RECAPTCHA_URL", "https://www.google.com/recaptcha/api/siteverify"
    )
    google_recaptcha_secret_key = get_from_settings_or_raise_missing_config("GOOGLE_RECAPTCHA_SECRET_KEY")

    logger.info("Checking GoogleRecaptcha")

    data = {"response": g_recaptcha_response, "secret": google_recaptcha_secret_key}

    with request() as r:
        resp = r.post(google_recaptcha_url, data=data)
    
    result_json = resp.json()

    if not result_json.get("success"):
        logger.info(f"GoogleRecaptcha failed! Input: {g_recaptcha_response} Output: {result_json}")

    return result_json.get("success")
