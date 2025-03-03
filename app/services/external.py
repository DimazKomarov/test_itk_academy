from httpx import AsyncClient

from core.config import settings


class ExternalService:
    @staticmethod
    async def get_response(url):
        async with AsyncClient() as client:
            response = await client.get(url, headers={"apikey": settings.API_KEY})
            return response.json()

    @classmethod
    async def get_list_of_currencies(cls):
        url = f"{settings.API_BASE_URL}/currencies"
        result = await cls.get_response(url)

        result_dict = {}
        for key, value in result["data"].items():
            value = {
                "name": value["name"],
                "code": value["code"],
                "symbol": value["symbol"],
            }
            result_dict.update({key: value})

        return result_dict

    @classmethod
    async def convert_currencies(cls, currency_pair: dict):
        url = f"{settings.API_BASE_URL}/latest?base_currency={currency_pair["from_currency"]}"

        if currency_pair["to_currencies"]:
            currencies = ','.join(currency_pair["to_currencies"])
            url = f"{url}&currencies={currencies}"

        result = await cls.get_response(url)
        result_dict = {}
        for key, value in result["data"].items():
            result_dict.update({key: value * currency_pair["count"]})

        return result_dict
