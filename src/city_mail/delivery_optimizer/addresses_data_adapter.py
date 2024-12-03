from typing import Protocol

import httpx
from pydantic import BaseModel


class AddressData(BaseModel):
    name: str
    latitude: float
    longitude: float


class AddressesDataPort(Protocol):
    def get_multiple_addresses_data(self, addresses: list[str]) -> list[AddressData]:
        pass

    def get_address_data(self, address: str) -> AddressData:
        pass


class NominatimAddressesDataAdapter(AddressesDataPort):
    def get_multiple_addresses_data(self, addresses: list[str]) -> list[AddressData]:
        return [self.get_address_data(address) for address in addresses]

    def get_address_data(self, address: str) -> AddressData:
        params = {"q": address, "format": "json"}

        response = httpx.get(
            f"https://nominatim.openstreetmap.org/search", params=params
        )
        response.raise_for_status()

        return self._map_response_to_model(response.json()[0])

    def _map_response_to_model(self, response: dict) -> AddressData:
        return AddressData(
            name=response["display_name"],
            latitude=response["lat"],
            longitude=response["lon"],
        )
