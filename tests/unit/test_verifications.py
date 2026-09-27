from alive_verify import AliveVerifyClient
from datetime import datetime
from alive_verify.enums import FailureReason



def test_verify_by_number(monkeypatch):
    client = AliveVerifyClient(
        username="test-user",
        password="test-password",
        environment="test",
    )

    def fake_post(endpoint, json=None):
        assert endpoint == "/verifications"

        assert json == {
            "cardNumber": "S123456789012A",
            "discountId": 14448,
        }

        return {
            "id": 123,
            "createdOn": "2026-09-27T00:00:00+00:00",
            "cardNumber": "S123456789012A",
            "mode": "NUMBER",
            "discountId": 14448,
            "result": "SUCCESSFUL",
            "cardType": "ISIC",
        }

    monkeypatch.setattr(
        client,
        "post",
        fake_post,
    )

    verification = client.verify_by_number(
        card_number="S123456789012A",
        discount_id=14448,
    )

    assert verification.id == 123
    assert verification.mode == "NUMBER"
    assert verification.result == "SUCCESSFUL"
    assert verification.successful is True
    assert verification.card_type == "ISIC"
    assert isinstance(verification.created_on, datetime)

def test_verify_by_cardholder(monkeypatch):
    client = AliveVerifyClient(
        username="test-user",
        password="test-password",
        environment="test",
    )

    def fake_post(endpoint, json=None):
        assert endpoint == "/verifications"

        assert json == {
            "cardNumber": "S123456789012A",
            "cardholderName": "John Doe",
            "discountId": 14448,
        }

        return {
            "id": 456,
            "createdOn": "2026-09-27T00:00:00+00:00",
            "cardNumber": "S123456789012A",
            "cardholderName": "John Doe",
            "mode": "CARDHOLDER",
            "discountId": 14448,
            "result": "SUCCESSFUL",
            "cardType": "ISIC",
        }

    monkeypatch.setattr(
        client,
        "post",
        fake_post,
    )

    verification = client.verify_by_cardholder(
        card_number="S123456789012A",
        cardholder_name="John Doe",
        discount_id=14448,
    )

    assert verification.id == 456
    assert verification.mode == "CARDHOLDER"
    assert verification.successful is True
    assert verification.cardholder_name == "John Doe"
    assert isinstance(verification.created_on, datetime)

def test_failed_verification_with_eligibility_error(monkeypatch):
    client = AliveVerifyClient(
        username="test-user",
        password="test-password",
        environment="test",
    )

    def fake_post(endpoint, json=None):
        return {
            "id": 789,
            "createdOn": "2026-09-27T00:00:00+00:00",
            "cardNumber": "S123456789012A",
            "mode": "CARDHOLDER",
            "discountId": 14448,
            "result": "FAILED",
            "reason": "NOT_ELIGIBLE",
            "cardType": "ISIC",
            "eligibilityErrors": [
                {
                    "code": "rateQuota.exceeded",
                    "params": {
                        "limit": 1,
                        "interval": 1,
                        "type": "CARD",
                    },
                }
            ],
        }

    monkeypatch.setattr(
        client,
        "post",
        fake_post,
    )

    verification = client.verify_by_cardholder(
        card_number="S123456789012A",
        cardholder_name="John Doe",
        discount_id=14448,
    )

    assert verification.successful is False
    assert verification.reason.value == "NOT_ELIGIBLE"

    assert len(verification.eligibility_errors) == 1

    error = verification.eligibility_errors[0]

    assert error.code == "rateQuota.exceeded"
    assert error.params["limit"] == 1
    assert error.params["type"] == "CARD"
    assert verification.reason == FailureReason.NOT_ELIGIBLE


def test_verify_by_chip(monkeypatch):
    client = AliveVerifyClient(
        username="test-user",
        password="test-password",
        environment="test",
    )

    def fake_post(endpoint, json=None):
        assert endpoint == "/verifications"

        assert json == {
            "chipNumber": "EB16CF53",
            "discountId": 14448,
        }

        return {
            "id": 1001,
            "createdOn": "2026-09-27T00:00:00+00:00",
            "mode": "CHIP",
            "discountId": 14448,
            "result": "SUCCESSFUL",
            "cardType": "ISIC",
            "chipNumber": "EB16CF53",
        }

    monkeypatch.setattr(client, "post", fake_post)

    verification = client.verify_by_chip(
        chip_number="EB16CF53",
        discount_id=14448,
    )

    assert verification.mode == "CHIP"
    assert verification.chip_number == "EB16CF53"
    assert verification.successful is True
    assert isinstance(verification.created_on, datetime)


def test_verify_by_phone(monkeypatch):
    client = AliveVerifyClient(
        username="test-user",
        password="test-password",
        environment="test",
    )

    def fake_post(endpoint, json=None):
        assert endpoint == "/verifications"

        assert json == {
            "cardholderPhone": "+420606912554",
            "cardholderName": "John Doe",
            "discountId": 14448,
        }

        return {
            "id": 1002,
            "createdOn": "2026-09-27T00:00:00+00:00",
            "cardholderName": "John Doe",
            "cardholderPhone": "+420606912554",
            "mode": "PHONE",
            "discountId": 14448,
            "result": "SUCCESSFUL",
            "cardType": "ISIC",
        }

    monkeypatch.setattr(client, "post", fake_post)

    verification = client.verify_by_phone(
        cardholder_phone="+420606912554",
        cardholder_name="John Doe",
        discount_id=14448,
    )

    assert verification.mode == "PHONE"
    assert isinstance(verification.created_on, datetime)
    assert verification.cardholder_phone == "+420606912554"
    assert verification.successful is True