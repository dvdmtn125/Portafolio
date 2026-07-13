"""Tests para las entidades del dominio: City y WeatherRecord."""

from datetime import date

import pytest

from domain.entities import City, WeatherRecord


@pytest.fixture
def medellin() -> City:
    return City(
        name="Medellin",
        latitude=6.2442,
        longitude=-75.5812,
        department="Antioquia",
    )


class TestCity:
    def test_crea_ciudad_valida(self, medellin: City) -> None:
        assert medellin.name == "Medellin"
        assert medellin.department == "Antioquia"

    def test_es_inmutable(self, medellin: City) -> None:
        with pytest.raises(AttributeError):
            medellin.name = "Bogota"

    @pytest.mark.parametrize("latitud_invalida", [91, -91, 180, -200])
    def test_rechaza_latitud_invalida(self, latitud_invalida: float) -> None:
        with pytest.raises(ValueError, match="Latitud invalida"):
            City(
                name="Ciudad Test",
                latitude=latitud_invalida,
                longitude=0,
                department="Test",
            )

    @pytest.mark.parametrize("longitud_invalida", [181, -181, 360])
    def test_rechaza_longitud_invalida(self, longitud_invalida: float) -> None:
        with pytest.raises(ValueError, match="Longitud invalida"):
            City(
                name="Ciudad Test",
                latitude=0,
                longitude=longitud_invalida,
                department="Test",
            )

    def test_rechaza_nombre_vacio(self) -> None:
        with pytest.raises(ValueError, match="nombre de la ciudad"):
            City(name="   ", latitude=0, longitude=0, department="Test")


class TestWeatherRecord:
    def test_crea_registro_valido(self, medellin: City) -> None:
        record = WeatherRecord(
            city=medellin,
            record_date=date(2026, 1, 15),
            temperature_max=28.0,
            temperature_min=18.0,
            precipitation_mm=5.5,
            humidity_percent=70.0,
        )
        assert record.city == medellin
        assert record.temperature_max == 28.0

    def test_calcula_temperatura_promedio(self, medellin: City) -> None:
        record = WeatherRecord(
            city=medellin,
            record_date=date(2026, 1, 15),
            temperature_max=30.0,
            temperature_min=20.0,
            precipitation_mm=0,
            humidity_percent=60.0,
        )
        assert record.temperature_avg == 25.0

    def test_rechaza_temp_min_mayor_a_max(self, medellin: City) -> None:
        with pytest.raises(ValueError, match="minima no puede ser mayor"):
            WeatherRecord(
                city=medellin,
                record_date=date(2026, 1, 15),
                temperature_max=15.0,
                temperature_min=20.0,
                precipitation_mm=0,
                humidity_percent=50.0,
            )

    def test_rechaza_precipitacion_negativa(self, medellin: City) -> None:
        with pytest.raises(ValueError, match="precipitacion no puede ser negativa"):
            WeatherRecord(
                city=medellin,
                record_date=date(2026, 1, 15),
                temperature_max=25.0,
                temperature_min=15.0,
                precipitation_mm=-1.0,
                humidity_percent=50.0,
            )

    @pytest.mark.parametrize("humedad_invalida", [-1, 101, 150])
    def test_rechaza_humedad_invalida(
        self, medellin: City, humedad_invalida: float
    ) -> None:
        with pytest.raises(ValueError, match="Humedad invalida"):
            WeatherRecord(
                city=medellin,
                record_date=date(2026, 1, 15),
                temperature_max=25.0,
                temperature_min=15.0,
                precipitation_mm=0,
                humidity_percent=humedad_invalida,
            )
