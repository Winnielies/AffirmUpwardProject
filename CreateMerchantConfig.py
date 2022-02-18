from xmlrpc.client import boolean
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, root_validator

app = FastAPI()

class MerchantConfig(BaseModel):
    minimum_amount: float = 0.0
    maximum_amount: float
    prequal_enabled: bool = False
    
    # Validator to check for true/false which are treated as 1/0
    @root_validator(pre=True)
    def check_bool(cls, values):
        max_amount = values.get("maximum_amount")
        min_amount = values.get("minimum_amount")

        if type(max_amount) == boolean or type(min_amount) == boolean:
            raise TypeError("please enter a valid number")
        return values
    
    class MerchantExtra:
        schema_extra = {
            "example": [
            {
                "minimum_amount": 30000,
                "maximum_amount": 200000,
                "prequal_enabled": True
            }],
            "description": [
            {
                "minimum_amount": "Minimum amount (in cents) that a consumer can get a loan for",
                "maximum_amount": "Maximum amount (in cents) that a consumer can get a loan for",
                "prequal_enabled": "Flag to indicate if Prequal feature is enabled for this merchant"
            }]
        }

# In-memory storage
merchant_data = [{"merchant_id": "1"}, 
                {"merchant_id": "2"},
                {"merchant_id": "3" },
                {"merchant_id":"4f572866-0e85-11ea-94a8-acde48001122"}
                ]

@app.post("/{merchant_id}")
def create_merchant(merchant:MerchantConfig, merchant_id: str):
    merchant_profile = merchant.dict()

    # Check to ensure that the max amount is greater than min amount and both max and min are non-negative values
    if merchant_profile["maximum_amount"] <= merchant_profile["minimum_amount"]:
        return JSONResponse(status_code = 400, content = "Maximum loan amount is less than or equal to minimum amount")
    elif merchant_profile["maximum_amount"] < 0 or merchant_profile["minimum_amount"] < 0:
        return JSONResponse(status_code = 400, content = "Loan amount can not be less than 0")

    # Check the in-memory storage to ensure the merchant exists in the storage via merchant id
    for index, merchant in enumerate(merchant_data):
        if merchant["merchant_id"] == merchant_id:
            merchant["minimum_amount"] = merchant_profile["minimum_amount"]
            merchant["maximum_amount"] = merchant_profile["maximum_amount"]
            merchant["prequal_enabled"] = merchant_profile["prequal_enabled"]
            return {"Merchant ID":merchant_id}

        elif (index == len(merchant_data) - 1) & (merchant["merchant_id"] != merchant_id):
            return JSONResponse(status_code = 400, content = "Merchant is not found in the database")




