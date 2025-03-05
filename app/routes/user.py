from fastapi import APIRouter, HTTPException, Depends, Request
from app.user import User, UserLogin
from app.database import get_db_connection
import bcrypt
import mysql.connector
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "sua_chave_secreta"

def create_jwt_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)  # Token expira em 24 horas
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

router = APIRouter()

# Rota de Registro
@router.post("/register")
def register(user: User, db=Depends(get_db_connection)):
    cursor = db.cursor()

    # Hash da senha
    hashed_password = bcrypt.hashpw(user.senha.encode(), bcrypt.gensalt())

    try:
        query = """
            INSERT INTO usuarios (nome, email, cpf, idade, filhos_ou_parentes_atipicos, senha_hash)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user.nome, user.email, user.cpf, user.idade, user.filhos_ou_parentes_atipicos, hashed_password))
        db.commit()
        return {"message": "Usuário registrado com sucesso!"}
    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=400, detail="Email ou CPF já está em uso.")
    finally:
        cursor.close()
        db.close()

# Rota de Login
@router.post("/login")
async def login(request: Request, db=Depends(get_db_connection)):
    try:
        # Log dos dados brutos recebidos na requisição
        body = await request.body()
        print("Corpo da requisição (bruto):", body.decode())  # Log do corpo bruto

        # Converte os dados brutos para JSON
        data = await request.json()
        print("Dados recebidos (JSON):", data)

        # Valida os dados com o modelo Pydantic
        user_login = UserLogin(**data)
        print("Dados validados:", user_login)

        # Consulta o usuário pelo email ou CPF
        query = "SELECT * FROM usuarios WHERE email = %s OR cpf = %s"
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (user_login.identifier, user_login.identifier))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        # Verifica se a senha fornecida corresponde ao hash armazenado
        if not bcrypt.checkpw(user_login.senha.encode(), user['senha_hash'].encode()):
            raise HTTPException(status_code=401, detail="Senha incorreta.")

        # Gera o token JWT
        token = create_jwt_token(user['id'])

        return {
            "access_token": token,
            "user": {
                "id": user['id'],
                "nome": user['nome'],
                "email": user['email']
            }
        }

    except Exception as e:
        print("Erro interno:", str(e))  # Log do erro
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

    finally:
        cursor.close()
        db.close()
