# Alive Verify Python

Unofficial Python client for the Alive Verify API. (focused on ISIC - International Student Identity Card)

The library provides a simple interface for card verification, partner information and transaction reporting using the Alive Verify REST API.

> [!NOTE]
> This project is not affiliated with or endorsed by GTS ALIVE Group.

## Installation

```bash
pip install alive-verify
```

### Authentication
Alive Verify uses HTTP Basic Authentication.¨
```bash

from alive_verify import AliveVerifyClient

client = AliveVerifyClient(
    username="your-username",
    password="your-password",
    environment="test",
)

```

### Available environments:
* test
* production

### Get partner information
```bash
partner = client.get_partner()

print(partner.name)
print(partner.currency)

for discount in partner.discounts:
    print(discount.id, discount.name)
```

### Card verification
#### By cardholder
```bash
verification = client.verify_by_cardholder(
    card_number="S...",
    cardholder_name="John Doe",
    discount_id=12345,
)

if verification.successful:
    print("Card verified")
else:
    print(verification.reason)

```

#### By card number
```bash
verification = client.verify_by_number(
    card_number="S...",
    discount_id=12345,
)
```



#### By RFID chip
```bash
verification = client.verify_by_chip(
    chip_number="EB16CF53",
    discount_id=12345,
)
```


#### By phone number
```bash
verification = client.verify_by_phone(
    cardholder_phone="+420606912554",
    discount_id=12345,
)
```


Availability of verification modes depends on permissions assigned to your Alive Verify API account.

### Transactions
```bash
from datetime import datetime

transaction = client.create_receipt(
    discount_id=12345,
    verification_id=verification.id,
    issued_on=datetime.now().astimezone(),
    amount_paid=100.0,
)
```

#### Revoke a transaction:
```bash
client.revoke_receipt(transaction.id)
```


### Error handling
```bash
from alive_verify import (
    AliveAuthenticationError,
    AliveForbiddenError,
    AliveValidationError,
)

try:
    verification = client.verify_by_number(
        card_number="S...",
    )

except AliveForbiddenError as error:
    print(error)
```


### Development
```bash
Install development dependencies:
pip install -e ".[dev]"

Run unit tests:
pytest -v
```

Integration tests are disabled by default because they call the real Alive Verify test API.To enable them in PowerShell:
```bash
$env:ALIVE_VERIFY_RUN_INTEGRATION="1"
pytest -v tests\integration
``` 

Credentials are loaded from .env:
```bash
ALIVE_VERIFY_USERNAME=...
ALIVE_VERIFY_PASSWORD=...
ALIVE_VERIFY_TEST_CARD_NUMBER=...
ALIVE_VERIFY_TEST_CARDHOLDER_NAME=...
ALIVE_VERIFY_TEST_DISCOUNT_ID=...
```
> [!CAUTION]
> Do not commit .env