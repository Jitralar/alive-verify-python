from alive_verify import (
    AliveAPIError,
    AliveForbiddenError,
    AliveVerifyClient,
    CardType,
    Discount,
    EligibilityError,
    FailureReason,
    Partner,
    Transaction,
    TransactionStatus,
    Verification,
    VerificationMode,
    VerificationResult,
)


def test_public_api_exports():
    assert AliveVerifyClient is not None
    assert Partner is not None
    assert Discount is not None
    assert Verification is not None
    assert EligibilityError is not None
    assert Transaction is not None

    assert CardType.ISIC.value == "ISIC"
    assert VerificationMode.CARDHOLDER.value == "CARDHOLDER"
    assert VerificationResult.SUCCESSFUL.value == "SUCCESSFUL"
    assert FailureReason.CARD_EXPIRED.value == "CARD_EXPIRED"
    assert TransactionStatus.REVOKED.value == "REVOKED"

    assert issubclass(AliveForbiddenError, AliveAPIError)