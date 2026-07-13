from datetime import date

import pytest
import requests

from domain.entities import City
from infrastructure.open_meteo_client import OpenMeteoClient


@pytest.fixture
def medellin() -> City:
    return City(name="Medellín", latitude=6.2442, longitude=-75.5812, department="Antioquia")

@pytest.fixture
def client() -> OpenMeteoClient:
    return OpenMeteoClient()


def _build_fake_response(mocker, json_data: dict, status_ok: bool = True):
    fake_response = mocker.Mock()
    fake_response.json.return_value = json_data
    if status_ok:
        fake_response.raise_for_status.return_value = None
    else:
        fake_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error: Internal Server Error for url")
    return fake_response

class TestGetWeatherHistory:
    def test_convierte_respuesta_json_en_weather_records(
            self, mocker, client: OpenMeteoClient, medellin: City
    ) -> None:
        fake_json = {
            "daily": {
                "time": ["2026-01-01", "2026-01-02"],
                "temperature_2m_max": [28.0, 29.5],
                "temperature_2m_min": [18.0, 19.0],
                "precipitation_sum": [2.0, 0.0],
                "relative_humidity_2m_mean": [65.0, 60.0],
            }
        }
        fake_response = _build_fake_response(mocker, fake_json)
        mock_get = mocker.patch(
            "infrastructure.open_meteo_client.requests.get", 
            return_value=fake_response,
        )

        result = client.get_weather_history(
            city=medellin,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 2),
        )

        assert len(result) == 2
        assert result[0].record_date == date(2026, 1, 1)
        assert result[0].temperature_max == 28.0
        assert result[1].temperature_min == 19.0
        mock_get.assert_called_once()

    def test_envia_parametros_correctos_a_la_api(
            self, mocker, client: OpenMeteoClient, medellin: City
    ) -> None:
        fake_response = _build_fake_response(mocker, {"daily": {}})
        mock_get = mocker.patch(
            "infrastructure.open_meteo_client.requests.get",
            return_value=fake_response,
        )

        client.get_weather_history(
            city=medellin,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 31),
        )

        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["params"]["latitude"] == medellin.latitude
        assert call_kwargs["params"]["longitude"] == medellin.longitude
        assert call_kwargs["params"]["start_date"] == "2026-01-01"
        assert call_kwargs["params"]["end_date"] == "2026-01-31"

    def test_propaga_error_http(
            self, mocker, client: OpenMeteoClient, medellin: City
    ) -> None:
        fake_response = _build_fake_response(mocker, {}, status_ok=False)
        mocker.patch(
            "infrastructure.open_meteo_client.requests.get",
            return_value=fake_response,
        )

        with pytest.raises(requests.HTTPError):
            client.get_weather_history(
                city=medellin,
                start_date=date(2026, 1, 1),
                end_date=date(2026, 1, 2),
            )


class TestGetCurrentWeather:
    def test_obtiene_clima_actual_correctamente(
            self, mocker, client: OpenMeteoClient, medellin: City
    ) -> None:
        fake_json = {
            "daily": {
                "time": ["2026-07-05"],
                "temperature_2m_max": [26.0],
                "temperature_2m_min": [17.0],
                "precipitation_sum": [0.0],
                "relative_humidity_2m_mean": [55.0]
            }
        }
        fake_response = _build_fake_response(mocker, fake_json)
        mocker.patch(
            "infrastructure.open_meteo_client.requests.get",
            return_value=fake_response,
        )

        result = client.get_current_weather(medellin)

        assert result.record_date == date(2026, 7, 5)
        assert result.temperature_max == 26.0

    def test_lanza_error_si_no_hay_datos(
            self, mocker, client: OpenMeteoClient, medellin: City
    ) -> None:
        fake_response = _build_fake_response(mocker, {"daily": {"time": []}})
        mocker.patch(
            "infrastructure.open_meteo_client.requests.get",
            return_value=fake_response,
        )

        with pytest.raises(ValueError, match="no devolvio datos"):
            client.get_current_weather(medellin)