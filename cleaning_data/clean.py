import pandas as  pd 
import numpy as np 
import regex as re
from datetime import datetime

positive =  pd.read_csv("positive_amazon.csv" , index_col= 0 )
negative =  pd.read_csv("critical_amazon.csv" , index_col= 0 )


# cleaining data for date column 
pattern = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}\b"
date_format_1 = "%B %d, %Y"
date_format_2 = "%d %B %Y"
star = r"^\d+(?:\.\d+)?" 

d =  []

# Use re.findall to extract the date of positive reviews
for x in positive.date:
  extracted_date = re.findall(pattern,  x )[0]
  date_object = datetime.strptime(  extracted_date, date_format_1).date().strftime('%Y-%m-%d')
  d.append(date_object)

positive.date = d 

d= []
# Use re.findall to extract the date of negative reviews
for x in negative.date:
  extracted_date = re.findall( "^(Reviewed\s+in\s+India\s+on)\s+(\d{1,2}\s[a-zA-Z]+\s\d{4})$",  x )[0][1]
  date_object = datetime.strptime(  extracted_date, date_format_2).date().strftime('%Y-%m-%d')
  d.append(date_object)

negative.date = d 



# Use re.findall to extract the rating of positive reviews
r=  []
for x in positive.star:
  extracted_rating = re.findall(star, x)[0]
  r.append(extracted_rating)

positive.star = r 

# Use re.findall to extract the rating of negative reviews 
r= []
for x in negative.star:
  extracted_rating = re.findall(star, x)[0]
  r.append(extracted_rating)

negative.star = r 


positive.to_csv("positive_amazon.csv")
negative.to_csv("critical_amazon.csv")


  

