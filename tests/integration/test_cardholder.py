import os
import pytest

from dotenv import load_dotenv

from alive_verify import AliveVerifyClient


load_dotenv()
if os.getenv("ALIVE_VERIFY_RUN_INTEGRATION") != "1":
    pytest.skip(
        "Integration tests are disabled.",
        allow_module_level=True,
    )


def test_verify_by_cardholder():
    client = AliveVerifyClient(
        username=os.environ["ALIVE_VERIFY_USERNAME"],
        password=os.environ["ALIVE_VERIFY_PASSWORD"],
        environment="test",
    )

    verification = client.verify_by_cardholder(
        card_number=os.environ["ALIVE_VERIFY_TEST_CARD_NUMBER"],
        cardholder_name=os.environ["ALIVE_VERIFY_TEST_CARDHOLDER_NAME"],
        discount_id=int(
            os.environ["ALIVE_VERIFY_TEST_DISCOUNT_ID"]
        ),
    )

    assert verification.id > 0
    assert verification.mode == "CARDHOLDER"
    assert verification.result in ["SUCCESSFUL", "FAILED"]