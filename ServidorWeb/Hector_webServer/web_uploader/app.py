import os

from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile

app = FastAPI()

@app.get('/')     #decorador de funcion para añadir otras cosas
def hello():
    return "Hello"
@app.get('/bye')     #decorador de funcion para añadir otras cosas
def bye():
    return "bye"

@app.post('/upload-file/')
def upload_file(file:UploadFile=File(...)):
    try:
        os.makedirs('./uploads',exist_ok=True)
    except:
        return "Upload failed"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8081)
