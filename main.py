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

def convertir_maildir_a_mbox(ruta_maildir, ruta_mbox):
    """
    Convierte un buzón de correo en formato Maildir a formato MBOX.

    :param ruta_maildir: La ruta al directorio Maildir.
    :param ruta_mbox: La ruta del archivo MBOX de salida.
    """
    print(f"Abriendo el buzón Maildir en: {ruta_maildir}")
    # Acceder al buzón Maildir de origen
    maildir_box = mailbox.Maildir(ruta_maildir, create=False)
    
    print(f"Creando el archivo MBOX en: {ruta_mbox}")
    # Crear el buzón MBOX de destino
    mbox_box = mailbox.mbox(ruta_mbox) # <--- LÍNEA CORREGIDA
    
    # Bloquear el archivo MBOX para evitar corrupción durante la escritura
    mbox_box.lock()
    
    contador = 0
    try:
        print("Iniciando la conversión de mensajes...")
        # Iterar sobre cada mensaje en el Maildir y agregarlo al MBOX
        for mensaje in maildir_box.itervalues():
            mbox_box.add(mensaje)
            contador += 1
        print(f"Se han procesado {contador} mensajes.")
    
    finally:
        # Asegurarse de desbloquear y cerrar el buzón MBOX
        mbox_box.flush()
        mbox_box.unlock()
        mbox_box.close()
        print("Buzón MBOX cerrado de forma segura.")

def main():
    """Función principal que maneja la interacción con el usuario."""
    # Oculta la ventana principal de tkinter
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo(
        "Paso 1: Seleccionar Carpeta Maildir",
        "Por favor, selecciona la carpeta Maildir que deseas convertir.\n"
        "Esta carpeta debe contener las subcarpetas 'cur' y 'new'."
    )
    
    # Abrir el diálogo para seleccionar la carpeta Maildir de origen
    maildir_path = filedialog.askdirectory(title="Selecciona la carpeta Maildir de origen")
    
    if not maildir_path:
        print("Operación cancelada por el usuario.")
        return

    # Validar que la carpeta seleccionada es un Maildir
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
        "Paso 2: Guardar como MBOX",
        "Ahora, elige la ubicación y el nombre para el nuevo archivo MBOX."
    )

    # Abrir el diálogo para guardar el archivo MBOX de destino
    mbox_path = filedialog.asksaveasfilename(
        title="Guardar archivo como MBOX",
        defaultextension=".mbox",
        filetypes=[("Archivos MBOX", "*.mbox"), ("Todos los archivos", "*.*")]
    )
    
    if not mbox_path:
        print("Operación cancelada por el usuario.")
        return
        
    print(f"Archivo MBOX de destino: {mbox_path}")

    try:
        convertir_maildir_a_mbox(maildir_path, mbox_path)
        messagebox.showinfo("Éxito", f"¡Conversión completada con éxito!\n\nEl archivo ha sido guardado en:\n{mbox_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante la conversión:\n\n{e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()