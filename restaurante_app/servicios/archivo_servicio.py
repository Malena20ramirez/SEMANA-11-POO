import json
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
    def __init__(self, ruta_datos: str = "datos") -> None:
        self._ruta_datos = Path(ruta_datos)
        self._ruta_productos = self._ruta_datos / "productos.json"
        self._ruta_usuarios = self._ruta_datos / "usuarios.json"
        self._ruta_ventas = self._ruta_datos / "ventas.json"

    def cargar_productos(self) -> list[Producto]:
        # JSON -> diccionarios -> objetos Producto.
        datos = self._leer_lista(self._ruta_productos, "productos")
        productos: list[Producto] = []

        for item in datos:
            if not isinstance(item, dict):
                print("Se encontro un registro de producto con formato invalido y fue omitido.")
                continue

            try:
                producto = Producto(
                    item["codigo"],
                    item["nombre"],
                    item["precio"],
                    item.get("disponible", True),
                    item.get("stock", 0),
                )
                productos.append(producto)
            except KeyError:
                print("Se encontro un registro de producto incompleto y fue omitido.")
            except ValueError as error:
                print(f"Se encontro un producto con datos invalidos: {error}")

        return productos

    def guardar_productos(self, productos: list[Producto]) -> bool:
        # Objetos Producto -> diccionarios -> JSON.
        datos = []
        for producto in productos:
            datos.append(producto.convertir_a_diccionario())
        return self._guardar_lista(self._ruta_productos, datos, "productos")

    def cargar_usuarios(self) -> list[Usuario]:
        # JSON -> objetos Usuario.
        datos = self._leer_lista(self._ruta_usuarios, "usuarios")
        usuarios: list[Usuario] = []

        for item in datos:
            if not isinstance(item, dict):
                print("Se encontro un registro de usuario con formato invalido y fue omitido.")
                continue

            try:
                usuarios.append(Usuario(item["identificacion"], item["nombre"]))
            except KeyError:
                print("Se encontro un registro de usuario incompleto y fue omitido.")
            except ValueError as error:
                print(f"Se encontro un usuario con datos invalidos: {error}")

        return usuarios

    def guardar_usuarios(self, usuarios: list[Usuario]) -> bool:
        # Objetos Usuario -> JSON.
        datos = []
        for usuario in usuarios:
            datos.append(usuario.convertir_a_diccionario())
        return self._guardar_lista(self._ruta_usuarios, datos, "usuarios")

    
    def cargar_ventas(self) -> list[Venta]:
        datos = self._leer_lista(self._ruta_ventas, "ventas")
        ventas: list[Venta] = []

        for item in datos:
            if not isinstance(item, dict):
                print("Se encontro un registro de venta con formato invalido y fue omitido.")
                continue

            try:
                ventas.append(
                    Venta(
                        item["usuario_id"],
                        item["producto_codigo"],
                        item.get("cantidad", 1),
                    )
                )
            except KeyError:
                print("Se encontro un registro de venta incompleto y fue omitido.")
            except ValueError as error:
                print(f"Se encontro una venta con datos invalidos: {error}")

        return ventas

    def guardar_ventas(self, ventas: list[Venta]) -> bool:
        # Objetos Venta -> JSON.
        datos = []
        for venta in ventas:
            datos.append(venta.convertir_a_diccionario())
        return self._guardar_lista(self._ruta_ventas, datos, "ventas")

    def _leer_lista(self, ruta: Path, nombre: str) -> list:
        # Metodo de apoyo para no repetir el manejo de errores de archivos.
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"El archivo de {nombre} no tiene un formato JSON valido.")
            return []
        except PermissionError:
            print(f"No hay permisos suficientes para leer el archivo de {nombre}.")
            return []

        if not isinstance(datos, list):
            print(f"El archivo de {nombre} debe contener una lista de registros.")
            return []

        return datos

    def _guardar_lista(self, ruta: Path, datos: list, nombre: str) -> bool:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"No hay permisos suficientes para guardar el archivo de {nombre}.")
            return False
