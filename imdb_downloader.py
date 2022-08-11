import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

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

def get_roles(soup):
    try:
        roles_arr = []
        roles = soup.find("div", {"class": "filmo-category-section"})
        for role in roles.find_all("div", recursive=False):
            if len(role.find_all("a", {"class": "in_production"})) == 0:
                res = ""
                for val in role.find_all(text=True, recursive=False):
                    if val.strip() != "":
                        res = val.strip()
                roles_arr.append(res + " in " + str(role.find("a").text))
                if len(roles_arr) > 2:
                    break
        return roles_arr
    except:
        return None

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
        return res
    except:
        return None

def get_spouse(soup):
    try:
        spouse = soup.find("div", {"id": "details-spouses"}).find("a").text
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
        return str(", ".join(res))
    except:
        return None

def get_children(soup):
    try:
        res = []
        arr = soup.find("div", {"id": "details-children"}).find_all(text = True, recursive = True)
        for val in arr:
            if (val.strip() != "") and (val.strip() != "Children:") and (val.strip() != "|"):
                res.append(val.strip())
        return " | ".join(res)
    except:
        return None

def get_parents(soup):
    try:
        res = []
        arr = soup.find("div", {"id": "details-parents"}).find_all(text = True, recursive = True)
        for val in arr:
            if (val.strip() != "") and (val.strip() != "Parents:") and (val.strip() != "|"):
                res.append(val.strip())
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
        return " | ".join(res)
    except:
        return None

def main():
    names = ["Ian Somerhalder", "Selena Gomez", "David Henry", "Adam Driver", "Adam Sandler"]
    columns = ["Person name", "URL", "Role 1", "Role 2", "Role 3", "Video", "Actor description",
                                "Other works", "Alternate names", "Spouse", "Children", "Parents", "Personal quotes",
                                "Trivia", "Trademark", "Nickname"]
    df_main = pd.DataFrame(columns = columns)
    for name in tqdm(names):
        url = get_url(name)
        headers = {"Accept-Language": "en,en-gb;q=0.5"}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, features="lxml")
        d = {columns[0]: [name], columns[1]: [url], columns[2]: [get_roles(soup)[0]], columns[3]: [get_roles(soup)[1]], 
            columns[4]: [get_roles(soup)[2]], columns[5]: [get_video_url(soup)], columns[6]: [get_bio(url)], 
            columns[7]: [get_other_works(soup)], columns[8]: [get_alternate_names(soup)], columns[9]: [get_spouse(soup)],
            columns[10]: [get_children(soup)], columns[11]: [get_parents(soup)], columns[12]: [get_quotes(soup)],
            columns[13]: [get_trivia(soup)], columns[14]: [get_trademark(soup)], columns[15]: [get_nickname(soup)]}
        df_temp = pd.DataFrame.from_dict(d)
        df_main = pd.concat([df_main, df_temp], ignore_index = True)
    df_main.to_excel("output.xlsx")
    return "Done!"

if __name__ == "__main__":
    main()