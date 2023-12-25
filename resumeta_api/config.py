# Define the global configs

from fastapi.encoders import jsonable_encoder
import datetime


def encode_input(data) -> dict:
    """Encode the input data."""
    data = jsonable_encoder(data)
    data = {k: v for k, v in data.items() if v is not None}
    return data


date_encoder = {
    datetime.date: lambda dt: datetime.datetime(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    )
}
