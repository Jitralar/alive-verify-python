import requests
from requests.auth import HTTPBasicAuth
from datetime import date, datetime
from .utils import serialize_date, serialize_datetime
from .models import Partner, Verification, Transaction

from .exceptions import (
    AliveAPIError,
    AliveAuthenticationError,
    AliveForbiddenError,
    AliveValidationError,
)


class AliveVerifyClient:

    TEST_URL = "https://dm.test.aliveplatform.com/api"
    PRODUCTION_URL = "https://dm.aliveplatform.com/api"

    def __init__(
        self,
        username: str,
        password: str,
        environment: str = "test",
        timeout: float = 10.0,
    ):
        if environment == "test":
            self.base_url = self.TEST_URL
        elif environment == "production":
            self.base_url = self.PRODUCTION_URL
        else:
            raise ValueError("Environment must be 'test' or 'production'.")

        self.timeout = timeout

        self.session = requests.Session()

        self.session.auth = HTTPBasicAuth(
            username,
            password,
        )

        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict | None = None,
        json: dict | None = None,
    ):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            timeout=self.timeout,
        )


        if not response.ok:
            try:
                error_data = response.json()
            except ValueError:
                error_data = {}

            message = error_data.get(
                "message",
                f"Alive Verify API returned HTTP {response.status_code}",
            )

            if response.status_code == 400:
                raise AliveValidationError(
                    message,
                    status_code=response.status_code,
                    response=error_data,
                )

            if response.status_code == 401:
                raise AliveAuthenticationError(
                    message,
                    status_code=response.status_code,
                    response=error_data,
                )

            if response.status_code == 403:
                raise AliveForbiddenError(
                    message,
                    status_code=response.status_code,
                    response=error_data,
                )

            raise AliveAPIError(
                message,
                status_code=response.status_code,
                response=error_data,
            )

        if not response.content:
            return None

        return response.json()

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ):
        return self._request(
            "GET",
            endpoint,
            params=params,
        )

    def post(
        self,
        endpoint: str,
        json: dict | None = None,
    ):
        return self._request(
            "POST",
            endpoint,
            json=json,
        )

    def put(
        self,
        endpoint: str,
        json: dict | None = None,
    ):
        return self._request(
            "PUT",
            endpoint,
            json=json,
        )

    def get_partner(self) -> Partner:
        data = self.get("/partner")

        return Partner.from_dict(data)

    def _add_verification_options(
        self,
        data: dict,
        discount_id: int | None = None,
        cardholder_date_of_birth: date | str | None = None,
        card_valid_longer_than: date | str | None = None,
    ) -> dict:

        if discount_id is not None:
            data["discountId"] = discount_id

        if cardholder_date_of_birth is not None:
            data["cardholderDateOfBirth"] = serialize_date(
                cardholder_date_of_birth
            )

        if card_valid_longer_than is not None:
            data["cardValidLongerThan"] = serialize_date(
                card_valid_longer_than
            )

        return data


    def _verify(self, data: dict) -> Verification:
        response = self.post(
            "/verifications",
            json=data,
        )

        return Verification.from_dict(response)


    def verify_by_number(
        self,
        card_number: str,
        discount_id: int | None = None,
        cardholder_date_of_birth: date | str | None = None,
        card_valid_longer_than: date | str | None = None,
    ) -> Verification:

        data = {
            "cardNumber": card_number,
        }

        data = self._add_verification_options(
            data,
            discount_id,
            cardholder_date_of_birth,
            card_valid_longer_than,
        )

        return self._verify(data)

    def verify_by_cardholder(
        self,
        card_number: str,
        cardholder_name: str,
        discount_id: int | None = None,
        cardholder_date_of_birth: date | str | None = None,
        card_valid_longer_than: date | str | None = None,
    ) -> Verification:

        data = {
            "cardNumber": card_number,
            "cardholderName": cardholder_name,
        }

        data = self._add_verification_options(
            data,
            discount_id,
            cardholder_date_of_birth,
            card_valid_longer_than,
        )

        return self._verify(data)


    def verify_by_chip(
        self,
        chip_number: str,
        discount_id: int | None = None,
        cardholder_date_of_birth: date | str | None = None,
        card_valid_longer_than: date | str | None = None,
    ) -> Verification:

        data = {
            "chipNumber": chip_number,
        }

        data = self._add_verification_options(
            data,
            discount_id,
            cardholder_date_of_birth,
            card_valid_longer_than,
        )

        return self._verify(data)


    def verify_by_phone(
        self,
        cardholder_phone: str,
        cardholder_name: str | None = None,
        discount_id: int | None = None,
        cardholder_date_of_birth: date | str | None = None,
        card_valid_longer_than: date | str | None = None,
    ) -> Verification:

        data = {
            "cardholderPhone": cardholder_phone,
        }

        if cardholder_name is not None:
            data["cardholderName"] = cardholder_name

        data = self._add_verification_options(
            data,
            discount_id,
            cardholder_date_of_birth,
            card_valid_longer_than,
        )

        return self._verify(data)

    def create_receipt(
        self,
        discount_id: int,
        verification_id: int,
        issued_on: datetime | str,
        amount_paid: float,
    ) -> Transaction:

        data = {
            "discountId": discount_id,
            "verificationId": verification_id,
            "issuedOn": serialize_datetime(issued_on),
            "amountPaid": amount_paid,
        }

        response = self.post(
            "/receipts",
            json=data,
        )

        return Transaction.from_dict(response)

    def revoke_receipt(self, receipt_id: int) -> None:
        self.put(
            f"/receipts/{receipt_id}/status",
            json={
                "status": "REVOKED",
            },
        )