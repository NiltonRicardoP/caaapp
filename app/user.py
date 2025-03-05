from pydantic import BaseModel

class User(BaseModel):
    nome: str
    email: str  # Mantido como string simples, sem EmailStr
    cpf: str
    idade: int
    filhos_ou_parentes_atipicos: bool
    senha: str

class UserLogin(BaseModel):
    identifier: str  # Pode ser email ou CPF
    senha: str
