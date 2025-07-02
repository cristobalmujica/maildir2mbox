import os
import mailbox
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def validar_maildir(ruta_maildir):
    """Verifica si una ruta parece ser un directorio Maildir válido."""
    # Un Maildir válido debe contener al menos las carpetas 'cur' y 'new'.
    return os.path.isdir(os.path.join(ruta_maildir, 'cur')) and \
           os.path.isdir(os.path.join(ruta_maildir, 'new'))

def encontrar_maildirs(raiz_maildir):
    """Recorre recursivamente la estructura y retorna todas las rutas que sean Maildir válidos."""
    maildirs_encontrados = []
    for dirpath, dirnames, filenames in os.walk(raiz_maildir):
        if validar_maildir(dirpath):
            maildirs_encontrados.append(dirpath)
    return maildirs_encontrados

def convertir_maildir_a_mbox(ruta_maildir, ruta_mbox):
    """
    Convierte todos los buzones Maildir (incluyendo subcarpetas) a un único archivo MBOX.
    Añade una cabecera X-Folder con la subcarpeta de origen.

    :param ruta_maildir: La ruta al directorio Maildir.
    :param ruta_mbox: La ruta del archivo MBOX de salida.
    """
    print(f"Buscando todos los Maildir en: {ruta_maildir}")
    maildirs = encontrar_maildirs(ruta_maildir)
    print(f"Se encontraron {len(maildirs)} carpetas Maildir.")
    
    mbox_box = mailbox.mbox(ruta_mbox) # <--- LÍNEA CORREGIDA
    
    # Bloquear el archivo MBOX para evitar corrupción durante la escritura
    mbox_box.lock()
    
    contador = 0
    try:
        print("Iniciando la conversión de mensajes...")
        for maildir_path in maildirs:
            # Obtener la subcarpeta relativa
            subcarpeta = os.path.relpath(maildir_path, ruta_maildir)
            print(f"Procesando Maildir: {maildir_path} (X-Folder: {subcarpeta})")
            maildir_box = mailbox.Maildir(maildir_path, create=False)
            # Iterar sobre cada mensaje en el Maildir y agregarlo al MBOX
            for mensaje in maildir_box.itervalues():
                # Añadir cabecera X-Folder
                mensaje.add_header('X-Folder', subcarpeta)
                mbox_box.add(mensaje)
                contador += 1
        print(f"Se han procesado {contador} mensajes en total.")
    
    finally:
        # Asegurarse de desbloquear y cerrar el buzón MBOX
        mbox_box.flush()
        mbox_box.unlock()
        mbox_box.close()
        print("Buzón MBOX cerrado de forma segura.")

def convertir_maildir_a_mbox_multi(ruta_maildir, carpeta_destino):
    """
    Convierte todos los buzones Maildir (incluyendo subcarpetas) a archivos MBOX separados,
    usando como nombre la combinación de la carpeta principal y la subcarpeta.
    Todos los archivos tendrán extensión .mbox y solo se crean si hay mensajes.
    """
    nombre_principal = os.path.basename(os.path.normpath(ruta_maildir))
    print(f"Buscando todos los Maildir en: {ruta_maildir}")
    maildirs = encontrar_maildirs(ruta_maildir)
    print(f"Se encontraron {len(maildirs)} carpetas Maildir.")
    
    contador_total = 0
    for maildir_path in maildirs:
        subcarpeta = os.path.relpath(maildir_path, ruta_maildir)
        # Construir nombre: principal + _ + subcarpeta (sin puntos ni barras)
        if subcarpeta == '.' or subcarpeta == '':
            nombre = nombre_principal
        else:
            nombre_sub = subcarpeta.replace('\\', '/').replace('/', '_')
            if nombre_sub.startswith('.'):
                nombre_sub = nombre_sub[1:]
            nombre = f"{nombre_principal}_{nombre_sub}"
        mbox_filename = nombre + '.mbox'
        mbox_path = os.path.join(carpeta_destino, mbox_filename)
        os.makedirs(os.path.dirname(mbox_path), exist_ok=True)
        print(f"Preparando MBOX: {mbox_path}")
        maildir_box = mailbox.Maildir(maildir_path, create=False)
        mensajes = list(maildir_box.itervalues())
        if not mensajes:
            print(f"  Sin mensajes, no se crea: {mbox_path}")
            continue
        mbox_box = mailbox.mbox(mbox_path)
        mbox_box.lock()
        contador = 0
        try:
            for mensaje in mensajes:
                mbox_box.add(mensaje)
                contador += 1
        finally:
            mbox_box.flush()
            mbox_box.unlock()
            mbox_box.close()
        print(f"  Mensajes exportados: {contador}")
        contador_total += contador
    print(f"Se han procesado {contador_total} mensajes en total.")

def main():
    """Función principal que maneja la interacción con el usuario."""
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo(
        "Paso 1: Seleccionar Carpeta Maildir",
        "Por favor, selecciona la carpeta Maildir que deseas convertir.\n"
        "Esta carpeta debe contener las subcarpetas 'cur' y 'new'."
    )
    maildir_path = filedialog.askdirectory(title="Selecciona la carpeta Maildir de origen")
    if not maildir_path:
        print("Operación cancelada por el usuario.")
        return
    if not validar_maildir(maildir_path):
        messagebox.showerror(
            "Error de Carpeta",
            "La carpeta seleccionada no parece ser un directorio Maildir válido.\n"
            "Asegúrate de que contenga las subcarpetas 'cur' y 'new'."
        )
        print("La ruta seleccionada no es un Maildir válido.")
        return
    print(f"Carpeta Maildir seleccionada: {maildir_path}")

    messagebox.showinfo(
        "Paso 2: Seleccionar carpeta destino",
        "Ahora, elige la carpeta donde se guardarán los archivos MBOX (se replicará la estructura de carpetas)."
    )
    carpeta_destino = filedialog.askdirectory(title="Selecciona la carpeta de destino para los MBOX")
    if not carpeta_destino:
        print("Operación cancelada por el usuario.")
        return
    print(f"Carpeta de destino seleccionada: {carpeta_destino}")

    try:
        convertir_maildir_a_mbox_multi(maildir_path, carpeta_destino)
        messagebox.showinfo("Éxito", f"¡Conversión completada con éxito!\n\nLos archivos han sido guardados en:\n{carpeta_destino}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante la conversión:\n\n{e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()