from datetime import date, timedelta

from domain.entities import City, WeatherRecord
from domain.repositories import WeatherRepository


class FetchWeatherUseCase:
    def __init__(self, weather_repository: WeatherRepository) -> None:
        self._weather_repository = weather_repository

    def execute(
        self, city: City, start_date: date, end_date: date
    ) -> list[WeatherRecord]:
        """Obtiene el historial climatico de una ciudad en un rango de fechas.

        Args:
            city: Ciudad de la cual se quiere obtener el clima.
            start_date: Fecha inicial del rango (inclusive).
            end_date: Fecha final del rango (inclusive).

        Returns:
            Lista de registros climaticos ordenados por fecha.

        Raises:
            ValueError: Si start_date es posterior a end_date, o si el
                rango solicitado supera un ano.
        """
        if start_date > end_date:
            raise ValueError(
                "La fecha inicial no puede ser posterior a la fecha final"
            )

        if end_date - start_date > timedelta(days=366):
            raise ValueError(
                "El rango de fechas no puede superar un ano"
            )

        return self._weather_repository.get_weather_history(
            city=city, start_date=start_date, end_date=end_date
        )

    def execute_current(self, city: City) -> WeatherRecord:
        """Obtiene el clima actual de una ciudad.

        Args:
            city: Ciudad de la cual se quiere obtener el clima actual.

        Returns:
            Registro climatico mas reciente disponible.
        """
        return self._weather_repository.get_current_weather(city=city)
