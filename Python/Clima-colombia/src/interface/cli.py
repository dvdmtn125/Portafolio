import argparse
import sys
from datetime import date, datetime

from application.use_cases.fetch_weather import FetchWeatherUseCase
from infrastructure.geocoding_city_repository import GeocodingCityRepository
from infrastructure.open_meteo_client import OpenMeteoClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="clima-colombia",
        description="Consulta datos climaticos de ciudades colombianas.",
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    parser_actual = subparsers.add_parser(
        "actual", help="Consulta el clima actual de una ciudad"
    )
    parser_actual.add_argument(
        "--ciudad", required=True, help="Nombre de la ciudad (ej. Medellin)"
    )

    parser_historial = subparsers.add_parser(
        "historial", help="Consulta el historial climatico de una ciudad"
    )
    parser_historial.add_argument(
        "--ciudad", required=True, help="Nombre de la ciudad (ej. Medellin)"
    )
    parser_historial.add_argument(
        "--desde",
        required=True,
        help="Fecha inicial en formato YYYY-MM-DD",
    )
    parser_historial.add_argument(
        "--hasta",
        required=True,
        help="Fecha final en formato YYYY-MM-DD",
    )

    return parser


def parse_date_arg(value: str, field_name: str) -> date:
    """
    Args:
        value: Fecha en formato texto.
        field_name: Nombre de argumento (para el mensaje error).

    Returns:
        objeto date correspondiente.
    """
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        print(
            f"Error: '{field_name}' debe tener formato YYYY-MM-DD "
            f"(recibido: '{value}')",
            file=sys.stderr,
        )
        sys.exit(1)

def run_actual(ciudad_nombre: str) -> None:
    city_repository = GeocodingCityRepository()
    weather_client = OpenMeteoClient()
    use_case = FetchWeatherUseCase(weather_repository=weather_client)

    city = city_repository.get_city_by_name(ciudad_nombre)
    if city is None:
        print(
            f"Error: no se encontro la ciudad '{ciudad_nombre}' en Colombia",
            file=sys.stderr,
        )
        sys.exit(1)

    record = use_case.execute_current(city)

    print(f"\nClima actual en {city.name} ({city.department}):")
    print(f"  Temperatura maxima: {record.temperature_max}°C")
    print(f"  Temperatura minima: {record.temperature_min}°C")
    print(f"  Temperatura promedio: {record.temperature_avg:.1f}°C")
    print(f"  Precipitacion: {record.precipitation_mm} mm")
    print(f"  Humedad: {record.humidity_percent}%\n")

def run_historial(ciudad_nombre: str, desde: str, hasta: str) -> None:
    city_repository = GeocodingCityRepository()
    weather_client = OpenMeteoClient()
    use_case = FetchWeatherUseCase(weather_repository=weather_client)

    city = city_repository.get_city_by_name(ciudad_nombre)
    if city is None:
        print(
            f"Error: no se encontro la ciudad '{ciudad_nombre}' en Colombia",
            file=sys.stderr,
        )
        sys.exit(1)

    start_date = parse_date_arg(desde, "--desde")
    end_date = parse_date_arg(hasta, "--hasta")

    try:
        records = use_case.execute(
            city=city, start_date=start_date, end_date=end_date
        )
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    print(f"\nHistorial climatico de {city.name} ({city.department}):")
    print(f"{'Fecha':<12} {'Max':>6} {'Min':>6} {'Prec(mm)':>10} {'Hum(%)':>8}")
    print("-" * 46)
    for record in records:
        print(
            f"{record.record_date.isoformat():<12} "
            f"{record.temperature_max:>6.1f} "
            f"{record.temperature_min:>6.1f} "
            f"{record.precipitation_mm:>10.1f} "
            f"{record.humidity_percent:>8.1f}"
        )
    print()

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.comando == "actual":
            run_actual(args.ciudad)
        elif args.comando == "historial":
            run_historial(args.ciudad, args.desde, args.hasta)
    except Exception as error:
        print(f"Error inesperado: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()