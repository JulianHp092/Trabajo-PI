from io import BytesIO
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from matplotlib import pyplot as plt
import pandas as pd

# Leer los datos de los archivos CSV
clientes_df = pd.read_csv("clientes_segmentados.csv", index_col="ID cliente")
productos_mas_vendidos_df = pd.read_csv("productos_mas_vendidos.csv")
productos_menos_vendidos_df = pd.read_csv("productos_menos_vendidos.csv")
resultados_cohorte_df = pd.read_csv("resultados_cohorte.csv")

def get_grafica():
        #Obtener gráfica de la proporción de clientes por segmento.
    oro_customers_count = len(clientes_df[clientes_df["Cliente"] == "Oro"])
    plata_customers_count = len(clientes_df[clientes_df["Cliente"] == "Plata"])
    bronce_customers_count = len(clientes_df[clientes_df["Cliente"] == "Bronce"])

    classes = ["Oro", "Plata", "Bronce"]
    counts = [oro_customers_count, plata_customers_count, bronce_customers_count]

    fig, ax = plt.subplots()
    ax.bar(classes, counts, color=['gold', 'silver', 'brown'])
    ax.set_xlabel('Segmento')
    ax.set_ylabel('Cantidad de Clientes')
    ax.set_title('Segmentación de Clientes por RFM')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    
    return StreamingResponse(buf, media_type="image/png")

def get_producto_mas_consumido(año: int, mes: int):
    #Obtener el producto más consumido del mes.
    try:
        producto_mas_consumido = resultados_cohorte_df.loc[(resultados_cohorte_df["Año"] == año) &
                                                           (resultados_cohorte_df["Mes"] == mes),
                                                           "Consumido"].iloc[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="No se encontraron datos para el año y mes especificados")

    return {"año": año, "mes": mes, "producto_mas_consumido": producto_mas_consumido}

def get_producto_mas_vendido():
    #Obtener lista de los 15 productos más vendidos.
    productos_mas_vendidos = productos_mas_vendidos_df.head(15)["Nombre producto"].tolist()
    return {"productos_mas_vendidos": productos_mas_vendidos}

def get_producto_menos_vendido():
    #Obtener lista de los 15 productos menos vendidos.
    productos_menos_vendidos = productos_menos_vendidos_df.tail(15)["Nombre producto"].tolist()
    return {"productos_menos_vendidos": productos_menos_vendidos}