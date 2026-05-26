from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator


app = FastAPI(title="KBank BillPayment API", version="1.0.0")


# Mock data for inquiry/lookup. Replace this with real database queries in production.
LOOKUP_DATA = {
    ("300000025751", "1733084"): {
        "tranAmount": "120.00",
        "terminalNo": "xxxxxxx8888",
        "billerType": "",
        "info1": "",
        "info2": "",
        "info3": "",
        "duedate": "",
        "rtpReference": "",
    },
    ("300000025752", "1733085"): {
        "tranAmount": "250.00",
        "terminalNo": "xxxxxxx8888",
        "billerType": "",
        "info1": "",
        "info2": "",
        "info3": "",
        "duedate": "",
        "rtpReference": "",
    },
}


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


class BillLookupRequest(BaseModel):
    functionName: str
    transactionId: str
    transactionDateTime: datetime
    billerType: str = ""
    billerId: str
    terminalNo: str
    channelCode: str = ""
    tranAmount: str = ""
    senderBankCode: str
    reference1: str = ""
    reference2: str = ""
    language: Optional[str] = "EN"
    apiKey: str

    @field_validator("functionName")
    @classmethod
    def validate_function_name(cls, value: str) -> str:
        if value != "BillLookup":
            raise ValueError('functionName must be "BillLookup"')
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

    @field_validator("terminalNo")
    @classmethod
    def validate_terminal_no(cls, value: str) -> str:
        if value != "xxxxxxx8888":
            raise ValueError('terminalNo must be "xxxxxxx8888" for this mock inquiry')
        return value

    @field_validator("channelCode")
    @classmethod
    def validate_channel_code(cls, value: str) -> str:
        if value != "MOB":
            raise ValueError('channelCode must be "MOB" for this mock inquiry')
        return value

    @field_validator("apiKey")
    @classmethod
    def validate_api_key(cls, value: str) -> str:
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


class BillLookupResponse(BaseModel):
    functionName: str = "BillLookupResponse"
    transactionId: str
    transactionDateTime: str
    billerTransactionId: str
    responseCode: str = "0000"
    responseDescription: str = "Success"
    billerType: str
    billerId: str
    terminalNo: str
    reference1: str
    reference2: str
    info1: str = ""
    info2: str = ""
    info3: str = ""
    duedate: str = ""
    rtpReference: str = ""
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


@app.post("/bell/v1/billpayment/payment", response_model=BillPaymentResponse)
def bill_payment_bell(request: BillPaymentRequest) -> BillPaymentResponse:
    return bill_payment(request)


@app.post("/pang/v1/billpayment/payment", response_model=BillPaymentResponse)
def bill_payment_pang(request: BillPaymentRequest) -> BillPaymentResponse:
    return bill_payment(request)


@app.post("/v1/billpayment/lookup", response_model=BillLookupResponse)
def bill_lookup(request: BillLookupRequest) -> BillLookupResponse:
    try:
        response_datetime = datetime.now().astimezone().isoformat(timespec="milliseconds")
        lookup_key = (request.reference1, request.reference2)
        record = LOOKUP_DATA.get(lookup_key)

        if record is None:
            return BillLookupResponse(
                transactionId=request.transactionId,
                transactionDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1001",
                responseDescription="Data not found",
                billerType=request.billerType,
                billerId=request.billerId,
                terminalNo=request.terminalNo,
                reference1=request.reference1,
                reference2=request.reference2,
            )

        if request.tranAmount and request.tranAmount != record["tranAmount"]:
            return BillLookupResponse(
                transactionId=request.transactionId,
                transactionDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1002",
                responseDescription="Invalid amount",
                billerType=record["billerType"],
                billerId=request.billerId,
                terminalNo=record["terminalNo"],
                reference1=request.reference1,
                reference2=request.reference2,
                info1=record["info1"],
                info2=record["info2"],
                info3=record["info3"],
                duedate=record["duedate"],
                rtpReference=record["rtpReference"],
            )

        return BillLookupResponse(
            transactionId=request.transactionId,
            transactionDateTime=response_datetime,
            billerTransactionId=request.transactionId,
            billerType=record["billerType"],
            billerId=request.billerId,
            terminalNo=record["terminalNo"],
            reference1=request.reference1,
            reference2=request.reference2,
            info1=record["info1"],
            info2=record["info2"],
            info3=record["info3"],
            duedate=record["duedate"],
            rtpReference=record["rtpReference"],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/bell/v1/billpayment/lookup", response_model=BillLookupResponse)
def bill_lookup_bell(request: BillLookupRequest) -> BillLookupResponse:
    return bill_lookup(request)


@app.post("/pang/v1/billpayment/lookup", response_model=BillLookupResponse)
def bill_lookup_pang(request: BillLookupRequest) -> BillLookupResponse:
    return bill_lookup(request)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
