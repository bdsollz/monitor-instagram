from fastapi import FastAPI
from monitor import get_followers_count

app = FastAPI()

@app.get("/")
def read_root():
    count = get_followers_count()
    return {"seguidores": count}
