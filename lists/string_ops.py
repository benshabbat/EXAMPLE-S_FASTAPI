from fastapi import FastAPI
import os
import json

app = FastAPI()


@app.get("feature/reverse/{text}")
def reverse_str(text: str): 
    return {"normal_string":text,"reversed_text":text[::-1]}


@app.get("featuer/uppercase/{text}")
def to_upper(text: str): 
    return {"normal_string":text,"uppercased":text.upper()}


@app.get("featuer/remove-vowels")
def remove_vowels(s: str): 
    vowels="aeuioAEIOU"
    without_vowels=""
    for char in s:
        if char not in vowels:
            without_vowels+=char
    return {"normal_string":s,"without_vowels":without_vowels}



@app.post("featuer/remove-every-third")
def remove_every_third(s: str):
    new_string = ""
    for idx,char in enumerate(s):
        if idx %3 !=0:
            new_string += char   
        
    
    return  { "original": s, "result": new_string}

@app.get("/fraturs/letter-counts")
def letter_counts_map(text: str):
    text_letter_counts = {}
    set_text = set(text)
    for letter in set_text:
        text_letter_counts[letter] = text.count(letter)
        
    object_to_save = {
        "original": text,
        "counts": text_letter_counts,   
    }
    
    # Create data directory if it doesn't exist
 
    os.makedirs("data", exist_ok=True)
  
    with open("data/letter_counts.json", "w") as f:
        json.dump(object_to_save, f) 
          
    return {
        "original": text,
        "counts": text_letter_counts,   
        "saved_to": "data/letter_counts.json"
    }
  
