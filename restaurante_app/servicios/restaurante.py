from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    def __init__(
        self,
        productos_iniciales: list[Producto] | None = None,
        usuarios_iniciales: list[Usuario] | None = None,
        ventas_iniciales: list[Venta] | None = None,
    ) -> None:
       
        self._productos: list[Producto] = productos_iniciales.copy() if productos_iniciales else []
        self._usuarios: list[Usuario] = (
            usuarios_iniciales.copy() if usuarios_iniciales else []
        )
        self._ventas: list[Venta] = ventas_iniciales.copy() if ventas_iniciales else []

    def registrar_producto(self, producto: Producto) -> bool:
        if self.buscar_producto(producto.codigo) is not None:
            return False

        self._productos.append(producto)
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        codigo = codigo.strip()
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def actualizar_producto(
        self,
        codigo: str,
        nuevo_nombre: str,
        nuevo_precio: float,
        nuevo_stock: int,
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False

        self._productos.remove(producto)
        return True

    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    def contar_productos(self) -> int:
        return len(self._productos)

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if self.buscar_usuario(usuario.identificacion) is not None:
            return False

        self._usuarios.append(usuario)
        return True

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        identificacion = identificacion.strip()
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None

    def actualizar_usuario(self, identificacion: str, nuevo_nombre: str) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False

        usuario.nombre = nuevo_nombre
        return True

    def eliminar_usuario(self, identificacion: str) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False

        self._usuarios.remove(usuario)
        return True

    def listar_usuarios(self) -> list[Usuario]:
        return self._usuarios.copy()

    def prestar_producto(self, codigo_producto: str, identificacion_usuario: str) -> bool:
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        # Reglas de negocio antes de crear la relacion.
        if usuario is None or producto is None:
            return False
        
        if not producto.disponible:
            return False

    def devolver_producto(self, codigo_producto: str, identificacion_usuario: str) -> bool:
        producto = self.buscar_producto(codigo_producto)

        if producto.disponible:
            return False

    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_usuario: str,
        cantidad: int = 1,
    ) -> bool:
        # MEJORA SEMANA 11: nueva operacion para vender y descontar stock.
        # Desde aqui empieza la operacion de venta: Usuario -> Venta -> Libro.
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        # Reglas de negocio: usuario, producto, tipo VENTA y stock suficiente.
        if usuario is None or producto is None:
            return False
        if not producto.es_de_venta():
            return False
        if producto.stock < cantidad:
            return False

        # Aqui se registra la relacion de venta.
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        # Y aqui se ve el cambio interno del producto: stock disminuye.
        producto.vender(cantidad)
        return True

    def listar_ventas(self) -> list[Venta]:
        return self._ventas.copy()

    def consultar_operaciones_usuario(
        self,
        identificacion_usuario: str,
    ) -> tuple[list[Venta]]:
        identificacion_usuario = identificacion_usuario.strip()
        ventas_usuario: list[Venta] = []

        for venta in self._ventas:
            if venta.usuario_id == identificacion_usuario:
                ventas_usuario.append(venta)

        return ventas_usuario
    
    def obtener_categorias_unicas(self) -> set[str]:
        categorias: set[str] = set()
        for producto in self._productos:
            categorias.add(producto.categoria)
        return categorias

    def existe_categoria(self, categoria: str) -> bool:
        return categoria.strip() in self.obtener_categorias_unicas()
