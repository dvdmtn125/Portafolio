"""Tests para el caso de uso FetchWeatherUseCase."""

from datetime import date

import pytest

from application.use_cases.fetch_weather import FetchWeatherUseCase
from domain.entities import City, WeatherRecord
from domain.repositories import WeatherRepository


class FakeWeatherRepository(WeatherRepository):
    """Implementacion falsa de WeatherRepository para tests."""

    def __init__(self) -> None:
        self.history_calls: list[tuple[City, date, date]] = []
        self.fake_history: list[WeatherRecord] = []
        self.fake_current: WeatherRecord | None = None

    def get_weather_history(
        self, city: City, start_date: date, end_date: date
    ) -> list[WeatherRecord]:
        self.history_calls.append((city, start_date, end_date))
        return self.fake_history

    def get_current_weather(self, city: City) -> WeatherRecord:
        if self.fake_current is None:
            raise ValueError("No hay clima actual configurado en el fake")
        return self.fake_current


@pytest.fixture
def medellin() -> City:
    return City(
        name="Medellin",
        latitude=6.2442,
        longitude=-75.5812,
        department="Antioquia",
    )


@pytest.fixture
def fake_repository() -> FakeWeatherRepository:
    return FakeWeatherRepository()


@pytest.fixture
def use_case(fake_repository: FakeWeatherRepository) -> FetchWeatherUseCase:
    return FetchWeatherUseCase(weather_repository=fake_repository)


class TestFetchWeatherHistory:
    def test_obtiene_historial_correctamente(
        self,
        use_case: FetchWeatherUseCase,
        fake_repository: FakeWeatherRepository,
        medellin: City,
    ) -> None:
        expected_records = [
            WeatherRecord(
                city=medellin,
                record_date=date(2026, 1, 1),
                temperature_max=28.0,
                temperature_min=18.0,
                precipitation_mm=2.0,
                humidity_percent=65.0,
            )
        ]
        fake_repository.fake_history = expected_records

        result = use_case.execute(
            city=medellin,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 31),
        )

        assert result == expected_records

    def test_delega_correctamente_al_repositorio(
        self,
        use_case: FetchWeatherUseCase,
        fake_repository: FakeWeatherRepository,
        medellin: City,
    ) -> None:
        start = date(2026, 1, 1)
        end = date(2026, 1, 31)

        use_case.execute(city=medellin, start_date=start, end_date=end)

        assert fake_repository.history_calls == [(medellin, start, end)]

    def test_rechaza_fecha_inicial_posterior_a_final(
        self, use_case: FetchWeatherUseCase, medellin: City
    ) -> None:
        with pytest.raises(ValueError, match="no puede ser posterior"):
            use_case.execute(
                city=medellin,
                start_date=date(2026, 2, 1),
                end_date=date(2026, 1, 1),
            )

    def test_rechaza_rango_mayor_a_un_anio(
        self, use_case: FetchWeatherUseCase, medellin: City
    ) -> None:
        with pytest.raises(ValueError, match="no puede superar un ano"):
            use_case.execute(
                city=medellin,
                start_date=date(2025, 1, 1),
                end_date=date(2026, 12, 31),
            )

    def test_acepta_rango_de_exactamente_un_dia(
        self,
        use_case: FetchWeatherUseCase,
        fake_repository: FakeWeatherRepository,
        medellin: City,
    ) -> None:
        same_day = date(2026, 1, 1)

        result = use_case.execute(
            city=medellin, start_date=same_day, end_date=same_day
        )

        assert result == fake_repository.fake_history


class TestFetchCurrentWeather:
    def test_obtiene_clima_actual_correctamente(
        self,
        use_case: FetchWeatherUseCase,
        fake_repository: FakeWeatherRepository,
        medellin: City,
    ) -> None:
        expected_record = WeatherRecord(
            city=medellin,
            record_date=date(2026, 7, 5),
            temperature_max=26.0,
            temperature_min=17.0,
            precipitation_mm=0.0,
            humidity_percent=55.0,
        )
        fake_repository.fake_current = expected_record

        result = use_case.execute_current(medellin)

        assert result == expected_record

    def test_lanza_error_si_no_hay_clima_configurado(
        self, use_case: FetchWeatherUseCase, medellin: City
    ) -> None:
        with pytest.raises(ValueError, match="No hay clima actual"):
            use_case.execute_current(medellin)
