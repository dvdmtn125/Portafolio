import requests

from domain.entities import City
from domain.repositories import CityRepository

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
COUNTRY_CODE = "CO"


class GeocodingCityRepository(CityRepository):
    def __init__(self, timeout_seconds: int = 10) -> None:
        self._timeout_seconds = timeout_seconds

    def get_city_by_name(self, name: str) -> City | None:
        """
        Args:
            name: Nombre de la ciudad a  buscar (ej. "Bucaramanga").
        
        Returns:
            La ciudad encontrada, o None si no hay  resultado en Colombia.

        Raises:
            requests.HTTPError: Si la API responde con un error HTTP.
            requests.Timeout: Si la solicitud excede el tiempo limite.
        """
        params = {
            "name": name,
            "count": 10,
            "country": COUNTRY_CODE,
            "language": "es",
            "format": "json",
        }

        response = requests.get(
            GEOCODING_URL, params=params, timeout=self._timeout_seconds
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        colombian_results = [
            r for r in results if r.get("country_code") == COUNTRY_CODE
        ]

        if not colombian_results:
            return None
        
        best_match = colombian_results[0]
        return City(
            name=best_match["name"],
            latitude=best_match["latitude"],
            longitude=best_match["longitude"],
            department=best_match.get("admin1", "Desconocido"),
        )
    
    def get_all_cities(self) -> list[City]:
        """
        Raises:
            NotImplementedError: Siempre, ya que no existe un catalogo fijo de ciudades
            en esta implementacion.
        """
        raise NotImplementedError(
            "GeocodingCityRepository no mantiene un catalogo fijo de "
            "ciudades; usa get_city_by_name para buscar dinamicamente"
        )