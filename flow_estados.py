from api_models import ApiState
from db_functions import Repository, Pedidos
from datetime import datetime
import agentes
import json
import random
import requests

current_date = datetime.now().strftime('%Y-%m-%d')


def flujo_nombre(state:ApiState):

    rpta=agentes.obtener_nombre(state.buffer)

    rpta=json.loads(rpta)

    print(rpta)

    if(rpta["nombre"]!="Consultora"): 
        state.nombre=rpta["nombre"]
        state.estado="Base"
        state.respuesta=f"""Perfecto {state.nombre} 💪💪💪 Ahora estoy lista para registrar los pedidos que tengas 😍😍😍

Solo necesitaria 3 cosas:

1) El nombre de tu clienta
2) El teléfono de tu clienta
3) La cantidad y productos que esta llevando

Quedo a la espera 🥰🥰🥰
""" 
        state.buffer=[]
    else:
        state.respuesta=rpta["respuesta_usuario"]


def flujo_pedido(state:ApiState):


    skus_poc=["200106284","200113178","200109873","210102579","200083615","200095864","200105011","200098673","200102430"]

    rpta=agentes.obtener_pedido(state)

    rpta=json.loads(rpta)

    print(rpta)

    state.respuesta=rpta["respuesta_usuario"]

    if(rpta["estado"]=="COMPLETADO"):

        state.buffer=[]    

        for i in rpta["pedidos"]:

            id=random.randint(1,100000)+random.randint(50000,60000)
            sku_rand=skus_poc[random.randint(0,9)]

            producto=i[0]
            cantidad=i[1]

            print(producto)
            print(cantidad)
            
            Repository(Pedidos).write(id=id,sku=sku_rand,numero=state.numero,fecha=current_date,cantidad=cantidad,nombre_vendio=rpta["nombre_clienta"],numero_vendio=rpta["numero_clienta"])

        state.respuesta="Pedido registrado muchas gracias!"

        requests.get(f"https://5kivbvxais.us-east-1.awsapprunner.com/products/{state.numero[10:]}/{sku_rand}/closest")

        #LLAMADA A LA API DE JOAQUIN (MI NUMERO)