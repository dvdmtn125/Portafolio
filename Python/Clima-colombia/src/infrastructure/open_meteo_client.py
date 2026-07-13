from datetime import date, datetime

import requests

from domain.entities import City, WeatherRecord
from domain.repositories import WeatherRepository

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

DAILY_PARAMS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "relative_humidity_2m_mean",
]


class OpenMeteoClient(WeatherRepository):
    def __init__(self, timeout_seconds: int = 10):
        self._timeout_seconds = timeout_seconds

    def get_weather_history(
            self, city: City, start_date: date, end_date: date
    ) -> list[WeatherRecord]:
        """
        Args:
            city: Ciudad para la cual se desea obtener el historial del clima.
            start_date: Fecha de inicio del historial (inclusive).
            end_date: Fecha de fin del historial (inclusive).

        Returns:
            Lista de registros climaticos ordenados por fecha.

        Raises:
            requests.HTTPError: Si la API responde con error HTTP.
            requests.Timeout: Si la solicitud excede el tiempo de espera configurado.
        """
        params = {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "daily": ",".join(DAILY_PARAMS),
            "timezone": "America/Bogota",
        }

        response = requests.get(
            ARCHIVE_URL, params=params, timeout=self._timeout_seconds
        )
        response.raise_for_status()
        data = response.json()

        return self._parse_daily_records(city, data)
    
    def get_current_weather(self, city: City) -> WeatherRecord:
        """
        Args:
            city: Ciudad para la cual se desea obtener el clima actual.

        Returns:
            Registro climático actual.

        Raises:
            requests.HTTPError: Si la API responde con error HTTP.
            requests.Timeout: Si la solicitud excede el tiempo de espera configurado.
        """
        params = {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "daily": ",".join(DAILY_PARAMS),
            "timezone": "America/Bogota",
            "forecast_days": 1,
        }

        response = requests.get(
            FORECAST_URL, params=params, timeout=self._timeout_seconds
        )
        response.raise_for_status()
        data = response.json()

        records = self._parse_daily_records(city, data)
        if not records:
            raise ValueError(
                f"Open-Meteo no devolvio datos para {city.name}"
            )
        return records[0]
    
    def _parse_daily_records(
            self, city: City, data: dict
    ) -> list[WeatherRecord]:
        """
        Args:
            city: Ciudad para la cual se desea obtener los registros diarios.
            data: Respuesta JSON devuelta por la API de Open-Meteo (Seccion "daily").

        Returns:
            Lista de registros climaticos diarios ordenados por fecha.
        """
        daily = data.get("daily", {})
        dates = daily.get("time", [])
        temps_max = daily.get("temperature_2m_max", [])
        temps_min = daily.get("temperature_2m_min", [])
        precipitation = daily.get("precipitation_sum", [])
        humidity = daily.get("relative_humidity_2m_mean", [])

        records = []
        for i, date_str in enumerate(dates):
            record = WeatherRecord(
                city=city,
                record_date=datetime.strptime(date_str, "%Y-%m-%d").date(),
                temperature_max=temps_max[i],
                temperature_min=temps_min[i],
                precipitation_mm=precipitation[i],
                humidity_percent=humidity[i],
            )
            records.append(record)

        return records