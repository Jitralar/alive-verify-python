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


def test_get_partner():
    client = AliveVerifyClient(
        username=os.environ["ALIVE_VERIFY_USERNAME"],
        password=os.environ["ALIVE_VERIFY_PASSWORD"],
        environment="test",
    )

    partner = client.get_partner()

    assert partner.name
    assert partner.currency
    assert len(partner.discounts) > 0