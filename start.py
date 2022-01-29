from jsonpickle import encode
from scrape import get_all_movies,get_all_series

movies=get_all_movies()
series=get_all_series()

result={}
result['movies']=[obj.__dict__ for obj in movies]
result['series']=[obj.__dict__ for obj in series]


with open("db.json", "w") as w:
    w.write(encode(result, unpicklable=False,indent=4))  
    
