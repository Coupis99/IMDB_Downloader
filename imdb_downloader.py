from operator import index
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import time 
from openpyxl import load_workbook
from os.path import exists


def get_url(name):
    try:
        query = "+".join(name.split())
        r = requests.get(f"https://www.imdb.com/search/name/?name={query}")
        soup = BeautifulSoup(r.text, 'html.parser')
        apendix = soup.find("div", {"class": "lister-item mode-detail"}).find("a").get("href")
        url = "https://www.imdb.com" + apendix
        return url
    except:
        return None

def get_born(soup):
    try:
        res_arr = []
        arr = soup.find("div", {"id": "name-born-info"}).find_all(text = True, recursive = True)
        for val in arr:
            if val.strip() != "" and val.strip() != "Born:":
                res_arr.append(val.strip())
        if len(res_arr) != 0:
            return str(" ".join(res_arr))
        else:
            return None
    except:
        return None

def get_roles(soup):
    roles_arr = [None, None, None]
    try:
        roles = soup.find("div", {"id": "jumpto"}).find_all("a")
        if len(roles) == 0:
            return roles_arr
        leng = 0
        if len(roles) > 2:
            leng = 3
        else:
            leng = len(roles)
        for i in range(leng):
            roles_arr[i] = roles[i].text
        return roles_arr
    except:
        return roles_arr

def get_video_url(soup):
    try:
        apendix = soup.find("div", {"class": "heroWidget"}).find("a").get("href")
        video_url = "https://www.imdb.com" + apendix
        return video_url
    except:
        return None

def get_bio(url):
    try:
        headers = {"Accept-Language": "en,en-gb;q=0.5"}
        r = requests.get(url +"/bio", headers=headers)
        soup = BeautifulSoup(r.text, features="lxml")
        bio = soup.find("div", {"class": "soda odd"}).find("p").text.strip()
        if bio == "":
            return None
        return bio
    except:
        return None

def get_other_works(soup):
    try:
        res = ""
        arr = soup.find("div", {"id": "details-other-works"}).find_all(text = True, recursive = False)
        for val in arr:
            if val.strip() != "":
                res = val.strip()
                break
        if res == "":
            return None
        return res
    except:
        return None

def get_spouse(soup):
    try:
        spouse = soup.find("div", {"id": "details-spouses"}).find("a").text
        if spouse == "":
            return None
        return spouse
    except:
        return None

def get_alternate_names(soup):
    try:
        res = []
        akas = soup.find("div", {"id": "details-akas"}).find_all(text = True, recursive = False)
        for val in akas:
            if val.strip() != "":
                res.append(val.strip())
        if res == []:
            return None
        return str(", ".join(res))
    except:
        return None

def get_children(soup):
    try:
        res = []
        arr = soup.find("div", {"id": "details-children"}).find_all(text = True, recursive = True)
        for val in arr:
            if (val.strip() != "") and (val.strip() != "Children:") and (val.strip() != "|") and (val.strip() != "»") and (val != "See more"):
                res.append(val.strip())
        if res == []:
            return None
        return " | ".join(res)
    except:
        return None

def get_parents(soup):
    try:
        res = []
        arr = soup.find("div", {"id": "details-parents"}).find_all(text = True, recursive = True)
        for val in arr:
            if (val.strip() != "") and (val.strip() != "Parents:") and (val.strip() != "|") and (val.strip() != "»") and (val != "See more"):
                res.append(val.strip())
        if res == []:
            return None
        return " | ".join(res)
    except:
        return None

def get_quotes(soup):
    try:
        res = []
        arr = soup.find("div", {"id": "dyk-personal-quote"}).find_all(text = True, recursive = True)
        for val in arr:
            if (val.strip() != "") and (val.strip() != "Personal Quote:") and (val.strip() != "»") and (val != "See more"):
                res.append(val.strip())
        if res == []:
            return None
        return " | ".join(res)
    except:
        return None

def get_trivia(soup):
    try:
        res = []
        arr = soup.find("div", {"id": "dyk-trivia"}).find_all(text = True, recursive = True)
        for val in arr:
            if (val.strip() != "") and (val.strip() != "Trivia:") and (val.strip() != "»") and (val != "See more"):
                res.append(val.strip())
        if res == []:
            return None
        return " | ".join(res)
    except:
        return None

def get_trademark(soup):
    try:
        res = []
        arr = soup.find("div", {"id": "dyk-trademark"}).find_all(text = True, recursive = True)
        for val in arr:
            if (val.strip() != "") and (val.strip() != "Trademark:") and (val.strip() != "»") and (val != "See more"):
                res.append(val.strip())
        if res == []:
            return None
        return " | ".join(res)
    except:
        return None

def get_nickname(soup):
    try:
        res = []
        arr = soup.find("div", {"id": "dyk-nickname"}).find_all(text = True, recursive = True)
        for val in arr:
            if (val.strip() != "") and (val.strip() != "Nickname:") and (val.strip() != "»") and (val != "See more"):
                res.append(val.strip())
        if res == []:
            return None
        return " | ".join(res)
    except:
        return None

def create_excel(df, file):
    writer = pd.ExcelWriter(file)
    df.to_excel(writer, sheet_name="Screenwriters", index=False)
    writer.save()
    return "Excel created"

def update_excel(df ,file):
    reader = pd.read_excel(file, engine='openpyxl')
    book = load_workbook(file)
    writer = pd.ExcelWriter(file, engine='openpyxl') 
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
    df.to_excel(writer, sheet_name = 'Screenwriters', index=False, header=False, startrow=len(reader)+1)
    writer.save()
    return "Excel updated"

def main():
    wait_time = 60
    file = "output2.xlsx"
    miss_file = "miss_file.xlsx"
    names = []
    names_df = pd.read_excel("Screenwriters.xlsx")
    for val in names_df["Screenwriters"]:
        names.append(val)
    columns = ["Person name", "URL", "Born", "Role 1", "Role 2", "Role 3", "Video", "Actor description",
    "Other works", "Alternate names", "Spouse", "Children", "Parents", "Personal quotes",
    "Trivia", "Trademark", "Nickname"]
    df_main = pd.DataFrame(columns = columns)
    if not exists(file):
        create_excel(df_main, file)
    column = ["Missing names"]
    miss_df = pd.DataFrame(columns=column)
    if not exists(miss_file):
        create_excel(miss_df, miss_file)
    start_time = time.time()
    for name in tqdm(names):
        url = get_url(name)
        if url != None:
            headers = {"Accept-Language": "en,en-gb;q=0.5"}
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, features="lxml")
            d = {columns[0]: [name], columns[1]: [url], columns[2]: [get_born(soup)], columns[3]: [get_roles(soup)[0]], columns[4]: [get_roles(soup)[1]], 
                columns[5]: [get_roles(soup)[2]], columns[6]: [get_video_url(soup)], columns[7]: [get_bio(url)], 
                columns[8]: [get_other_works(soup)], columns[9]: [get_alternate_names(soup)], columns[10]: [get_spouse(soup)],
                columns[11]: [get_children(soup)], columns[12]: [get_parents(soup)], columns[13]: [get_quotes(soup)],
                columns[14]: [get_trivia(soup)], columns[15]: [get_trademark(soup)], columns[16]: [get_nickname(soup)]}
            df_temp = pd.DataFrame.from_dict(d)
            df_main = pd.concat([df_main, df_temp], ignore_index = True)
        else:
                miss_df.loc[""] = str(name)
                update_excel(miss_df, miss_file)
        end_time = time.time()
        print(end_time - start_time)
        print(df_main)
        if end_time - start_time > wait_time:
            update_excel(df_main, file)
            print("Written")
            df_main = pd.DataFrame(columns = columns)
            start_time = time.time()
    update_excel(df_main, file)
    print("Finished!")
    return "Done!"

if __name__ == "__main__":
    main()