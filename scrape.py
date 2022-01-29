from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from models import Season, Video, Serie
import re

MOVIES_URL="https://www.starz.com/ar/en/view-all/blocks/1523534"
SERIES_URL="https://www.starz.com/ar/en/view-all/blocks/1523514"

driver = webdriver.Chrome()
driver.implicitly_wait(12)
driver.maximize_window()

def get_all_movies()->List[Video]:
    driver.get(MOVIES_URL)
    full_movies_list=[]
    urls=set(map(lambda a: a.get_attribute('href'),driver.find_elements(By.CSS_SELECTOR,"article div a")))
    for url in urls:
        full_movies_list.append(get_full_movie(url))
    return full_movies_list
        

def get_full_movie(url:str)->Video:
    driver.get(url)
    movie=Video()
    movie.artwork=driver.find_element(By.TAG_NAME,"starz-picture-sources picture source").get_attribute('srcset')
    movie.title=driver.find_element(By.ID,'moviesDetailsH1').text.replace('Watch ','').replace(' Online','')
    metadata=driver.find_element(By.CSS_SELECTOR,"ul.meta-list.text-uppercase").find_elements(By.TAG_NAME,'li')
    show_more_button=driver.find_element(By.CSS_SELECTOR,'button.more-link')
    if show_more_button.is_displayed():
        show_more_button.click()
    movie.details=driver.find_element(By.CSS_SELECTOR,'div.logline.truncate-container').find_element(By.TAG_NAME,'p').text
    movie.age_rating=metadata[0].text
    movie.length=int(metadata[1].text.split(" ")[0])
    movie.genres=re.split(r',\s*',metadata[2].text)
    movie.date=metadata[3].text
    movie.audio=metadata[4].text if len(metadata)==5 else None
    movie.profile=url
    return movie

def get_all_series()->List[Serie]:
    driver.get(SERIES_URL)
    series_ul=driver.find_elements(By.CSS_SELECTOR,"article div a") #chequear si podemos evitar el set
    urls=set()
    for element in series_ul:
        urls.add(element.get_attribute('href'))
    full_series_list=[]
    for url in urls:
        full_series_list.append(get_full_serie(url))
    return full_series_list

def get_full_serie(url:str)->Serie:          
    driver.get(url)
    serie=Serie()
    serie.artwork=driver.find_element(By.TAG_NAME,"starz-picture-sources picture source").get_attribute('srcset')
    serie.title=driver.find_element(By.ID,'seriesDetailsH1').text
    [age_rating,episode_number,genres,year]=driver.find_element(By.CSS_SELECTOR,"ul.meta-list.text-uppercase").find_elements(By.TAG_NAME,'li')
    show_more_button=driver.find_element(By.CSS_SELECTOR,'button.more-link')
    if show_more_button.is_displayed():
        show_more_button.click()
    serie.details=driver.find_element(By.CSS_SELECTOR,'div.logline.truncate-container p').text
    serie.age_rating=age_rating.text
    serie.episode_number=int(episode_number.text.split(' ',1)[0])
    serie.genres=re.split(r',\s*',genres.text)
    serie.date=year.text.split(' ',1)[0]
    serie.profile=url
    for season_url in list(map(lambda a: a.get_attribute('href'),driver.find_elements(By.CSS_SELECTOR,'div.season-number a'))) :
        season=Season()
        season.url=season_url
        season.episodes=get_all_episodes(season.url)
        serie.seasons.append(season) 
    return serie
    
def get_all_episodes(url:str):
    episode_list=[]
    driver.get(url)
    episodes=driver.find_elements(By.CSS_SELECTOR,'a.episode-link')
    for epi in episodes:
        epi.click()
        episode_list.append(get_full_episode())
        driver.back()
    return episode_list

def get_full_episode():
    episode=Video()
    episode.artwork=driver.find_element(By.CSS_SELECTOR,'picture source').get_attribute('srcset')
    episode.title=driver.find_element(By.CSS_SELECTOR,'h5.episode-title').get_attribute('innerHTML')
    [age,length,year,audio]=driver.find_elements(By.CSS_SELECTOR,'section.episode-details-container div.metadata ul.meta-list li')
    episode.age_rating=age.get_attribute('innerHTML')
    episode.length=int(length.get_attribute('innerHTML').split(" ")[0])
    episode.date=year.get_attribute('innerHTML')
    episode.audio=audio.get_attribute('innerHTML')
    episode.profile=driver.current_url
    show_more_button=driver.find_element(By.CSS_SELECTOR,'button.more-link')
    if show_more_button.is_displayed():
        show_more_button.click()
    episode.details=driver.find_element(By.CSS_SELECTOR,'div.logline.truncate-container p').text
    return episode