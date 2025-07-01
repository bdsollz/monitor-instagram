from fastapi import FastAPI
from monitor import get_followers_count, start_monitoring
import threading
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    try:
        return {"seguidores": get_followers_count()}
    except:
        return {"erro": "Erro ao obter dados"}

@app.get("/web")
def web_view():
    try:
        count = get_followers_count()
        return f"<h1>Seguidores:</h1><h2>{count}</h2>"
    except:
        return f"<h1>Seguidores:</h1><h2>Erro ao obter dados</h2>"

if __name__ == "__main__":
    threading.Thread(target=start_monitoring, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
