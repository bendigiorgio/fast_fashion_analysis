from datetime import date
from logging import error
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession


product_price = []
product_name = []
product_brand = []
product_ranking = []
brands = ["Shein","Zara","H&M","GU","GRL"]
brand_url = ["https://jp.shein.com/trends/New-in-Trends-sc-00654187.html?ici=jpen_tab01navbar02&scici=navbar_WomenHomePage~~tab01navbar02~~2~~itemPicking_00654187~~~~0&src_module=topcat&src_tab_page_id=page_home1659095785592&src_identifier=fc%3DWomen%60sc%3DTRENDS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar02%60jc%3DitemPicking_00654187&srctype=category&userpath=category-TRENDS","https://www.zara.com/jp/ja/woman-trend-10-l1327.html?v1=1591812","https://www2.hm.com/ja_jp/ladies/shop-by-product/view-all.html","https://www.gu-global.com/jp/ja/category/women","https://www.grail.bz/disp/ranking/001001004/"]
brands_counter = 0


def get_product_info(target_url = brand_url[brands_counter], target_brand = brands[brands_counter]):
    #Sets counter for product ranking, ensure that the URL links to page sorted by rank
    product_ranking_temp = 0
    requests = HTMLSession()
    target_html = requests.get(target_url)
    #allow for js to load on page
    target_html.html.render(timeout=60)
    soup = BeautifulSoup(target_html.html.html, "lxml")
    
    if target_brand == "Shein":
        #Scrapes price, name and appends to list for Shein
        #main_div = soup.find(id="product-list-v2__container")
        product_elements = soup.find_all(class_="S-product-item__info")
        print(product_elements)
        for product_elements in product_elements:
            product_name = product_elements.find("div", class_="S-product-item__name")
            product_price = product_elements.find("span", class_="S-product-item__retail-price")
            product_name.append(product_name.text.strip())
            product_price.append(product_price.text.strip())
            product_brand.append(target_brand)
            product_ranking.append(product_ranking_temp)
            product_ranking_temp += 1

    elif target_brand == "H&M":
        #Scrapes price, name and appends to list for H&M
        product_elements = soup.find_all(class_="product-item")
        
        for product_elements in product_elements:
            product_name = product_elements.find("h3", class_="item-heading")
            product_price = product_elements.find("span", class_="price regular")
            product_name.append(product_name.text.strip())
            product_price.append(product_price.text.strip())
            product_brand.append(target_brand)
            product_ranking.append(product_ranking_temp)
            product_ranking_temp += 1


    elif target_brand == "Zara":
        #Scrapes price, name and appends to list for Zara
        product_elements = soup.find_all(class_="product-grid-product-info")
        
        for product_elements in product_elements:
            product_name = product_elements.find("a", class_="product-link _item product-grid-product-info__name link")
            product_price = product_elements.find("span", class_="price-current__amount")
            product_name.append(product_name.text.strip())
            product_price.append(product_price.text.strip())
            product_brand.append(target_brand)
            product_ranking.append(product_ranking_temp)
            product_ranking_temp += 1
            product_ranking.append(product_ranking_temp)
            product_ranking_temp += 1

    elif target_brand == "GU":
            #Scrapes price, name and appends to list for GU
        product_elements = soup.find_all(class_="wuegps-0 hNPbGf")

        for product_elements in product_elements:
            product_name = product_elements.find("div", class_="sc-1cim99l-0 nlScz")
            product_price = product_elements.find("span", class_="sc-150v5lj-0 yfgtrh-0 jhFnrv")
            product_name.append(product_name.text.strip())
            product_price.append(product_price.text.strip())
            product_brand.append(target_brand)
            product_ranking.append(product_ranking_temp)
            product_ranking_temp += 1
    
    elif target_brand == "GRL":
            #Scrapes price, name and appends to list for GRL
        product_elements = soup.find_all(class_="card-product-01")
        
        for product_elements in product_elements:
            product_name = product_elements.find("p", class_="Stxt-name js-line-clamp")
            product_price = product_elements.find("p", class_="txt-price")
            product_name.append(product_name.text.strip())
            product_price.append(product_price.text.strip())
            product_brand.append(target_brand)
            product_ranking.append(product_ranking_temp)
            product_ranking_temp += 1
    else:
        exit()
    #Rotates to the next brand
    rotate(brands,1)


def save_csv (current_date = date.today()):
    #Saves data to file
    df = pd.DataFrame({'Date':current_date,'Brand':product_brand,'Ranking':product_ranking,'Product Name':product_name,'Price':product_price}) 
    df.to_csv('fast_fashion_ranking_'+current_date+'.csv', index=False, encoding='utf-8')


def rotate(l, n):
    #Rotates a list n times
    return l[n:] + l[:n]


def main(brands):
    for brands in brands:
        get_product_info()
        if input("Would you like to continue? The next brand is" + brands[0] + " y/n") == "y":
            get_product_info()
        else:
            print("Ending process")
            exit()
    save_csv()


main(brands)