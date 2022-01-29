from typing import List

class Content:
    profile:str
    title:str
    artwork:str
    date:str
    genres:List[str]
    age_rating:str
    details:str

class Video(Content):
    audio:str
    length:int

class Season:
    url:str
    episodes:List[Video]

class Serie(Content):
    episode_number:int
    seasons:List[Season]
    def __init__(self):
        self.seasons=[]
    
