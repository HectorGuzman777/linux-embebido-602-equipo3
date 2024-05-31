from fastapi import FastAPI

app = FastAPI()

@app.get('/')     #decorador de funcion para añadir otras cosas
def hello():
    return "Hello"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8080)
