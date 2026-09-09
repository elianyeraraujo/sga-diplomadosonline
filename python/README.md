# Implementación en Python - SGA-DO

Esta carpeta contiene la implementación en Python del Sistema de Gestión Académica de DiplomadosOnline (SGA-DO).

## Archivos principales

- `main.py`: código fuente principal del sistema.
- `alumnos.txt`: almacena los datos de los alumnos y sus notas.
- `profesores.txt`: almacena los datos de los profesores.
- `certificados_pendientes.txt`: reporte generado con los alumnos aprobados pendientes de certificación.

## Funcionalidades

El sistema permite:

- Registrar alumnos.
- Registrar profesores.
- Registrar notas.
- Deshacer el último registro de nota mediante una pila (LIFO).
- Generar una cola de certificados (FIFO).
- Mostrar un reporte general.
- Guardar y recuperar los datos mediante archivos de texto.

## Ejecución

Desde la carpeta `python`, ejecutar:

```bash
python main.py