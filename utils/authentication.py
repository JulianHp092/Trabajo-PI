from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

# Credenciales de acceso
fake_users_db = {
    "Vero": "1234"  # Usuario: Vero, Contraseña: 1234
}

# Función para verificar las credenciales
def verificar_credenciales(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if username not in fake_users_db or fake_users_db[username] != password:
        raise HTTPException(status_code=401, detail="Nombre de usuario o contraseña incorrectos")
    return True