from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator


app = FastAPI(title="KBank BillPayment API", version="1.0.0")


class BillPaymentRequest(BaseModel):
    functionName: str
    transactionId: str
    transactionDateTime: datetime
    billerType: str = ""
    billerId: str
    terminalNo: str
    channelCode: str
    tranAmount: str
    senderBankCode: str
    isRetry: str
    reference1: str
    reference2: str
    language: Optional[str] = "EN"
    apiKey: str
    dueDate: Optional[str] = ""
    rtpReference: Optional[str] = ""
    rqAppId: Optional[str] = ""

    @field_validator("functionName")
    @classmethod
    def validate_function_name(cls, value: str) -> str:
        if value != "BillPayment":
            raise ValueError('functionName must be "BillPayment"')
        return value

    @field_validator("billerId")
    @classmethod
    def validate_biller_id(cls, value: str) -> str:
        if value != "98499":
            raise ValueError('billerId must be "98499"')
        return value

    @field_validator("senderBankCode")
    @classmethod
    def validate_sender_bank_code(cls, value: str) -> str:
        if value != "Kbank":
            raise ValueError('senderBankCode must be "Kbank"')
        return value

    @field_validator("isRetry")
    @classmethod
    def validate_is_retry(cls, value: str) -> str:
        if value != "0":
            raise ValueError('isRetry must be "0" for this exercise')
        return value

    @field_validator("apiKey")
    @classmethod
    def validate_api_key(cls, value: str) -> str:
        # Exercise docs sometimes show "SequreKey123" and sometimes "SecureKey123".
        # Accept both values to keep compatibility.
        if value not in {"SequreKey123", "SecureKey123"}:
            raise ValueError('apiKey must be "SequreKey123" or "SecureKey123"')
        return value

    @field_validator("transactionDateTime")
    @classmethod
    def validate_transaction_datetime_today(cls, value: datetime) -> datetime:
        current_date = datetime.now(value.tzinfo).date() if value.tzinfo else datetime.now().date()
        if value.date() != current_date:
            raise ValueError("transactionDateTime must be today")
        return value


class BillPaymentResponse(BaseModel):
    functionName: str = "BillPaymentResponse"
    transactionId: str
    responseDateTime: str
    billerTransactionId: str
    responseCode: str = "0000"
    responseDescription: str = "Success"
    terminalNo: str
    settlementDate: str = ""
    rsAppId: str = ""


@app.post("/v1/billpayment/payment", response_model=BillPaymentResponse)
def bill_payment(request: BillPaymentRequest) -> BillPaymentResponse:
    try:
        response_datetime = datetime.now().astimezone().isoformat(timespec="milliseconds")

        return BillPaymentResponse(
            transactionId=request.transactionId,
            responseDateTime=response_datetime,
            billerTransactionId=request.transactionId,
            terminalNo=request.terminalNo,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
