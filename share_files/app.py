import shutil
from fastapi import FastAPI, UploadFile

from http import HTTPStatus

app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


# @app.post('/send-file', status_code=HTTPStatus.CREATED)
# async def create_upload_file(file: UploadFile):

#     with open(f'./files/{file.filename}','wb') as new_file:
#         await file.seek(0)
#         shutil.copyfileobj(file.file, new_file)

#     return {'filename': file.filename}


@app.post('/send-file', status_code=HTTPStatus.CREATED)
async def create_upload_file(file: UploadFile):
    chunk_size: int = 1024
    with open(f'./files/{file.filename}','wb') as new_file:
        
        # Enquanto houver dados no arquivo de origem
        
        while True:
            # Lê os dados em blocos
            chunk = await file.read(chunk_size)
            
            
            # Se o bloco estiver vazio, significa que o arquivo terminou
            if not chunk:
                print('executando chunk')
                break
            
            # Escreve o bloco no novo arquivo
            new_file.write(chunk)

    return {'filename': file.filename}

