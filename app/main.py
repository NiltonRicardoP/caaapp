from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes.symbols import router as symbols_router  # Importando as rotas de symbols
from app.routes.user import router as user_router  # Importando as rotas de user

# Inicializa o aplicativo FastAPI
app = FastAPI()

# Configuração do CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (ajuste conforme necessário)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Montar a pasta 'uploads' para servir arquivos estáticos
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

# Incluir as rotas de users
app.include_router(user_router, prefix="/users", tags=["users"])

# Incluir as rotas de symbols
app.include_router(symbols_router)

# Executar o servidor diretamente (opcional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
