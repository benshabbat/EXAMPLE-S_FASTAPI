from fastapi import FastAPI
import uvicorn

app = FastAPI()



@app.get("/")
def read_root():
    return {"messag"}
@app.get("/{text}")
def get_root(text: str):
    return {"message": f"Welcome to the String Operations API, you entered: {text}"}