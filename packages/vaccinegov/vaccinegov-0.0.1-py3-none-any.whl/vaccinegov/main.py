from httpx import Client
from .schemas.providers import Provider, ProviderLocation
from .schemas.manufacturers import VaccineManufacturer
import typing
from loguru import logger


class VaccinesGov(object):
    def __init__(self):
        self._base_client = Client(
            base_url="https://api.us.castlighthealth.com/vaccine-finder/v1/",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
            },
        )

    def available_vaccines(self) -> typing.List[VaccineManufacturer]:
        """Current available vaccines available to the U.S Population

        Returns:
            typing.List[VaccineManufacturer]: List of Vaccines
        """
        _request = self._base_client.get("/medications")
        _request.raise_for_status()
        return [VaccineManufacturer(raw_data=x) for x in _request.json()]

    def lookup_provider(self, unique_id) -> Provider:
        """Lookup provider by unique id.

        Args:
            unique_id (str): Unique ID of provider.

        Returns:
            Provider: Provider
        """
        try:
            _request = self._base_client.get(f"/provider-locations/{unique_id}")
            _request.raise_for_status()
            return Provider(client=self._base_client, incoming_data=_request.json())
        except Exception:
            logger.exception("issue searching")

    def search_via_coordinates(
        self, vaccines: typing.List[VaccineManufacturer], latitude, longitude, radius=25
    ):

        """Search for a vaccine available within a radius of provided latitude and longitude.

        Args:
            vaccines (typing.List[VaccineManufacturer]): List of vaccines you would like to search.
            latitude (float): Latitude of location
            longitude (float): Longitude of location
            radius (int, optional): Radius to search within.. Increasing this radius may result in errors.. Defaults to 25 miles.
        """
        try:
            _vaccine_ids = [x.id for x in vaccines]
            _request_for_search = self._base_client.get(
                "/provider-locations/search",
                params={
                    "medicationGuids": ",".join(_vaccine_ids),
                    "lat": latitude,
                    "long": longitude,
                    "radius": radius,
                },
            )
            _request_for_search.raise_for_status()
            _results = [
                Provider(client=self._base_client, incoming_data=x)
                for x in _request_for_search.json()["providers"]
            ]
            return _results
        except Exception:
            logger.exception("Issue searching")

    def search_via_zip_code(
        self, vaccines: typing.List[VaccineManufacturer], zipcode, radius=25
    ):
        """Helper function that will find the correct latitude and longitude from provided zip code.
        This will use the https://public.opendatasoft.com/ API and forward coordinates to ``search_via_coordinates``

        Args:
            vaccines (typing.List[VaccineManufacturer]): List of vaccines you would like to search.
            zipcode (int): U.S Zip Code
            radius (int, optional): Radius to search within.. Increasing this radius may result in errors.. Defaults to 25 miles.
        """
        try:
            _request_for_coordinates_from_zipcode = self._base_client.get(
                "https://public.opendatasoft.com/api/records/1.0/search/",
                params={"dataset": "us-zip-code-latitude-and-longitude", "q": zipcode},
            )
            _request_for_coordinates_from_zipcode.raise_for_status()
            _request_for_coordinates_from_zipcode = (
                _request_for_coordinates_from_zipcode.json()
            )
            logger.debug(
                f"Location: {zipcode} > {_request_for_coordinates_from_zipcode['records'][0]['fields']['city']} => ({_request_for_coordinates_from_zipcode['records'][0]['fields']['latitude']}lat, {_request_for_coordinates_from_zipcode['records'][0]['fields']['longitude']}long)"
            )
        except Exception:
            logger.exception("issue searching")

        return self.search_via_coordinates(
            vaccines=vaccines,
            latitude=_request_for_coordinates_from_zipcode["records"][0]["fields"][
                "latitude"
            ],
            longitude=_request_for_coordinates_from_zipcode["records"][0]["fields"][
                "longitude"
            ],
            radius=radius,
        )
