from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
from app.database import get_db_connection

router = APIRouter()

# Rota para fazer upload de imagens e adicionar a descrição
@router.post("/upload-symbol")
async def upload_symbol(description: str = Form(...), file: UploadFile = File(...)):
    try:
        print(f"Recebendo upload: descrição={description}, arquivo={file.filename}")
        
        # Caminho para salvar a imagem
        upload_dir = "app/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = file.filename.lower()
        file_location = f"{upload_dir}/{filename}"
        
        # Salvar o arquivo
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        image_url = f"https://caaapp.onrender.com/uploads/{filename}"
        
        # Inserir no banco de dados
        db = get_db_connection()
        cursor = db.cursor()
        query = "INSERT INTO symbols (description, image_url) VALUES (%s, %s)"
        cursor.execute(query, (description, image_url))
        db.commit()
        
        print("Símbolo adicionado com sucesso!")
        return JSONResponse(content={"message": "Símbolo adicionado com sucesso!"})
    except Exception as e:
        print(f"Erro ao fazer upload: {e}")
        return JSONResponse(content={"message": "Erro ao fazer upload!"}, status_code=500)

@router.get("/symbols")
def get_symbols():
    try:
        print("Recebendo solicitação para /symbols")
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM symbols")
        symbols = cursor.fetchall()

        # Garantir que as URLs estejam corretas
        for symbol in symbols:
            if symbol['image_url']:
                symbol['image_url'] = f"https://caaapp.onrender.com/uploads/{symbol['image_url'].split('/')[-1]}"
            else:
                symbol['image_url'] = None  # Caso a URL seja nula

        print(f"Retornando símbolos: {symbols}")
        return symbols
    except Exception as e:
        print(f"Erro ao buscar símbolos: {e}")
        return JSONResponse(content={"message": "Erro ao buscar símbolos!"}, status_code=500)



from fastapi import FastAPI

app = FastAPI()

# Servir arquivos estáticos na pasta uploads
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

# Incluir rotas do módulo symbols
app.include_router(router)
