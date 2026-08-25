# Restaurante App -  Semana 11

## Estudiante:
Ramirez Pacho Malena Jimena

---

## 1. Descripción del Proyecto
Evolución de la aplicación modular `restaurante_app`. Esta versión amplía el sistema para gestionar la operación principal de **venta de productos**, relacionando un `Usuario` registrado con un `Producto` disponible, controlando el stock y garantizando la persistencia completa mediante archivos JSON.

---

## 2. Estructura del Repositorio
```text
restaurante_app/
│
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
│
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
│
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
│
├── main.py
└── README.md
```

- `datos/`: Almacena los archivos JSON (`productos.json`, `usuarios.json`, `ventas.json`).
- `modelos/`: Clases de dominio (`Producto`, `Usuario`, `Venta`).
- `servicios/`:
  - `archivo_servicio.py`: Mapeo y persistencia JSON con manejo de excepciones.
  - `restaurante.py`: Lógica de negocio y reglas del sistema.
- `main.py`: Interfaz por consola interactiva.


4. Relación Principal: Usuario + Producto → Venta
La operación de venta conecta ambas entidades principales bajo el siguiente flujo:

Se verifica la existencia del Usuario registrado mediante su identificación.

Se verifica la existencia del Producto mediante su código.

Se valida que la cantidad solicitada sea estrictamente mayor a 0 y que el producto disponga de stock suficiente.

Se crea un nuevo objeto Venta y se añade a la colección de ventas.

Se disminuye la cantidad del producto y se persisten automáticamente los cambios en ventas.json y productos.json.

5. Control de Stock del Producto
Antes de vender: Se valida que cantidad_solicitada <= stock_disponible.

Durante la venta: El método producto.vender(cantidad) decrementa el atributo stock.

Protección: Se impide que el stock alcance valores negativos, rechazando la transacción si la cantidad excede la existencia actual.

6. Persistencia y Manejo de Excepciones
La persistencia de datos utiliza json.dump() y json.load() con codificación UTF-8. Se han controlado explícitamente las siguientes excepciones:

FileNotFoundError: Si los archivos JSON no existen al iniciar, la aplicación arranca con colecciones vacías [] sin interrumpir la ejecución.

json.JSONDecodeError: Captura y notifica en consola si un archivo JSON presenta un formato inválido o corrompido.

PermissionError: Controla fallos de permisos al intentar leer o escribir en el disco.

KeyError: Previene errores en la reconstrucción de objetos si falta alguna clave esperada en los diccionarios JSON.

ValueError: Valida que cantidades, precios y stocks sean valores numéricos válidos.
