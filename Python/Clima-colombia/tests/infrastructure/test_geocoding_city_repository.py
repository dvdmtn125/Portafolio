"""Tests para GeocodingCityRepository usando pytest-mock (sin llamadas reales)."""

import pytest
import requests

from infrastructure.geocoding_city_repository import GeocodingCityRepository


@pytest.fixture
def repository() -> GeocodingCityRepository:
    return GeocodingCityRepository()


def _build_fake_response(mocker, json_data: dict, status_ok: bool = True):
    """Crea un objeto de respuesta falso que imita requests.Response."""
    fake_response = mocker.Mock()
    fake_response.json.return_value = json_data
    if status_ok:
        fake_response.raise_for_status.return_value = None
    else:
        fake_response.raise_for_status.side_effect = requests.HTTPError(
            "500 Server Error"
        )
    return fake_response


class TestGetCityByName:
    def test_encuentra_ciudad_correctamente(
        self, mocker, repository: GeocodingCityRepository
    ) -> None:
        fake_json = {
            "results": [
                {
                    "name": "Medellin",
                    "latitude": 6.2442,
                    "longitude": -75.5812,
                    "admin1": "Antioquia",
                    "country_code": "CO",
                }
            ]
        }
        fake_response = _build_fake_response(mocker, fake_json)
        mocker.patch(
            "infrastructure.geocoding_city_repository.requests.get",
            return_value=fake_response,
        )

        city = repository.get_city_by_name("Medellin")

        assert city is not None
        assert city.name == "Medellin"
        assert city.latitude == 6.2442
        assert city.longitude == -75.5812
        assert city.department == "Antioquia"

    def test_retorna_none_si_no_hay_resultados(
        self, mocker, repository: GeocodingCityRepository
    ) -> None:
        fake_response = _build_fake_response(mocker, {"results": []})
        mocker.patch(
            "infrastructure.geocoding_city_repository.requests.get",
            return_value=fake_response,
        )

        city = repository.get_city_by_name("CiudadQueNoExiste")

        assert city is None

    def test_retorna_none_si_falta_la_clave_results(
        self, mocker, repository: GeocodingCityRepository
    ) -> None:
        fake_response = _build_fake_response(mocker, {})
        mocker.patch(
            "infrastructure.geocoding_city_repository.requests.get",
            return_value=fake_response,
        )

        city = repository.get_city_by_name("Medellin")

        assert city is None

    def test_filtra_resultados_de_otros_paises(
        self, mocker, repository: GeocodingCityRepository
    ) -> None:
        """Ciudades homonimas en otros paises deben ser descartadas,
        incluso si la API las devuelve primero (ej. Madrid, Espana)."""
        fake_json = {
            "results": [
                {
                    "name": "Madrid",
                    "latitude": 40.4168,
                    "longitude": -3.7038,
                    "admin1": "Comunidad de Madrid",
                    "country_code": "ES",
                },
                {
                    "name": "Madrid",
                    "latitude": 4.7328,
                    "longitude": -74.2643,
                    "admin1": "Cundinamarca",
                    "country_code": "CO",
                },
            ]
        }
        fake_response = _build_fake_response(mocker, fake_json)
        mocker.patch(
            "infrastructure.geocoding_city_repository.requests.get",
            return_value=fake_response,
        )

        city = repository.get_city_by_name("Madrid")

        assert city is not None
        assert city.department == "Cundinamarca"

    def test_retorna_none_si_ningun_resultado_es_de_colombia(
        self, mocker, repository: GeocodingCityRepository
    ) -> None:
        fake_json = {
            "results": [
                {
                    "name": "Pekin",
                    "latitude": 39.9042,
                    "longitude": 116.4074,
                    "admin1": "Beijing",
                    "country_code": "CN",
                }
            ]
        }
        fake_response = _build_fake_response(mocker, fake_json)
        mocker.patch(
            "infrastructure.geocoding_city_repository.requests.get",
            return_value=fake_response,
        )

        city = repository.get_city_by_name("Pekin")

        assert city is None

    def test_toma_el_primer_resultado_colombiano_cuando_hay_varios(
        self, mocker, repository: GeocodingCityRepository
    ) -> None:
        fake_json = {
            "results": [
                {
                    "name": "Santa Rosa",
                    "latitude": 1.0,
                    "longitude": 2.0,
                    "admin1": "Bolivar",
                    "country_code": "CO",
                },
                {
                    "name": "Santa Rosa",
                    "latitude": 3.0,
                    "longitude": 4.0,
                    "admin1": "Cauca",
                    "country_code": "CO",
                },
            ]
        }
        fake_response = _build_fake_response(mocker, fake_json)
        mocker.patch(
            "infrastructure.geocoding_city_repository.requests.get",
            return_value=fake_response,
        )

        city = repository.get_city_by_name("Santa Rosa")

        assert city is not None
        assert city.department == "Bolivar"

    def test_usa_desconocido_si_falta_admin1(
        self, mocker, repository: GeocodingCityRepository
    ) -> None:
        fake_json = {
            "results": [
                {
                    "name": "Ciudad Sin Departamento",
                    "latitude": 1.0,
                    "longitude": 2.0,
                    "country_code": "CO",
                }
            ]
        }
        fake_response = _build_fake_response(mocker, fake_json)
        mocker.patch(
            "infrastructure.geocoding_city_repository.requests.get",
            return_value=fake_response,
        )

        city = repository.get_city_by_name("Ciudad Sin Departamento")

        assert city is not None
        assert city.department == "Desconocido"

    def test_envia_parametros_correctos_a_la_api(
        self, mocker, repository: GeocodingCityRepository
    ) -> None:
        fake_response = _build_fake_response(mocker, {"results": []})
        mock_get = mocker.patch(
            "infrastructure.geocoding_city_repository.requests.get",
            return_value=fake_response,
        )

        repository.get_city_by_name("Bucaramanga")

        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["params"]["name"] == "Bucaramanga"

    def test_propaga_error_http(
        self, mocker, repository: GeocodingCityRepository
    ) -> None:
        fake_response = _build_fake_response(mocker, {}, status_ok=False)
        mocker.patch(
            "infrastructure.geocoding_city_repository.requests.get",
            return_value=fake_response,
        )

        with pytest.raises(requests.HTTPError):
            repository.get_city_by_name("Medellin")


class TestGetAllCities:
    def test_lanza_not_implemented_error(
        self, repository: GeocodingCityRepository
    ) -> None:
        with pytest.raises(NotImplementedError, match="catalogo fijo"):
            repository.get_all_cities()
