from src.registro import registrar_acesso


def test_registra_un_nuevo_ingreso(tmp_path):
    """Si la persona no está en el archivo, debe agregarse una nueva línea."""
    archivo = tmp_path / "registro.csv"
    archivo.write_text("")  # archivo vacío, simula un registro nuevo

    registrar_acesso("Jerry Seinfeld", ruta_base=archivo)

    contenido = archivo.read_text()
    assert "Jerry Seinfeld" in contenido


def test_no_duplica_un_ingreso_existente(tmp_path):
    """Si la persona ya está registrada, no debe agregarse una segunda línea."""
    archivo = tmp_path / "registro.csv"
    archivo.write_text("Jerry Seinfeld, 2026-06-22 09:00:00")

    registrar_acesso("Jerry Seinfeld", ruta_base=archivo)

    contenido = archivo.read_text()
    # El nombre debe aparecer solo una vez, no dos
    assert contenido.count("Jerry Seinfeld") == 1


def test_registra_a_varias_personas_distintas(tmp_path):
    """Dos personas distintas deben poder registrarse ambas en el mismo archivo."""
    archivo = tmp_path / "registro.csv"
    archivo.write_text("")

    registrar_acesso("Jerry Seinfeld", ruta_base=archivo)
    registrar_acesso("Elaine Benes", ruta_base=archivo)

    contenido = archivo.read_text()
    assert "Jerry Seinfeld" in contenido
    assert "Elaine Benes" in contenido


def test_guarda_la_hora_en_el_formato_esperado(tmp_path):
    """La línea registrada debe incluir una fecha/hora con el formato
    YYYY-MM-DD HH:MM:SS."""
    import re

    archivo = tmp_path / "registro.csv"
    archivo.write_text("")

    registrar_acesso("Cosmo Kramer", ruta_base=archivo)

    contenido = archivo.read_text()
    patron = r"Cosmo Kramer,\s*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    assert re.search(patron, contenido)