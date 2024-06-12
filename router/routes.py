from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from controllers.client_controllers import create_cliente, delete_cliente, get_all_clientes, get_clientes_segmento, update_cliente
from controllers.stats_controller import get_grafica, get_producto_mas_consumido, get_producto_mas_vendido, get_producto_menos_vendido
from utils.authentication import verificar_credenciales

router = APIRouter()

# Mensaje de bienvenida
@router.get("/")
async def obtener_mensaje() -> dict:
    return {"message": "¡Bienvenido a la API de Eureka! Esta API proporciona información sobre productos más y menos vendidos, así como el producto más consumido por mes."}

# Obtener clientes por segmento
@router.get("/clientes/{segmento}")
async def obtener_clientes(segmento: str, authenticated: bool = Depends(verificar_credenciales)) -> dict:
    return get_clientes_segmento(segmento=segmento)

# CRUD - Create (Agregar un nuevo cliente)
@router.post("/clientes")
async def agregar_cliente(id_cliente: str, nombre: str, cliente: str, authenticated: bool = Depends(verificar_credenciales)) -> dict:
    return create_cliente(id_cliente= id_cliente, nombre=nombre, cliente=cliente)

# CRUD - Read (Obtener todos los clientes segmentados)
@router.get("/clientes")
async def obtener_todos_los_clientes(authenticated: bool = Depends(verificar_credenciales)):
    return get_all_clientes()

# CRUD - Update (Actualizar información de un cliente)
@router.put("/clientes/{id_cliente}")
async def actualizar_cliente(id_cliente: str, nombre: str, cliente: str, authenticated: bool = Depends(verificar_credenciales)):
    return update_cliente(id_cliente= id_cliente, nombre= nombre, cliente= cliente)

# CRUD - Delete (Eliminar un cliente)
@router.delete("/clientes/{id_cliente}")
async def eliminar_cliente(id_cliente: str, authenticated: bool = Depends(verificar_credenciales)) -> dict:
    return delete_cliente(id_cliente=id_cliente)

# Obtener gráfica de la proporción de clientes por segmento
@router.get("/grafica", response_class=StreamingResponse)
async def obtener_grafica(authenticated: bool = Depends(verificar_credenciales)) -> StreamingResponse:
    return get_grafica()

# Obtener el producto más consumido del mes
@router.get("/producto-más-consumido")
async def obtener_producto_mas_consumido(año: int, mes: int, authenticated: bool = Depends(verificar_credenciales)) -> dict:
    return get_producto_mas_consumido(año=año, mes=mes)

# Obtener lista de los 15 productos más vendidos
@router.get("/productos-más-vendidos")
async def obtener_productos_mas_vendidos(authenticated: bool = Depends(verificar_credenciales)) -> dict:
    return get_producto_mas_vendido()

# Obtener lista de los 15 productos menos vendidos
@router.get("/productos-menos-vendidos")
async def obtener_productos_menos_vendidos(authenticated: bool = Depends(verificar_credenciales)) -> dict:
    return get_producto_menos_vendido()