from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth import hash_password, verify_password, create_token, get_current_user

app = FastAPI()

# Base de datos simulada de usuarios (con roles: 'estudiante' o 'admin')
fake_users_db = {
    "estudiante1": {
        "username": "estudiante1",
        "hashed_password": hash_password("123456"),
        "role": "estudiante"
    }
}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales incorrectas"
        )
    access_token = create_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/publico")
def ruta_publica():
    return {"mensaje": "Este es un endpoint público accesible para cualquiera."}

@app.get("/privado")
def ruta_privada(current_user: dict = Depends(get_current_user)):
    return {"mensaje": f"Hola {current_user['username']}, autenticación exitosa."}

@app.get("/admin")
def ruta_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador (rol estudiante detectado)."
        )
    return {"mensaje": "Bienvenido al panel de administración."}