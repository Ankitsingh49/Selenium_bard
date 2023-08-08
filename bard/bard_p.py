from bardapi import Bard 
import regex as re 
import pandas as pd 


positive =  pd.read_csv("positive_amazon.csv" )


token =  'your_token_here' 

bard =  Bard(token) 

def crux_review(review):
  if review != "[]":
    prompt = f"Give me the crux of this Amazon review in 5 words or less. Review: {review}"
    crux = bard.get_answer(prompt)
    pattern = r"\*\*(.*?)\*\*"

  
    extracted_text = re.findall(pattern, crux['content'])

    return extracted_text 
  else:
    return "No review given"
  
positive["crux"] = positive.review.apply(crux_review)

positive.to_csv("positive_amazon.csv")
