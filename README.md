# maildir2mbox

Este proyecto es una herramienta en Python que permite convertir buzones de correo en formato Maildir (incluyendo todas sus subcarpetas) a archivos MBOX, facilitando la migración de correos electrónicos entre diferentes clientes de correo, como Thunderbird y Microsoft Outlook (vía herramientas intermedias).

## Características principales

- **Conversión recursiva:** Recorre toda la estructura de carpetas Maildir, detectando todas las subcarpetas válidas (que contienen `cur` y `new`).
- **Exportación múltiple:** Genera un archivo `.mbox` por cada carpeta Maildir encontrada, usando como nombre la combinación de la carpeta principal y la subcarpeta.
- **Compatibilidad con Thunderbird:** Los archivos `.mbox` generados pueden ser importados directamente en Thunderbird usando complementos como ImportExportTools NG.
- **Evita archivos vacíos:** Solo se crean archivos `.mbox` si la carpeta contiene mensajes.
- **Interfaz gráfica simple:** Utiliza `tkinter` para seleccionar carpetas de origen y destino de manera visual.

## ¿Qué es Maildir y MBOX?

- **Maildir:** Es un formato de almacenamiento de correo donde cada mensaje es un archivo individual, y las carpetas de correo son directorios con subdirectorios `cur`, `new` y `tmp`.
- **MBOX:** Es un formato donde todos los mensajes de una carpeta se almacenan en un solo archivo de texto plano, ampliamente soportado por clientes de correo.

## ¿Para qué sirve este proyecto?

- Migrar correos de servidores Linux, Zimbra, Dovecot, Postfix, etc. (que usan Maildir) a clientes de escritorio como Thunderbird o, indirectamente, a Outlook.
- Realizar respaldos de buzones Maildir en formato MBOX.
- Unificar y organizar correos dispersos en múltiples subcarpetas.

## ¿Cómo funciona?

1. **Ejecución:** Al ejecutar el script, se abre una ventana para seleccionar la carpeta Maildir de origen.
2. **Validación:** El programa verifica que la carpeta seleccionada sea un Maildir válido.
3. **Selección de destino:** Se solicita una carpeta donde se guardarán los archivos `.mbox` generados.
4. **Conversión:** El script recorre todas las subcarpetas Maildir, exportando cada una a un archivo `.mbox` con nombre descriptivo.
5. **Finalización:** Se muestra un mensaje de éxito y la ruta donde se guardaron los archivos.

## Ejemplo de nombres generados

Si la carpeta principal es `CMM` y tiene subcarpetas `.Sent`, `.Archive`, etc., los archivos generados serán:

- `CMM.mbox` (correos de la raíz)
- `CMM_Sent.mbox` (correos de la subcarpeta Sent)
- `CMM_Archive.mbox` (correos de la subcarpeta Archive)

## Requisitos

- Python 3.x
- Bibliotecas estándar: `os`, `mailbox`, `tkinter`

## Uso

1. Descarga o clona este repositorio.
2. Ejecuta el script principal:
   ```bash
   python main.py
   ```
3. Selecciona la carpeta Maildir de origen cuando se te solicite.
4. Selecciona la carpeta de destino para los archivos `.mbox`.
5. Espera a que finalice la conversión. Los archivos `.mbox` estarán listos para importar en Thunderbird.

## Importar en Thunderbird

1. Instala el complemento [ImportExportTools NG](https://addons.thunderbird.net/es/thunderbird/addon/importexporttools-ng/).
2. Haz clic derecho sobre "Carpetas locales" y elige "Importar archivo mbox".
3. Selecciona los archivos `.mbox` generados.

## Convertir a PST (Outlook)

Outlook no soporta MBOX directamente. Para migrar a PST:

1. Importa los `.mbox` en Thunderbird.
2. Exporta los correos como archivos `.eml` usando ImportExportTools NG.
3. Arrastra los `.eml` a Outlook o usa una herramienta de terceros para convertir de MBOX/EML a PST.

## Limitaciones

- No convierte directamente a PST.
- No preserva etiquetas o metadatos específicos de clientes de correo.
- El nombre de los archivos `.mbox` es plano (no crea subcarpetas anidadas en el sistema de archivos).

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

## Autor

Desarrollado por Ing. Cristobal Mujica.
