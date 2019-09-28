import mysql.connector 
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from itertools import cycle
import traceback
import pandas as pd
from multiprocessing import Pool

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shahab",
    database="pubs2")

df_ua = pd.read_csv("ua.csv")

k = []
a = df_ua.values.tolist()
for i in a:
    k.append(i[0])

useragents_global = cycle(k)

def url_search(journal_name):
    """It searches all the links and shows the appropriate link"""
    journal_name_new = journal_name.replace(" ", "+")
    f = "https://www.scimagojr.com/journalsearch.php?q={}".format(journal_name_new)
    user = next(useragents_global)
    a = "wrong"
    fh = 0
    while a != "right":
        try:
            response = requests.get(f,headers={'User-Agent': user})
            a = "right"
        except:
            if fh <= 10:
                time.sleep(10)
                fh += 1
                continue   
            else:
                return "NA"
    page_soup = BeautifulSoup(response.content, "html.parser")
    search = page_soup.findAll("div", {"class":"search_results"})
    search_new = search[0].findAll("a")
    num_of_search = len(search_new)
    if num_of_search == 0:
        return "NA"
    else:
        links = []
        for k in range(num_of_search):
            if search_new[k].span.text.lower() == journal_name:
                links.append("https://www.scimagojr.com/" + search_new[k]["href"])
                break
            else:
                continue
        if len(links) == 0:
            return "NA"
        else:
            link = links[0]
            return link
df = pd.read_csv("a.csv")

journals = df.loc[:, "journal"].tolist()

mycursor = mydb.cursor()


def scimagojr(jour):
    jour = jour.lower()
    url = url_search(jour)
    print(url)
    if url != "NA":
        df_useragents = pd.read_csv("ua.csv")
        w = []
        b = df_useragents.values.tolist()
        for j in b:
            w.append(j[0])
        useragents_global = cycle(w)
        user_agent = next(useragents_global)
        m = 0
        a = "wrong"
        while a != "right":
            try:
                response = requests.get(url,headers={'User-Agent': user_agent})
                a = "right"
                m += 1
            except:
                if m == 10:
                    break
                continue

        # table 1 
        page_soup = BeautifulSoup(response.content, "html.parser")
        journal_name_list = page_soup.findAll("div", {"class":"journaldescription colblock"})
        journal_name = journal_name_list[0].h1.text.strip()
        table = page_soup.findAll("table")
        tr_list0 = table[0].findAll("tr")
        td_list0 = tr_list0[0].findAll("td")
        country_name = td_list0[1].a.text.strip()
        h_index = page_soup.findAll("div", {"class" : "hindexnumber"})[0].text
        publisher_name = tr_list0[2].findAll("td")[1].a.text.strip()
        publication_type_name = tr_list0[3].findAll("td")[1].text.strip()
        issn = tr_list0[4].findAll("td")[1].text
        coverage = tr_list0[5].findAll("td")[1].text
        scope = tr_list0[6].findAll("td")[1].text.replace('"', '/').strip()
        print(coverage)
        sql = """INSERT INTO pubs2.journal(journal_name, country, publisher, publication_type, issn, coverage, scope, h_index) VALUES (
        "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")""".format(journal_name, country_name, publisher_name, publication_type_name, 
                                                           issn, coverage, scope, h_index)


        try:
            mycursor.execute(sql)
            mydb.commit()
        except Exception as e:
            print(e)
            print("non connected 1")
            mydb.rollback() 
            return "error"
        sql = "SELECT LAST_INSERT_ID()"
        try:
            mycursor.execute(sql)
            result1 = mycursor.fetchone()
            journal_id = result1[0]
        except:
            mydb.rollback()
            mydb.close()
            journal_id = -1

        # table 2 
        td_area_category = tr_list0[1].findAll("td")[1]
        a_list = td_area_category.findAll("a")
        area = []
        category = []
        for i in a_list:
            ln = i["href"]
            if "journalrank.php?area=" in ln:
                area.append(i.text)
            else:
                category.append(i.text)
        area_str = "| ".join(area)
        category_str = "| ".join(category)
        sql = """INSERT INTO pubs2.area(journal_id, areas, categories) VALUES ("{}", "{}", "{}")""".format(journal_id, area_str, category_str)
        try:
            mycursor.execute(sql)
            mydb.commit()
        except:
            print("non connected 2")
            mydb.rollback()

        # table 3
        tr_list1 = table[1].findAll("tr")
        for tr in tr_list1[1:]:
            a = tr.findAll("td")
            cat = a[0].text
            year = a[1].text
            quartile = a[2].text
            sql = """INSERT INTO pubs2.quartile(journal_id, categories, year, quartile) VALUES ("{}", "{}", "{}", "{}")""".format(journal_id, cat, year, quartile)
            try:
                mycursor.execute(sql)
                mydb.commit()
            except:
                print("non connected 3")
                mydb.rollback()


        # table 4
        tr_list2 = table[2].findAll("tr")

        years_sjr = []
        sjrs = []


        for tr in tr_list2[1:]:
            a = tr.findAll("td")
            year = a[0].text
            sjr = a[1].text
            years_sjr.append(year)
            sjrs.append(sjr)
        for t in range(len(years_sjr)):
            sql = """INSERT INTO pubs2.sjr(journal_id, year, sjr) VALUES ("{}", "{}", "{}")""".format(journal_id, years_sjr[t], sjrs[t])
            try:
                mycursor.execute(sql)
                mydb.commit()
            except:
                print("non connected 4")
                mydb.rollback()

        # table 5   
        tr_list3 = table[3].findAll("tr")

        years_year = []
        citations_4 = []
        citations_3 = []
        citations_2 = []

        for tr in tr_list3[1:]:
            a = tr.findAll("td")

            if "4" in a[0].text:     
                year = a[1].text
                citation_per_doc_4 = a[2].text
                years_year.append(year)
                citations_4.append(citation_per_doc_4)



            if "3" in a[0].text:
                citation_per_doc_3 = a[2].text
                citations_3.append(citation_per_doc_3)


            if "2" in a[0].text:
                citation_per_doc_2 = a[2].text
                citations_2.append(citation_per_doc_2)


        for y in range(len(years_year)):
            sql = """INSERT INTO pubs2.citation_per_document(journal_id, year, citation_2, citation_3, citation_4) VALUES ("{}", "{}", "{}", "{}", "{}")""".format(journal_id, years_year[y], citations_2[y], citations_3[y], 
            citations_4[y])
            try:
                mycursor.execute(sql)
                mydb.commit()
            except:
                print("non connected 5")
                mydb.rollback()


        # table 6
        tr_list4 = table[4].findAll("tr")


        year_self_total = []
        self_cites = []
        total_cites = []


        for tr in tr_list4[1:]:
            a = tr.findAll("td")
            if "Self" in a[0].text:
                year = a[1].text
                self_cite = a[2].text
                year_self_total.append(year)
                self_cites.append(self_cite)
            if "Total" in a[0].text:
                total_cite = a[2].text
                total_cites.append(total_cite)

        for u in range(len(year_self_total)):
            sql = """INSERT INTO pubs2.total_self_cite(journal_id, year, self_cite, total_cite) VALUES ("{}", "{}", "{}", "{}")""".format(journal_id, year_self_total[u], self_cites[u], total_cites[u])
            try:
                mycursor.execute(sql)
                mydb.commit()
            except:
                print("non connected 6")
                mydb.rollback()

        # table 7
        tr_list5 = table[5].findAll("tr")

        year_external = []
        cites_per_docs_ext = []
        cites_per_docs = []


        for tr in tr_list5[1:]:
            a = tr.findAll("td")
            if "External" in a[0].text:
                year = a[1].text
                year_external.append(year)
                external_cite_per_doc = a[2].text
                cites_per_docs_ext.append(external_cite_per_doc)
            else:
                cite_per_doc = a[2].text
                cites_per_docs.append(cite_per_doc)
    #     print(cites_per_docs)
    #     print(cites_per_docs_ext)
        for z in range(len(year_external)):
            sql = """INSERT INTO pubs2.external_cite_per_doc_right(journal_id, year, cites_per_doc, cites_per_doc_ext) VALUES ("{}", "{}", "{}", "{}")""".format(journal_id, year_external[z], cites_per_docs[z], cites_per_docs_ext[z])
            try:
                mycursor.execute(sql)
                mydb.commit()
            except:
    #             print(e)
                print("non connected 7")
                mydb.rollback()

        # table 8
        tr_list6 = table[6].findAll("tr")


        year_int = []
        int_collab = []


        for tr in tr_list6[1:]:
            a = tr.findAll("td")
            year = a[0].text
            international_collaboration = a[1].text
            year_int.append(year)
            int_collab.append(international_collaboration)

        for p in range(len(year_int)):
            sql = """INSERT INTO pubs2.international_collaboration_right(journal_id, year, int_collab) VALUES ("{}", "{}", "{}")""".format(journal_id, year_int[p], int_collab[p])
            try:
                mycursor.execute(sql)
                mydb.commit()
            except Exception as e:
                print(e)
                print("non connected 8")
                mydb.rollback()


        # table 9
        tr_list7 = table[7].findAll("tr")


        year_citable_list = []
        citable_doc_list = []
        non_citable_doc_list = []



        for tr in tr_list7[1:]:
            a = tr.findAll("td")
            if "Non" in a[0].text:
                year = a[1].text
                year_citable_list.append(year)
                non_citable_document = a[2].text
                non_citable_doc_list.append(non_citable_document)
            else:
                citable_document = a[2].text
                citable_doc_list.append(citable_document)

        for a in range(len(year_citable_list)):
            sql = """INSERT INTO pubs2.citable_documents(journal_id, year, citable_doc, non_citable_doc) VALUES ("{}", "{}", "{}", "{}")""".format(journal_id, year_citable_list[a], citable_doc_list[a], non_citable_doc_list[a])
            try:
                mycursor.execute(sql)
                mydb.commit()
            except:
                print("non connected 9")
                mydb.rollback()


        # table 10       
        tr_list8 = table[8].findAll("tr")

        year_cited = []
        cited_doc_list = []
        non_cited_doc_list = []


        for tr in tr_list8[1:]:
            a = tr.findAll("td")
            if "Unc" in a[0].text:
                year = a[1].text
                year_cited.append(year)
                uncited_document = a[2].text
                non_cited_doc_list.append(uncited_document)
            else:
                cited_document = a[2].text
                cited_doc_list.append(cited_document)

        for s in range(len(year_cited)):
            sql = """INSERT INTO pubs2.cited_documents_rightt(journal_id, year, cited_doc, non_cited_doc) VALUES ("{}", "{}", "{}", "{}")""".format(journal_id, year_cited[s], cited_doc_list[s], non_cited_doc_list[s])
            try:
                mycursor.execute(sql)
                mydb.commit()
            except:
                print("non connected 10")
                mydb.rollback()

        time.sleep(11)

    else:
        print("Nothing available")

            
    
    
            
            
            
    
            
            
    
    
    
    
    
            
                
        

        
            
            
    
            
    
    
    
    

error_list = []
def gen_func(jour_name):
    try:
        scimagojr(jour_name)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    p = Pool(6) # we can change the number of processors
    p.map(gen_func, journals)
    p.close()
    p.join()
    print("done")

