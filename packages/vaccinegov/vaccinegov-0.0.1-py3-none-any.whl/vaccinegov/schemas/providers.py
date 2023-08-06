import json
import typing
import arrow
import httpx
from .manufacturers import VaccineManufacturer


class ProviderLocation(object):
    """Represents the location of a provider."""

    def __init__(self, incoming_data: dict):
        self._raw_data = incoming_data

    @property
    def addresses(self) -> typing.List[str]:
        """Returns the street addresses of a provider."""
        return [self._raw_data["address1"], self._raw_data["address2"]]

    @property
    def city(self) -> str:
        """Returns the city of a provider"""
        return self._raw_data["city"]

    @property
    def state(self) -> str:
        """Returns the state of the provider"""
        return self._raw_data["state"]

    @property
    def zipcode(self) -> str:
        """Returns a zip code of a provider"""
        return self._raw_data["zip"]

    @property
    def coordinates(self) -> typing.Tuple[float, float]:
        """Returns the coordinates of a provider. tuple of lat, long"""
        return (self._raw_data["lat"], self._raw_data["long"])

    def __repr__(self) -> str:
        return f"<VaccineProviderLocation {hex(id(self))}>"

    def __str__(self) -> str:
        return self.addresses[0]


class Provider(object):
    """Represents a single vaccine provider such as your local doctor's office."""

    def __init__(
        self,
        client: httpx.Client,
        incoming_data: dict,
        get_full_information_on_creation=False,
    ):
        self._raw_data = incoming_data
        self._location_generated = ProviderLocation(incoming_data)
        self._client = client
        self._vaccines_available = []

        if self._raw_data.get("distance", False) != False:
            self._found_distance = self._raw_data["distance"]
        else:
            self._found_distance = None

        if get_full_information_on_creation == True:
            self.get_full_information()

    def get_full_information(self):
        try:
            _request_full_information = self._client.get(
                f"/provider-locations/{self.id}"
            )
            _request_full_information.raise_for_status()
            self._raw_data = _request_full_information.json()
        except Exception:
            pass

    def _return_incomplete_or_call_full(self, key_name):
        _get_info = self._raw_data.get(key_name, False)
        if _get_info == False:
            self.get_full_information()
            _get_info = self._raw_data.get(key_name, False)
            if _get_info == False:
                raise KeyError(
                    f"key name {key_name} was not found within incomplete nor full call."
                )
        return _get_info

    @property
    def id(self):
        """Returns the unique id of the provider.

        Returns:
            str: Unique ID for Provider.
        """
        return self._raw_data["guid"]

    @property
    def name(self):
        """Returns the display name of the provider.

        Returns:
            str: Display name of provider
        """
        return self._raw_data["name"]

    @property
    def location(self) -> ProviderLocation:
        """Returns ProviderLocation for provider.

        Returns:
            ProviderLocation: Location information for provider.
        """
        return self._location_generated

    @property
    def distance(self) -> typing.Union[None, float]:
        """Returns distance from the initial search query coordinates (will return None if you do a direct search.)


        Returns:
            typing.Union[None, float]: None if provider information is directly pulled.
        """
        return self._found_distance

    @property
    def prescreening_site(self) -> str:
        """Returns provider's prescreening website.

        Returns:
            str: Provider prescreening site.
        """
        return self._return_incomplete_or_call_full("prescreening_site")

    @property
    def website(self) -> str:
        """Returns the provider's homepage

        Returns:
            str: Provider homepage
        """
        return self._return_incomplete_or_call_full("website")

    @property
    def phone(self) -> str:
        """Returns phone number of provider.

        Returns:
            str: Phone number of provider.
        """
        return self._return_incomplete_or_call_full("phone")

    @property
    def updated(self) -> arrow.Arrow:
        """Returns an Arrow object based on when the provider's information was last updated.

        Returns:
            arrow.Arrow: Generated based on ISO-8601 timestamp
        """
        return arrow.get(self._return_incomplete_or_call_full("last_updated"))

    @property
    def vaccines_available(self) -> typing.List[VaccineManufacturer]:
        """Returns provider's *AVAILABLE* vaccines.

        Returns:
            typing.List[VaccineManufacturer]: List of Available vaccines.
        """
        if self._vaccines_available == []:
            return [
                VaccineManufacturer(vaccine_information)
                for vaccine_information in self._return_incomplete_or_call_full(
                    "inventory"
                )
                if vaccine_information["in_stock"] == "TRUE"
            ]
        return [
            VaccineManufacturer(vaccine_information)
            for vaccine_information in self._vaccines_available
        ]

    @property
    def vaccines_offered(self) -> typing.List[VaccineManufacturer]:
        """Returns all vaccines offered by provider.

        Returns:
            typing.List[VaccineManufacturer]: List of vaccines.
        """
        if self._vaccines_available == []:
            return [
                VaccineManufacturer(vaccine_information)
                for vaccine_information in self._return_incomplete_or_call_full(
                    "inventory"
                )
            ]
        return [
            VaccineManufacturer(vaccine_information)
            for vaccine_information in self._vaccines_available
        ]

    def __repr__(self) -> str:
        return f"<VaccineProvider {self.id}>"

    def __str__(self) -> str:
        return self._raw_data["name"]
