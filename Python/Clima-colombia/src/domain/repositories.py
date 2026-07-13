from abc import ABC, abstractmethod
from datetime import date

from domain.entities import City, WeatherRecord

class WeatherRepository(ABC):
    @abstractmethod
    def get_weather_history(self, city: City, start_date: date, end_date: date) -> list[WeatherRecord]:
        """
        Args: 
            city: Ciudad de la cual se desea obtener el historial meteorológico.
            start_date: Fecha inicial del rango (inclusive).
            end_date: Fecha final del rango (inclusive).
        
        Returns:
            Una lista de registros meteorológicos (WeatherRecord) para la ciudad y rango de fechas especificados.

        Raises:
            ValueError: Si la start_date es posterior a la end_date.
        """

        Raises: NotImplementedError

    @abstractmethod
    def get_current_weather(self, city: City) -> WeatherRecord:
        """
        Args:
            city: Ciudad de la cual se desea obtener el clima actual.
        
        Returns:
            Un registro meteorológico que representa el clima actual de la ciudad especificada.
        """

        Raises: NotImplementedError

class CityRepository(ABC):
    @abstractmethod
    def get_all_cities(self) -> list[City]:
        
        Raises: NotImplementedError

    @abstractmethod
    def get_city_by_name(self, name: str) -> City:
        """
        Args:
            name: Nombre de la ciudad (case-insensitive).
        
        Returns:
            La ciudad correspondiente al nombre especificado.

        Raises:
            ValueError: Si no se encuentra ninguna ciudad con el nombre proporcionado.
        """

        Raises: NotImplementedError

