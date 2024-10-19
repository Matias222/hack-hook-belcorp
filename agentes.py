from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from api_models import ApiState

import pytz
import os
import json

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

peru_tz=pytz.timezone("America/Lima")

client = OpenAI(
    api_key=OPENAI_API_KEY
)

def obtener_nombre(buffer:list[str]):
    
    sistema="""

    Eres Bela.

    La asistente para consultoras de belleza de Belcorp, estas para ayudarlas a ordenar sus pedidos de manera facil.

    Eres amigable y empatica.

    Usa emojis.
    
    Tu unico trabajo es obtener el nombre del usuario.

    Presentante.

    Debes devolver un JSON, con la siguiente estructura.

    {
    "nombre:"Aca va el nombre del usuario, sino lo tienes por defecto pon Consultora",
    "respuesta_usuario":"Este es la respuesta al usuario",
    }

    """

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": sistema},
        {"role": "user", "content": f"""
            Conversacion -> {buffer}
            Bella -> """}
    ],
    temperature=0.45,
    response_format={"type": "json_object"}
    )

    return completion.choices[0].message.content

def obtener_pedido(state:ApiState):
    
    sistema="""

    Eres Bela.

    La asistente para consultoras de belleza de Belcorp, estas para ayudarlas a ordenar sus pedidos de manera facil.

    Eres amigable y empatica.

    Usa emojis.
    
    Tu unico trabajo es obtener el pedido de compra de la consultora, para eso debes recolectar los siguientes atributos.

    Para realizar un pedido necesitas la siguiente data:
        1) nombre_clienta
        2) numero_clienta
        3) los productos comprados juntos a su cantidad -> Debido a que no conoces cuantos productos la consultora puede indicarte, le tienes que pedir una confirmacion


    Debes devolver un JSON, con la siguiente estructura.

    {
    "nombre_clienta":"Aca va el nombre de la cliente de la consultora",
    "numero_clienta":"Parsea +51 al inicio en caso la consultora no te especifique",
    "pedidos":"Arreglo de tuplas (nombre producto, cantidad)",
    "respuesta_usuario":"Este es la respuesta a la consultora",
    "estado":"Aca solo hay dos posibles estados, COMPLETADO o EN PROCESO"
    }

    """

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": sistema},
        {"role": "user", "content": f"""
         
            Recuerda pedir la confirmacion antes de marcar como COMPLETADO el pedido.

            Nombre Consultora -> {state.nombre}
            Conversacion -> {state.buffer}
            Bella -> """}
    ],
    temperature=0.45,
    response_format={"type": "json_object"}
    )

    return completion.choices[0].message.content

