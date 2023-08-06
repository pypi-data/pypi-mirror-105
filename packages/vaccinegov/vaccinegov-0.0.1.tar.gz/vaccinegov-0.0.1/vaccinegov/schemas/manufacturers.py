class VaccineManufacturer(object):
    """Represents a Vaccine Manufacturer such as Pfizer"""

    def __init__(self, raw_data):
        self._raw_data = raw_data

    @property
    def id(self) -> str:
        """Vaccine GUID

        Returns:
            str: GUID of Vaccine
        """
        return self._raw_data["guid"]

    @property
    def name(self) -> str:
        """Vaccine Display name

        Returns:
            str: Vaccine display name
        """
        return self._raw_data["name"]

    def __repr__(self) -> str:
        return f"<VaccineManufacturer {self._raw_data.get('name', 'UnknownManufacturer').replace(' ', '').replace('&', '')}>"

    def __str__(self) -> str:
        return self.name
