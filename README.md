# Restaurante App -  Semana 11

## Estudiante:
Ramirez Pacho Malena Jimena

## Descripción del Proyecto
Evolución de la aplicación `restaurante_app` para incorporar la gestión de **Ventas**, relacionando las entidades `Usuario` y `Producto`, control de **stock** en tiempo real y persistencia completa en archivos **JSON**.

## Estructura del Proyecto

```text
restaurante_app/
|
|-- datos/
|   |-- productos.json
|   |-- usuarios.json
|   `-- ventas.json
|
|-- modelos/
|   |-- producto.py
|   |-- usuario.py
|   `-- venta.py
|
|-- servicios/
|   |-- archivo_servicio.py
|   `-- restaurante.py
|
`-- main.py
```
- `datos/`: Almacena los archivos JSON (`productos.json`, `usuarios.json`, `ventas.json`).
- `modelos/`: Clases de dominio (`Producto`, `Usuario`, `Venta`).
- `servicios/`:
  - `archivo_servicio.py`: Mapeo y persistencia JSON con manejo de excepciones.
  - `restaurante.py`: Lógica de negocio y reglas del sistema.
- `main.py`: Interfaz por consola interactiva.

## Manejo de Excepciones Implementado
- `FileNotFoundError`: Carga colecciones vacías si el JSON no existe.
- `json.JSONDecodeError`: Captura archivos corruptos.
- `PermissionError`: Controla fallos de lectura/escritura.
- `ValueError`: Valida stock e ingresos numéricos.