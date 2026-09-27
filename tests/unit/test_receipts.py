from alive_verify import AliveVerifyClient
from datetime import datetime

def test_create_receipt(monkeypatch):
    client = AliveVerifyClient(
        username="test-user",
        password="test-password",
        environment="test",
    )

    def fake_post(endpoint, json=None):
        assert endpoint == "/receipts"

        assert json == {
            "discountId": 14448,
            "verificationId": 123456,
            "issuedOn": "2026-09-27T02:45:00+02:00",
            "amountPaid": 100.0,
        }

        return {
            "createdOn": "2026-09-27T00:45:01+00:00",
            "id": 987654,
            "discountId": 14448,
            "verificationId": 123456,
            "amountPaid": 100.0,
            "issuedOn": "2026-09-27T00:45:00+00:00",
        }

    monkeypatch.setattr(
        client,
        "post",
        fake_post,
    )

    transaction = client.create_receipt(
        discount_id=14448,
        verification_id=123456,
        issued_on="2026-09-27T02:45:00+02:00",
        amount_paid=100.0,
    )

    assert transaction.id == 987654
    assert transaction.discount_id == 14448
    assert transaction.verification_id == 123456
    assert transaction.amount_paid == 100.0
    assert isinstance(transaction.created_on, datetime)
    assert isinstance(transaction.issued_on, datetime)



def test_revoke_receipt(monkeypatch):
    client = AliveVerifyClient(
        username="test-user",
        password="test-password",
        environment="test",
    )

    def fake_put(endpoint, json=None):
        assert endpoint == "/receipts/987654/status"
        assert json == {
            "status": "REVOKED",
        }

        return None

    monkeypatch.setattr(
        client,
        "put",
        fake_put,
    )

    result = client.revoke_receipt(987654)

    assert result is None