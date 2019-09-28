import time
import mysql.connector
from bs4 import BeautifulSoup
import requests
import pandas as pd
from itertools import cycle
from multiprocessing import Pool


#MySql connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shahab",
    database="j")

# we check the database connection
if mydb:
    print("connected")
else:
    print("NOT connected")

mycursor = mydb.cursor()
df = pd.read_csv("authors.csv") #authors CSV file
df = df.dropna(axis=0)
df.info()

authors_array = df.loc[0:281465, "author_id"].values
authors_list = authors_array.tolist()
print(len(authors_list))


df_ua = pd.read_csv("ua.csv")

k = []
a = df_ua.values.tolist()
for i in a:
    k.append(i[0])

useragents = cycle(k)
# authorsids = cycle(authors_list)

def scrape(auth):
    print(auth)
    z = 0
    print(time.time())
    for i in range(1):
        url = "https://www.scopus.com/authid/detail.uri?authorId={}".format(auth)


        try:
            response = requests.get(url,headers={'User-Agent': next(useragents)})
            print("Request Successful")
            print(datetime.datetime.now())
        except:
            time.sleep(5)
            break


        while True:
            response = requests.get(url,headers={'User-Agent': next(useragents)})
            page_soup = BeautifulSoup(response.content, "html.parser")
            first = page_soup.findAll("h2", {"class" : "wordBreakWord"})
            if len(first) > 0:
                full_name = first[0].text.replace(",\xa0", " ").replace("\r", " ").replace("Is this you? Claim profile  Opens in new window", " ").strip()
                break
            else:
                time.sleep(5)
                continue






        try:
            other_names = page_soup.findAll("div", {"id" : "otherNameFormatBadges"})
            span_list = other_names[0].findAll("span")
            other_names = []
            for i in span_list:
                other_names.append(i.text.strip())
            others = "|".join(other_names).replace("|", "| ")
            t = len(other_names)
        except:
            others= "NA"
            t = 0


        try:
            university = page_soup.findAll("div", {"class" : "authAffilcityCounty"})[0].text.strip().replace("\r", " ")
        except:
            university = "NA"

        try:
            subject_areas = page_soup.findAll("span", {"class" : "badges"})
            subject_areas = subject_areas[t:]


            areas = []
            for i in range(len(subject_areas)):
                 areas.append(subject_areas[i].text.strip().replace(",", ""))

            subjects = ",".join(areas).replace(",", ", ")
        except:
            subjects="NA"

        try:
            documents_by_author = page_soup.findAll("span", {"class" : "fontLarge pull-left"})[0].text
            if len(documents_by_author) > 0:
                pass
            else:
                documents_by_author = 0
        except:
            documnets_by_author = 0

        try:
            total_citation_number = page_soup.findAll("span", {"class" : "fontLarge darkGrayText"})[0].text
            if len(total_citation_number) > 0:
                pass
            else:
                total_citation_number = 0
        except:
            total_citation_number = 0

        try:
            total_document = page_soup.findAll("div", {"class" : "lightGreyText"})[0].findAll("span")[1].text
            if len(total_document) > 0:
                pass
            else:
                total_document = 0

        except:
            total_document = 0

        try:
            h_index = page_soup.select("span[class='fontLarge']")[0].text


        except:
            h_index = 0

        print("sql")

        sql = """INSERT INTO authors(auth, full_name, others, university, subjects, documnet_by_author, total_citation_number, total_document, h_index) VALUES (
        "{}","{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")""".format(str(auth), full_name, others, university, subjects, int(documents_by_author),
                                                               int(total_citation_number), int(total_document), int(h_index))


        try:
            mycursor.execute(sql)
            mydb.commit()
        except:
            mydb.rollback()
            print("NOT connected")
        z += 1
        print("we have collected: {} number(s) so far".format(z))
        if auth == authors_list[-1]:
            break
        else:
            pass
        time.sleep(5) # 5 seconds sleep
    print("finished")


if __name__ == "__main__":
    p = Pool(6) # we can change the number of processors
    p.map(scrape, authors_list)
    p.close()
    p.join()
    print("done")
