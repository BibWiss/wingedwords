from bs4 import BeautifulSoup
import pandas as pd
import datetime
import csv
import string

# basic information, suffix used to loop through files

base_url = 'https://de.wikipedia.org/wiki/Liste_gefl%C3%BCgelter_Worte/' 
suffix = list(string.ascii_uppercase)
start_number = 1

# create columns

dates = []
time = []
tweet_content = []

# dates

today = datetime.date.today()
day1 = today + datetime.timedelta(days=1)

# start loop

for letter in suffix:
    with open('html/input_' + letter + '.html','r', encoding='utf-8') as f:
        html_doc = f.read()
    
    parent_path = "https://de.wikipedia.org/wiki/Liste_gefl%C3%BCgelter_Worte/" + letter
    
    soup = BeautifulSoup(html_doc, 'html.parser')
    toc_listings = soup.find_all("li", class_="toclevel-1")
    
    for listing in toc_listings:
        toc_link = parent_path + listing.find_next("a").get('href')
        word_name = listing.find("span", class_="toctext").string
        if word_name != "Einzelnachweise":
            content = '#WingedWord des Tages: \"' + word_name + '\" (Nr.' + str(start_number) + '). Zur Entstehung: ' + toc_link
            tweet_content.append(content)
            dates.append(day1)
            time.append(datetime.time(12).isoformat(timespec='minutes'))
            start_number += 1
            day1 = day1 + datetime.timedelta(days=1)

# save data as a dataframe

columns = ["Date", "time", "Tweet content", "image attachment", "latitude", "longitude"]
df = pd.DataFrame(data=zip(dates,time,tweet_content),columns=columns[0:3])
df[columns[3]] = ""
df[columns[4]] = ""
df[columns[5]] = ""

# shuffle tweet content:
# df['Tweet content'] = df["Tweet content"].sample(frac=1).values

print(df)

# create tsv from df

df.to_csv('wingedwords_output.tsv', sep="\t", index=False, quoting=csv.QUOTE_NONE)