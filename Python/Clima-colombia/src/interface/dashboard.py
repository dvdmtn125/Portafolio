import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from application.use_cases.fetch_weather import FetchWeatherUseCase
from infrastructure.geocoding_city_repository import GeocodingCityRepository
from infrastructure.open_meteo_client import OpenMeteoClient


@st.cache_resource
def get_use_case() -> FetchWeatherUseCase:
    weather_client = OpenMeteoClient()
    return FetchWeatherUseCase(weather_repository=weather_client)


@st.cache_resource
def get_city_repository() -> GeocodingCityRepository:
    return GeocodingCityRepository()


def render_header() -> None:
    st.set_page_config(page_title="Clima Colombia", page_icon="climate_icon.png")
    st.title("Clima Colombia")
    st.caption(
        "Consulta el clima actual e historico de cualquier ciudad colombiana, "
        "usando datos abiertos de Open-Meteo."
    )


def render_city_search() -> "City | None":
    city_repository = get_city_repository()

    city_name = st.text_input(
        "Ciudad", placeholder="Ej. Medellin, Bogota, Cartagena..."
    )

    if not city_name:
        st.info("Escribe el nombre de una ciudad colombiana para comenzar.")
        return None
    
    with st.spinner(f"Buscando'{city_name}'..."):
        try:
            city = city_repository.get_city_by_name(city_name)
        except Exception as error:
            st.error(f"Error al buscar la ciudad: {error}")
            return None
        
    if city is None:
        st.warning(f"No se encontro la ciudad '{city_name}' en Colombia.")
        return None
    
    st.success(f"Ciudad encontrada: {city.name} ({city.department})")
    return city


def render_current_weather(city) -> None:
    use_case = get_use_case()

    with st.spinner("Consultando clima actual..."):
        try:
            record = use_case.execute_current(city)
        except Exception as error:
            st.error(f"Error al obtener el clima actual: {error}")
            return
    
    st.subheader("Clima actual")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Temp. maxima", f"{record.temperature_max:.1f}°C")
    col2.metric("Temp. minima", f"{record.temperature_min:.1f}°C")
    col1.metric("Precipitacion", f"{record.precipitation_mm:.1f} mm")
    col1.metric("Humedad", f"{record.humidity_percent:.0f}%")


def render_historical_chart(city) -> None:
    use_case = get_use_case()

    st.subheader("Historial climatico")

    col1, col2 = st.columns(2)
    default_start = date.today() - timedelta(days=30)
    default_end = date.today() - timedelta(days=1)

    start_date = col1.date_input(
        "Desde", value=default_start, max_value=date.today()
    )
    end_date = col2.date_input(
        "Hasta", value=default_end, max_value=date.today()
    )

    if start_date > end_date:
        st.error("La fecha inicial no puede ser posterior a la fecha final.")
        return

    with st.spinner("Consultando historial climatico..."):
        try:
            records = use_case.execute(
                city=city, start_date=start_date, end_date=end_date
            )
        except ValueError as error:
            st.error(f"Error: {error}")
            return
        except Exception as error:
            st.error(f"Error al obtener el historial: {error}")
            return
        
    if not records:
        st.info("No hay datos disponibles para ese rango de fechas.")
        return
    
    chart_data = {
        "Fecha": [r.record_date for r in records],
        "Temp. maxima": [r.temperature_max for r in records],
        "Temp. minima": [r.temperature_min for r in records],
    }
    st.line_chart(chart_data, x="Fecha", y=["Temp. maxima", "Temp. minima"])

    precipitation_data = {
        "Fecha": [r.record_date for r in records],
        "Precipitacion (mm)": [r.precipitation_mm for r in records],
    }
    st.bar_chart(precipitation_data, x="Fecha", y="Precipitacion (mm)")

    with st.expander("Ver datos en tabla"):
        st.dataframe(
            {
                "Fecha": [r.record_date.isoformat() for r in records],
                "Max (°C)": [r.temperature_max for r in records],
                "Min (°C)": [r.temperature_min for r in records],
                "Precipitacion (mm)": [r.precipitation_mm for r in records],
                "Humedad (%)": [r.humidity_percent for r in records],
            },
            hide_index=True
        )


def main() -> None:
    render_header()
    city = render_city_search()

    if city is not None:
        render_current_weather(city)
        render_historical_chart(city)



if __name__ == "__main__":
    main()