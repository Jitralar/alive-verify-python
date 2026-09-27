import pytest

from alive_verify import AliveVerifyClient
from alive_verify.exceptions import AliveForbiddenError


class FakeResponse:
    ok = False
    status_code = 403
    content = b'{"message":"AccessDeniedHttpException: This account is not allowed to use NUMBER verification."}'

    def json(self):
        return {
            "message": (
                "AccessDeniedHttpException: "
                "This account is not allowed to use NUMBER verification."
            )
        }


def test_forbidden_error(monkeypatch):
    client = AliveVerifyClient(
        username="test-user",
        password="test-password",
        environment="test",
    )

    def fake_request(**kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        client.session,
        "request",
        fake_request,
    )

    with pytest.raises(AliveForbiddenError) as error:
        client.post(
            "/verifications",
            json={"cardNumber": "S123456789012A"},
        )

    assert error.value.status_code == 403
    assert "not allowed to use NUMBER" in str(error.value)