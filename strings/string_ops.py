
import os
import json
"""   
# Create data directory if it doesn't exist
 
    os.makedirs("data", exist_ok=True)
  
    with open("data/letter_counts.json", "w") as f:
        json.dump(object_to_save, f) 
          
"""



def reverse_str(text: str): 
    return {"normal_string":text,"reversed_text":text[::-1]}



def to_upper(text: str): 
    return {"normal_string":text,"uppercased":text.upper()}



def remove_vowels(s: str): 
    vowels="aeuioAEIOU"
    without_vowels=""
    for char in s:
        if char not in vowels:
            without_vowels+=char
    return {"normal_string":s,"without_vowels":without_vowels}



def remove_every_third(s: str):
    new_string = ""
    for idx,char in enumerate(s):
        if (idx+1) %3 !=0:
            new_string += char   
        
    
    return  { "original": s, "result": new_string}


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
  
