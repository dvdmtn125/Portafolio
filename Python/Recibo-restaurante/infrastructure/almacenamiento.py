from tkinter import filedialog

def guardar_recibo(contenido, abrir_dialogo=None):
    if abrir_dialogo is None:
        abrir_dialogo = lambda: filedialog.asksaveasfile(
            mode='w', 
            defaultextension='.txt',
            filetypes=[('Archivo de texto', '*.txt'), ('Todos los archivos', '*.*')],
            )


    archivo = abrir_dialogo()

    if archivo is None:
        return False
    
    try:
        archivo.write(contenido)
    finally:
        archivo.close()

    return True