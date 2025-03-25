from fastapi import FastAPI, UploadFile

from http import HTTPStatus

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/send-file', status_code=HTTPStatus.CREATED)
async def create_upload_file(file: UploadFile):

    with open(f'./{file.filename}','wb') as new_file:
        content = await file.read()
        new_file.write(content)

    return {'filename': file.filename}
