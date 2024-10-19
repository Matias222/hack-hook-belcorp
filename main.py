from fastapi import FastAPI, Request, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from ast import literal_eval
from typing import Optional
from db_functions import Repository, Consultora
from api_models import ApiState

import aux_functions
import twilio_functions
import flow_estados

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def extraer_json(request:Request):
    return await request.form()

@app.get("/")
def hello_world():
    return {'message': 'Hello from FastAPI'}

@app.post("/twilio-webhook")
def webhook(request: bytes=Depends(extraer_json)):

    numero = request["From"]
    mensaje = request["Body"]

    mensaje=aux_functions.handler_media(mensaje,request)

    if(mensaje=="-1"):
        twilio_functions.enviar_mensaje(numero,"Por ahora solo entiendo audios y texto 😔😔😔. No te puedo ayudar")
        return

    print("*"*50)
    print(numero,"->",mensaje)
    print("*"*50)

    #Nombre consultora
    #Nombre de los productos o producto
    #Cantidad de cada producto
    #Nombre de la persona venta y numero de la venta

    data_usuario=Repository(Consultora).read_by_primary_key(numero)

    if(data_usuario==None):
        data_usuario=Repository(Consultora).write(numero=numero,estado="Onboarding")

    print("Estado",data_usuario.estado)

    state=ApiState(buffer=data_usuario.buffer,estado=data_usuario.estado,numero=numero,nombre=data_usuario.nombre)

    state.buffer.append(f"Usuario: {mensaje}")

    state.print_state()

    if(state.estado=="Onboarding"):
        
        flow_estados.flujo_nombre(state)

    else:

        flow_estados.flujo_pedido(state)

    
    state.buffer.append(f"IA: {state.respuesta}")

    data_usuario=Repository(Consultora).update(pk=numero,buffer=state.buffer,estado=state.estado,nombre=state.nombre)

    twilio_functions.enviar_mensaje(state.numero,state.respuesta)
