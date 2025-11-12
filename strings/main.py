import uvicorn
from string_ops import reverse_str,remove_every_third,to_upper,letter_counts_map,remove_vowels
from fastapi import FastAPI


app = FastAPI()


@app.get("/reverse")
def reverse_string(text: str):
    return reverse_str(text)


@app.get("/uppercase/{text}")
def to_upper_str(text: str):
    return to_upper(text)
    
@app.post("/remove-vowels")
def remove_vowels_str(s: str): 
    return remove_vowels(s)


@app.post("/remove-every-third")
def remove_every_third_str(s: str):
    return remove_every_third(s)


@app.get("/letter-counts/")
def letter_counts_map_str(text: str):
    return letter_counts_map(text)     
 
    
def main_run():
    uvicorn.run(app, host="0.0.0.0", port=8000) 
    


if __name__ == "__main__":
    main_run()