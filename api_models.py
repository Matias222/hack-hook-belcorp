from collections import deque
from datetime import datetime
from typing import Literal
from fastapi import WebSocket, BackgroundTasks
from pydantic import BaseModel, Field

class ApiState(BaseModel):

    class Config: 
        arbitrary_types_allowed = True

    buffer: list | None = Field(default=[])
    estado: str | None = Field(default="Onboarding")
    nombre: str | None = Field(default="Consultora")
    numero: str | None
    respuesta: str | None = Field(default="")

    def print_state(self):
        print(f"Estado: {self.estado}, Nombre: {self.nombre}, Numero: {self.numero}, Buffer: {self.buffer}")
