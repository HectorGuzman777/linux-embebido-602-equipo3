import os
import shutil

from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def main():
    content = """
<!DOCTYPE html>
<html>
    <head>
        <title>Upload a file</title>
    </head>
    <body>
        <h1>Upload a file</h1>
        <form action="/uploadfile/" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit">
        </form>
    </body>
</html>
    """
    return content

@app.get('/')   #Decoradores de funciones: funcion que crea otras funciones
# (decora la funcion para añadirle otras cosas) en la ruta "/"" nos va a regresar un "Hello"
def hello():
    return "Casa_Inteligente"

@app.get('/bye')
def bye():
    return "Bye"

@app.post('/upload_file/')
def upload_file(file:UploadFile=File(...)):
    try:
        os.makedirs('./uploads', exist_ok=True)
        with open(f'./uploads/{file.filename}', "wb+") as f:
            shutil.copyfileobj(file.file, f)
    except:
        return "Upload falied"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8082)