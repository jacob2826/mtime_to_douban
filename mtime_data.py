import requests
from bs4 import BeautifulSoup
import re
import json


def run():

    data = open("mtime.csv", "a")
    headStr = "title,final,music,picture,director,story,show,impression,comment,date,method"
    data.write(headStr)
    # 需要通过浏览器获取自己的cookie
    cookies = {'loginEmail': 'abc%40gmail.com'}

    url = 'http://my.mtime.com/movie/seen/?&pageIndex='

    page = 1
    while (page <= 46):
        r = requests.get(url + str(page), cookies=cookies)
        r.encoding = 'UTF-8'
        content = r.text

        soup = BeautifulSoup(content, 'html.parser')

        seen = soup.find('div', id='seenMoviesRegion')
        # print(seen)

        movies = seen.find_all('ul', class_='clearfix', limit=10)
        
        movieIdList = []
        pattern = re.compile(r'\d+')
        for item in movies:
            link = item.find('a', class_='movie_75img').get('href')
            
            link = str(link)
            movieIdList.append(pattern.search(link).group())
        
        for id in movieIdList:
            comment = request_comment(cookies, id)
            commentJson = json.loads(comment[comment.index('=')+1:comment.rindex(';')])
            
            try:
                title = commentJson['value']['movieTitle']
                comment = commentJson['value']['userLastComment']

                ratinng = Rating()
                ratinng.rating = commentJson['value']['userRating']['Rating']
                ratinng.music = commentJson['value']['userRating']['Rother']
                ratinng.picture = commentJson['value']['userRating']['Rpicture']
                ratinng.director = commentJson['value']['userRating']['Rdirector']
                ratinng.story = commentJson['value']['userRating']['Rstory']
                rating.show = commentJson['value']['userRating']['Rshow']
                ratinng.impression = commentJson['value']['userRating']['Rtotal']
                
                print(title)
                date, method = request_method(cookies, id)
                write_to_file(data, title, rating, comment, date, method)
            except TypeError:
                print("Cannot access movie for movieId: " + id)

        page = page + 1
    data.close()

def write_to_file(data, title, rating, comment, date, method):
    data = open("mtime.csv", "a")
    title = str(title)
    
    finalRating = str(rating.rating)
    music = str(rating.music)
    picture = str(rating.picture)
    driector = str(rating.director)
    story = str(rating.story)
    show = str(rating.story)
    impression = str(rating.impression)

    comment = str(comment)
    date = str(date)
    method = str(method)
    item = title + "," + finalRating + "," + music + "," + picture + ","
        + driector + "," + story + ","
        + show + "," + impression + ","
        + comment + "," + date + "," + method + "\n"
    
    data.write(item)


# 获取观影方式
def request_method(cookies, movieId):
    url = 'http://service.mtime.com/database/databaseService.m?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Community.Controls.CommunityPages.DatabaseService&Ajax_CallBackMethod=GetAllMoviegoingLogs&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Fmovie.mtime.com%2FmovieId%2F&Ajax_CallBackArgument0=movieId'
    newurl = url.replace("movieId", movieId, 2)

    r = requests.get(newurl, cookies=cookies)
    raw = r.text

    try: 
        dateStart = raw.index("年")
        dateEnd = raw.index("日")
        date = raw[dateStart - 4:dateEnd + 1]
    except ValueError:
        date = 'null'
        print("没有观影方式")

    try:
        methodStart = raw.index("class=\\\"ml6 mr6\\\">")
        methodEnd = raw.index("</a>")
        method = raw[methodStart + 18:methodEnd]
    except ValueError:
        method = 'null'
        print("没有观影方式")

    print(date)
    print(method)
    return date, method


# 获取评论的详细信息
def request_comment(cookies, movieId):
    url = 'http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackMethod=GetMovieOverviewRating&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Fmovie.mtime.com%2FmovieId%2F&Ajax_CallBackArgument0=movieId'
    newurl = url.replace("movieId", movieId, 2)

    r = requests.get(newurl, cookies=cookies)
    # print(r.text)
    return r.text

if __name__ == "__main__":
    run()


class Rating:
    rating = 0.0
    music = 0.0
    picture = 0.0
    director = 0.0
    story = 0.0
    show = 0.0
    impression = 0.0
    
