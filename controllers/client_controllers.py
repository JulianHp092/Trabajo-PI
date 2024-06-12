from fastapi import HTTPException
import pandas as pd

# Leer los datos de los archivos CSV
clientes_df = pd.read_csv("clientes_segmentados.csv", index_col="ID cliente")

def get_clientes_segmento(segmento: str) -> dict:
    """
    Obtener clientes por segmento.
    """
    if segmento.lower() not in ["oro", "plata", "bronce"]:
        raise HTTPException(status_code=404, detail="Segmento no válido")

    clientes_segmento = clientes_df[clientes_df["Cliente"] == segmento.capitalize()]
    clientes = clientes_segmento["Nombre"].tolist()
    cantidad = len(clientes)
    porcentaje = (cantidad / len(clientes_df)) * 100

    return {
        "segmento": segmento.capitalize(),
        "clientes": clientes,
        "cantidad": cantidad,
        "porcentaje": f"{porcentaje:.2f}%"
    }

def create_cliente(id_cliente: str, nombre: str, cliente: str) -> dict:
    """ Agregar un nuevo cliente. """
    global clientes_df
    if cliente.lower() not in ["oro", "plata", "bronce"]:
        raise HTTPException(status_code=404, detail="Segmento no válido")

    nuevos_datos = pd.DataFrame({"ID_cliente": [id_cliente], "Nombre": [nombre], "Cliente": [cliente.capitalize()]})
    clientes_df = pd.concat([clientes_df, nuevos_datos])
    clientes_df.to_csv("clientes_segmentados.csv")
    return {"message": "Cliente agregado exitosamente"}

def get_all_clientes() -> dict:
    """ Obtener todos los clientes segmentados. """
    return clientes_df.to_dict(orient="index")


def update_cliente(id_cliente: str, nombre: str, cliente: str):
    """ Actualizar información de un cliente. """
    global clientes_df
    if id_cliente not in clientes_df.index:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if cliente.lower() not in ["oro", "plata", "bronce"]:
        raise HTTPException(status_code=404, detail="Segmento no válido")

    clientes_df.loc[id_cliente] = [nombre, cliente.capitalize()]
    clientes_df.to_csv("clientes_segmentados.csv")
    return {"message": "Cliente actualizado exitosamente"}

def delete_cliente(id_cliente: str) -> dict:
    """ Eliminar un cliente. """
    global clientes_df
    if id_cliente not in clientes_df.index:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    clientes_df = clientes_df.drop(id_cliente)
    clientes_df.to_csv("clientes_segmentados.csv")
    return {"message": "Cliente eliminado exitosamente"}