from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante

OPCIONES_MENU = (
    ("1", "Registrar producto"),
    ("2", "Buscar producto"),
    ("3", "Actualizar producto"),
    ("4", "Eliminar producto"),
    ("5", "Listar productos"),
    ("6", "Registrar usuario"),
    ("7", "Buscar usuario"),
    ("8", "Actualizar usuario"),
    ("9", "Eliminar usuario"),
    ("10", "Listar usuarios"),
    # MEJORA SEMANA 11: se agregan operaciones reales que relacionan objetos.
    ("11", "Prestar producto"),
    ("12", "Devolver producto"),
    ("13", "Vender producto"),
    ("14", "Consultar operaciones de usuario"),
    ("15", "Listar categorias unicas"),
    ("0", "Salir"),
)


# Funciones pequenas para entrada por consola.
# La logica importante queda en Restaurante.
def pedir_texto(mensaje: str) -> str:
    return input(mensaje).strip()


def pedir_entero(mensaje: str, valor_por_defecto: int | None = None) -> int:
    texto = pedir_texto(mensaje)
    if texto == "" and valor_por_defecto is not None:
        return valor_por_defecto
    return int(texto)


def mostrar_menu() -> None:
    print("\n===== RESTAURANTE APP =====")
    print("\nGESTION DE PRODUCTOS")
    for numero, descripcion in OPCIONES_MENU[:5]:
        print(f"{numero}. {descripcion}")

    print("\nGESTION DE USUARIOS")
    for numero, descripcion in OPCIONES_MENU[5:10]:
        print(f"{numero}. {descripcion}")

    print("\nOPERACIONES")
    for numero, descripcion in OPCIONES_MENU[10:14]:
        print(f"{numero}. {descripcion}")

    print("\nCONSULTAS")
    print(f"{OPCIONES_MENU[14][0]}. {OPCIONES_MENU[14][1]}")
    print("0. Salir")


def guardar_productos(archivo_servicio: ArchivoServicio, restaurante: Restaurante) -> None:
    # Guardado automatico despues de modificar productos.
    guardado = archivo_servicio.guardar_productos(restaurante.listar_productos())
    if not guardado:
        print("Los cambios de productos no pudieron guardarse.")


def guardar_usuarios(
    archivo_servicio: ArchivoServicio,
    restaurante: Restaurante,
) -> None:
    # Guardado automatico despues de modificar usuarios.
    guardado = archivo_servicio.guardar_usuarios(restaurante.listar_usuarios())
    if not guardado:
        print("Los cambios de usuarios no pudieron guardarse.")


def guardar_ventas(archivo_servicio: ArchivoServicio, restaurante: Restaurante) -> None:
    # MEJORA SEMANA 11: las ventas ahora se guardan en su propio JSON.
    # Guardado automatico despues de vender.
    guardado = archivo_servicio.guardar_ventas(restaurante.listar_ventas())
    if not guardado:
        print("Los cambios de ventas no pudieron guardarse.")


def registrar_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Registrar producto ---")
    codigo = pedir_texto("Codigo: ")
    nombre = pedir_texto("Nombre: ")
    precio = pedir_texto("Precio: ")

    try:
        stock = 0

        Producto = Producto(codigo, nombre, precio, True, stock)
        registrado = restaurante.registrar_producto(Producto)

        if registrado:
            print("Producto registrado correctamente.")
            guardar_productos(archivo_servicio, restaurante)
        else:
            print("El codigo ya se encuentra registrado.")
    except ValueError as error:
        print(error)


def buscar_producto(restaurante: Restaurante) -> None:
    print("\n--- Buscar producto ---")
    codigo = pedir_texto("Codigo del producto: ")
    producto = restaurante.buscar_producto(codigo)

    if producto is None:
        print("Producto no encontrado.")
    else:
        print(producto)


def actualizar_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Actualizar producto ---")
    codigo = pedir_texto("Codigo del producto: ")
    producto = restaurante.buscar_producto(codigo)

    if producto is None:
        print("Producto no encontrado.")
        return

    nuevo_nombre = pedir_texto("Nuevo nombre: ")
    nuevo_precio = pedir_texto("Nuevo precio: ")

    try:
        nuevo_stock = 0
        
        actualizado = restaurante.actualizar_producto(
            codigo,
            nuevo_nombre,
            nuevo_precio,
            nuevo_stock,
        )
    
        if actualizado:
            print("Producto actualizado correctamente.")
            guardar_productos(archivo_servicio, restaurante)
        else:
            print("No se pudo actualizar. Revise si el producto existe.")
    except ValueError as error:
        print(error)


def eliminar_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Eliminar producto ---")
    codigo = pedir_texto("Codigo del producto: ")
    producto = restaurante.buscar_producto(codigo)

    if producto is None:
        print("Producto no encontrado.")
        return

    eliminado = restaurante.eliminar_producto(codigo)

    if eliminado:
        print("Producto eliminado correctamente.")
        guardar_productos(archivo_servicio, restaurante)
    else:
        print("No se pudo eliminar. Revise si el producto existe.")
        print(f"No se puede eliminar. El producto esta en stock.")
        return

    eliminado = restaurante.eliminar_producto(codigo)

    if eliminado:
        print("Producto eliminado correctamente.")
        guardar_productos(archivo_servicio, restaurante)
    else:
        print("Producto no encontrado.")


def listar_productos(restaurante: Restaurante) -> None:
    print("\n--- Lista de productos ---")
    productos = restaurante.listar_productos()

    if len(productos) == 0:
        print("No hay productos registrados.")
        return

    for indice, producto in enumerate(productos):
        print(f"{indice + 1}. {producto}")

    primer_producto = productos[0]
    print(f"\nPrimer producto registrado: {primer_producto.nombre}")
    print(f"Total de productos: {restaurante.contar_productos()}")


def registrar_usuario(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Registrar usuario ---")
    identificacion = pedir_texto("Identificacion: ")
    nombre = pedir_texto("Nombre: ")

    try:
        usuario = Usuario(identificacion, nombre)
        registrado = restaurante.registrar_usuario(usuario)

        if registrado:
            print("Usuario registrado correctamente.")
            guardar_usuarios(archivo_servicio, restaurante)
        else:
            print("La identificacion ya se encuentra registrada.")
    except ValueError as error:
        print(error)


def buscar_usuario(restaurante: Restaurante) -> None:
    print("\n--- Buscar usuario ---")
    identificacion = pedir_texto("Identificacion del usuario: ")
    usuario = restaurante.buscar_usuario(identificacion)

    if usuario is None:
        print("Usuario no encontrado.")
    else:
        print(usuario)


def actualizar_usuario(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Actualizar usuario ---")
    identificacion = pedir_texto("Identificacion del usuario: ")

    if restaurante.buscar_usuario(identificacion) is None:
        print("Usuario no encontrado.")
        return

    nuevo_nombre = pedir_texto("Nuevo nombre: ")

    try:
        actualizado = restaurante.actualizar_usuario(identificacion, nuevo_nombre)

        if actualizado:
            print("Usuario actualizado correctamente.")
            guardar_usuarios(archivo_servicio, restaurante)
        else:
            print("Usuario no encontrado.")
    except ValueError as error:
        print(error)


def eliminar_usuario(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Eliminar usuario ---")
    identificacion = pedir_texto("Identificacion del usuario: ")
    eliminado = restaurante.eliminar_usuario(identificacion)

    if eliminado:
        print("Usuario eliminado correctamente.")
        guardar_usuarios(archivo_servicio, restaurante)
    else:
        print("Usuario no encontrado.")


def listar_usuarios(restaurante: Restaurante) -> None:
    print("\n--- Lista de usuarios ---")
    usuarios = restaurante.listar_usuarios()

    if len(usuarios) == 0:
        print("No hay usuarios registrados.")
        return

    for indice, usuario in enumerate(usuarios):
        print(f"{indice + 1}. {usuario}")


def prestar_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    
    print("\n--- Prestar producto ---")
    codigo_producto = pedir_texto("Codigo del producto: ")
    identificacion_usuario = pedir_texto("Identificacion del usuario: ")

    # El main valida mensajes para el usuario, pero la regla final esta en el servicio.
    producto = restaurante.buscar_producto(codigo_producto)
    usuario = restaurante.buscar_usuario(identificacion_usuario)

    if usuario is None:
        print("Usuario no encontrado.")
        return
    if producto is None:
        print("Producto no encontrado.")
        return
    if not producto.disponible:
        print("El producto no esta disponible.")
        return

def devolver_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    
    print("\n--- Devolver producto ---")
    codigo_producto = pedir_texto("Codigo del producto: ")
    identificacion_usuario = pedir_texto("Identificacion del usuario: ")

    devuelto = restaurante.devolver_producto(codigo_producto, identificacion_usuario)
    if devuelto:
        print("Producto devuelto correctamente.")
        guardar_productos(archivo_servicio, restaurante)
    else:
        print("No se pudo devolver. Revise el producto, el usuario y el prestamo activo.")


def vender_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    
    print("\n--- Vender producto ---")
    codigo_producto = pedir_texto("Codigo del producto: ")
    identificacion_usuario = pedir_texto("Identificacion del usuario: ")

    producto = restaurante.buscar_producto(codigo_producto)
    usuario = restaurante.buscar_usuario(identificacion_usuario)

    if usuario is None:
        print("Usuario no encontrado.")
        return
    if producto is None:
        print("Producto no encontrado.")
        return


    try:
        cantidad = pedir_entero("Cantidad (Enter para 1): ", 1)
        if producto.stock < cantidad:
            print("No hay stock suficiente.")
            return

        vendido = restaurante.vender_producto(codigo_producto, identificacion_usuario, cantidad)
        if vendido:
            print(f"Venta registrada correctamente. Stock actual: {producto.stock}")
            # Se guardan la venta creada y el nuevo stock del producto.
            guardar_ventas(archivo_servicio, restaurante)
            guardar_productos(archivo_servicio, restaurante)
        else:
            print("No fue posible realizar la venta.")
    except ValueError as error:
        print(error)


def consultar_operaciones_usuario(restaurante: Restaurante) -> None:
    
    print("\n--- Operaciones de usuario ---")
    identificacion = pedir_texto("Identificacion del usuario: ")
    usuario = restaurante.buscar_usuario(identificacion)

    if usuario is None:
        print("Usuario no encontrado.")
        return

    prestamos, ventas = restaurante.consultar_operaciones_usuario(identificacion)
    print(f"\nUsuario: {usuario.nombre}")

    print("\nPrestamos:")
    if len(prestamos) == 0:
        print("- Sin prestamos activos")
    else:


     print("\nVentas:")
    if len(ventas) == 0:
        print("- Sin ventas registradas")
    else:
        for venta in ventas:
            producto = restaurante.buscar_producto(venta.producto_codigo)
            nombre = producto.nombre if producto is not None else "Producto no encontrado"
            print(f"- {venta.producto_codigo} | {nombre} | Cantidad: {venta.cantidad}")


def listar_categorias_unicas(restaurante: Restaurante) -> None:
    print("\n--- Categorias unicas ---")
    categorias = restaurante.obtener_categorias_unicas()

    if len(categorias) == 0:
        print("No hay categorias registradas.")
        return

    for categoria in sorted(categorias):
        print(f"- {categoria}")

    categoria_consultada = pedir_texto("\nConsultar si existe una categoria (Enter para omitir): ")
    if categoria_consultada:
        if restaurante.existe_categoria(categoria_consultada):
            print("La categoria existe en el restaurante.")
        else:
            print("La categoria no existe en el restaurante.")


def ejecutar_menu() -> None:
    ruta_datos = Path(__file__).resolve().parent / "datos"
    archivo_servicio = ArchivoServicio(str(ruta_datos))
    
    restaurante = Restaurante(
        archivo_servicio.cargar_productos(),
        archivo_servicio.cargar_usuarios(),
        archivo_servicio.cargar_ventas(),
    )

    guardar_productos(archivo_servicio, restaurante)

    opciones = {
        "1": lambda: registrar_producto(restaurante, archivo_servicio),
        "2": lambda: buscar_producto(restaurante),
        "3": lambda: actualizar_producto(restaurante, archivo_servicio),
        "4": lambda: eliminar_producto(restaurante, archivo_servicio),
        "5": lambda: listar_productos(restaurante),
        "6": lambda: registrar_usuario(restaurante, archivo_servicio),
        "7": lambda: buscar_usuario(restaurante),
        "8": lambda: actualizar_usuario(restaurante, archivo_servicio),
        "9": lambda: eliminar_usuario(restaurante, archivo_servicio),
        "10": lambda: listar_usuarios(restaurante),
        "11": lambda: prestar_producto(restaurante, archivo_servicio),
        "12": lambda: devolver_producto(restaurante, archivo_servicio),
        "13": lambda: vender_producto(restaurante, archivo_servicio),
        "14": lambda: consultar_operaciones_usuario(restaurante),
        "15": lambda: listar_categorias_unicas(restaurante),
    }

    while True:
        mostrar_menu()
        opcion = pedir_texto("Seleccione una opcion: ")

        if opcion == "0":
            print("Gracias por usar Restaurante App.")
            break

        accion = opciones.get(opcion)
        if accion is None:
            print("Opcion invalida.")
        else:
            accion()


if __name__ == "__main__":
    ejecutar_menu()