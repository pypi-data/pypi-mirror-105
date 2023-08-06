import json
import requests


class Payment:
    def create_token(amount, on_success_endpoint=None, metadata=None):
        from zage import secret_key, payment_create_token

        if not secret_key:
            raise ValueError(
                "You must specify your secret key before calling create_token!"
            )

        data = {
            "secretKey": secret_key,
            "amount": amount,
        }

        if on_success_endpoint:
            data["onSuccessEndpoint"] = on_success_endpoint

        if metadata:
            if isinstance(metadata, dict):
                data["metadata"] = json.dumps(metadata)
            elif isinstance(metadata, str):
                data["metadata"] = metadata
            else:
                data["metadata"] = str(metadata)

        try:
            return requests.post(payment_create_token, data=data).json()
        except:
            return {"token": None}
