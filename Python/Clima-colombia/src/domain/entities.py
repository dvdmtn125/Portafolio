"""Entidades del dominio: representan los conceptos centrales del negocio,
sin conocimiento de infraestructura (APIs, bases de datos, etc.)."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class City:
    """Representa una ciudad colombiana con sus coordenadas geograficas."""

    name: str
    latitude: float
    longitude: float
    department: str

    def __post_init__(self) -> None:
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Latitud invalida: {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Longitud invalida: {self.longitude}")
        if not self.name.strip():
            raise ValueError("El nombre de la ciudad no puede estar vacio")


@dataclass(frozen=True)
class WeatherRecord:
    """Representa una medicion climatica de una ciudad en una fecha especifica."""

    city: City
    record_date: date
    temperature_max: float
    temperature_min: float
    precipitation_mm: float
    humidity_percent: float

    def __post_init__(self) -> None:
        if self.temperature_min > self.temperature_max:
            raise ValueError(
                "La temperatura minima no puede ser mayor que la maxima"
            )
        if self.precipitation_mm < 0:
            raise ValueError("La precipitacion no puede ser negativa")
        if not 0 <= self.humidity_percent <= 100:
            raise ValueError(f"Humedad invalida: {self.humidity_percent}")

    @property
    def temperature_avg(self) -> float:
        """Temperatura promedio del dia."""
        return (self.temperature_max + self.temperature_min) / 2
