from typing import Optional

from pydantic import BaseModel, conint


class CurrencyPair(BaseModel):
    from_currency: str
    to_currencies: Optional[list[str]] = None
    count: conint(ge=0) = 1
