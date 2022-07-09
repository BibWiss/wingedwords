from bs4 import BeautifulSoup
import pandas as pd
import datetime

with open('html/input_a.html','r', encoding='utf-8') as f:
    html_doc = f.read()

parent_path = "https://de.wikipedia.org/wiki/Liste_gefl%C3%BCgelter_Worte/A"
start_number = 1

soup = BeautifulSoup(html_doc, 'html.parser')
toc_listings = soup.find_all("li", class_="toclevel-1")

# dates

today = datetime.date.today()
day1 = today + datetime.timedelta(days=6)
print(day1)

# create columns and add data

dates = []
time = []
tweet_content = []

for listing in toc_listings:
    toc_link = parent_path + listing.find_next("a").get('href')
    word_name = listing.find("span", class_="toctext").string
    tweet_content.append('Geflügeltes Wort des Tages: ' + word_name + ' (#' + str(start_number) + '). Zur Entstehung: ' + toc_link)
    dates.append(day1)
    time.append(datetime.time(12).isoformat(timespec='minutes'))
    start_number += 1
    day1 = day1 + datetime.timedelta(days=1)

#print(tweet_content[3], dates[3], time[3])

# save data as a dataframe

columns = ["Date", "time", "Tweet content", "image attachment", "latitude", "longitude"]
df = pd.DataFrame(data=zip(dates,time,tweet_content),columns=columns[0:3])
df[columns[3]] = ""
df[columns[4]] = ""
df[columns[5]] = ""
df.drop(df.tail(1).index,inplace=True)
print(df)

# create tsv from df

df.to_csv('wingedwords_output.tsv', sep="\t", index=False)