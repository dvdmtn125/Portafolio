from datetime import date

import pytest

from domain.entities import City, WeatherRecord
from interface.cli import parse_date_arg, run_actual, run_historial


@pytest.fixture
def medellin() -> City:
    return City(
        name="Medellin",
        latitude=6.2442,
        longitude=75.5812,
        department="Antioquia",
    )


class TestParseDateArg:
    def test_convierte_fecha_valida(self) -> None:
        result = parse_date_arg("2026-01-15", "--desde")
        assert result == date(2026, 1, 15)

    def test_sale_con_error_si_formato_invalido(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            parse_date_arg("15/01/2026", "--desde")
        assert exc_info.value.code == 1


class TestRunActual:
    def test_muestra_clima_actual_correctamente(
            self, mocker, capsys, medellin: City
    ) -> None:
        fake_record = WeatherRecord(
            city=medellin,
            record_date=date(2026, 7, 5),
            temperature_max=26.0,
            temperature_min=17.0,
            precipitation_mm=0.0,
            humidity_percent=55.0,
        )

        mock_city_repo = mocker.Mock()
        mock_city_repo.get_city_by_name.return_value = medellin
        mocker.patch(
            "interface.cli.GeocodingCityRepository",
            return_value=mock_city_repo
        )
        mock_use_case = mocker.Mock()
        mock_use_case.execute_current.return_value = fake_record
        mocker.patch(
            "interface.cli.FetchWeatherUseCase",
            return_value=mock_use_case
        )
        mocker.patch("interface.cli.OpenMeteoClient")

        run_actual("Medellin")

        captured = capsys.readouterr()
        assert "Medellin" in captured.out
        assert "26.0" in captured.out
        assert "55.0" in captured.out

    def test_sale_con_error_si_ciudad_no_encontrada(
            self, mocker, capsys
    ) -> None:
        mock_city_repo = mocker.Mock()
        mock_city_repo.get_city_by_name.return_value = None
        mocker.patch(
            "interface.cli.GeocodingCityRepository",
            return_value=mock_city_repo,
        )
        mocker.patch("interface.cli.FetchWeatherUseCase")
        mocker.patch("interface.cli.OpenMeteoClient")

        with pytest.raises(SystemExit) as exc_info:
            run_actual("CiudadInventada")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "no se encontro la ciudad" in captured.err


class TestRunHistorial:
    def test_muestra_historial_correctamente(
            self, mocker, capsys, medellin: City
    ) -> None:
        fake_records = [
            WeatherRecord(
                city=medellin,
                record_date=date(2026, 1, 1),
                temperature_max=28.0,
                temperature_min=18.0,
                precipitation_mm=2.0,
                humidity_percent=65.0,
            ),
            WeatherRecord(
                city=medellin,
                record_date=date(2026, 1, 2),
                temperature_max=29.0,
                temperature_min=19.0,
                precipitation_mm=0.0,
                humidity_percent=60.0,
            ),
        ]

        mock_city_repo = mocker.Mock()
        mock_city_repo.get_city_by_name.return_value = medellin
        mocker.patch(
            "interface.cli.GeocodingCityRepository",
            return_value=mock_city_repo,
        )

        mock_use_case = mocker.Mock()
        mock_use_case.execute.return_value = fake_records
        mocker.patch(
            "interface.cli.FetchWeatherUseCase", return_value=mock_use_case
        )
        mocker.patch("interface.cli.OpenMeteoClient")

        run_historial("Medellin", "2026-01-01", "2026-01-02")

        captured = capsys.readouterr()
        assert "2026-01-01" in captured.out
        assert "2026-01-02" in captured.out
        assert "28.0" in captured.out

    def test_sale_con_error_si_ciudad_no_encontrada(
            self, mocker, capsys
    ) -> None:
        mock_city_repo = mocker.Mock()
        mock_city_repo.get_city_by_name.return_value = None
        mocker.patch(
            "interface.cli.GeocodingCityRepository",
            return_value=mock_city_repo,
        )
        mocker.patch("interface.cli.FetchWeatherUseCase")
        mocker.patch("interface.cli.OpenMeteoClient")

        with pytest.raises(SystemExit) as exc_info:
            run_historial("CiudadInventada", "2026-01-01", "2026-01-31")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "no se encontro la ciudad" in captured.err

    def test_sale_con_error_si_rango_de_fechas_invalido(
            self, mocker, capsys, medellin: City
    ) -> None:
        mock_city_repo = mocker.Mock()
        mock_city_repo.get_city_by_name.return_value = medellin
        mocker.patch(
            "interface.cli.GeocodingCityRepository",
            return_value=mock_city_repo,
        )

        mock_use_case = mocker.Mock()
        mock_use_case.execute.side_effect = ValueError(
            "La fecha inicial no puede ser posterior a la fecha final"
        )
        mocker.patch(
            "interface.cli.FetchWeatherUseCase", return_value=mock_use_case
        )
        mocker.patch("interface.cli.OpenMeteoClient")

        with pytest.raises(SystemExit) as exc_info:
            run_historial("Medellin", "2026-02-01", "2026-01-01")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "no puede ser posterior" in captured.err

    def test_sale_con_error_si_fecha_mal_formateada(
            self, mocker, capsys, medellin: City
    ) -> None:
        mock_city_repo = mocker.Mock()
        mock_city_repo.get_city_by_name.return_value = medellin
        mocker.patch(
            "interface.cli.GeocodingCityRepository",
            return_value=mock_city_repo,
        )
        mocker.patch("interface.cli.FetchWeatherUseCase")
        mocker.patch("interface.cli.OpenMeteoClient")

        with pytest.raises(SystemExit) as exc_info:
            run_historial("Medellin", "01-01-2026", "2026-01-31")

        assert exc_info.value.code == 1