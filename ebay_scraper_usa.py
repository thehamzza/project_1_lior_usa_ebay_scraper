import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta, date
import datefinder
now = datetime.now()
current_date_time = now.strftime("%Y-%m-%d %H-%M-%S")
import re
from filter_functions import *
import sys, os
from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def get_data(url_in):
    try:
        r = requests.get(url_in,verify=False)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup)
        rows_data = soup.find_all("h3", attrs={"class": "lvtitle"})
        prices_tag = soup.find_all("span", attrs={"class": "bold bidsold"})
        times_sold = soup.find_all("span", attrs={"class": "tme"})
        # changes in version 1.3.2 only
        all_images_url = soup.find_all("img", attrs={"class": "img"})

        titles=[]
        urls=[]
        prices=[]
        sold_dates=[]
        shipment_locations=[]
        items_solds=[]
        image_urls=[]
        product_category=[]
        VERO=[]



        for row,price_text,date_s,img in zip(rows_data,prices_tag,times_sold, all_images_url):
            title =row.text
            row=str(row)
            href=row.split('''href="''')[1].split('"')[0]
            price=price_text.text
            price=str(price).strip()
            try:
                #removing $ sign
                price_range = re.findall(r"\d+\.\d+", price)
                print("USD Price : ", price_range)
                #converting USD price to Israeli Shekels
                file_currency_rate = open("currency_rate.txt", "r")
                currency_rate = file_currency_rate.readline()
                currency_rate = float(currency_rate)
                new_price = []
                for i in range(0, len(price_range)):
                    np = str(round(float(price_range[i])*currency_rate, 2))
                    new_price.append(np)

                new_price = " to ".join(new_price)
                print("Shekels Price : ", new_price)

            except Exception as e:
                print(e)

            # calling vero function from filter functions
            vero_word = "nill"
            vero_word = vero_forbidden_words_function(title, vero_word)
            VERO.append(vero_word)


            image_url=img['src']
            titles.append(str(title).strip())
            prices.append(new_price)
            urls.append(href)
            image_urls.append(image_url)
            #print("IMAGE URL : ", image_urls)

            #selecting only date
            date_text=str(date_s.text).strip()
            matches = list(datefinder.find_dates(date_text))
            if len(matches) > 0:
                # date returned will be a datetime.datetime object. here we are only using the first match.
                date = matches[0]

                date_matches = re.findall('(\d{2,4}[-](\d{2})[-]\d{2})', str(date))
                for date_match in date_matches:
                    date=date_match[0]

            else:
                print('No dates found')

            sold_dates.append(str(date))
            #print("Sold_dates : ", sold_dates)

            r2 = requests.get(href,verify=False)
            soup2 = BeautifulSoup(r2.text, 'html.parser')

            location = soup2.find("span", attrs={"ux-textspans ux-textspans--BOLD ux-textspans--SECONDARY"})
            #print("LOCATION : ", location.text)

            sold_ite = soup2.find("a", attrs={"class": "vi-txt-underline"})
            sold_ite_list = re.findall(r'\d+', str((sold_ite.text).strip()))
            sold_ite = ' '.join(map(str, sold_ite_list))
            shipment_locations.append(str(location.text).strip())
            items_solds.append(sold_ite)
            #new column of category
            prod_category = soup2.find("a", attrs={"class": "seo-breadcrumb-text"})
            prod_category = str((prod_category.text).strip())
            product_category.append(prod_category)

            #print("product_category : ", prod_category)

            print(f'Data Fetching For : {str(title).strip()}')

            #print("Items SOld : ", items_solds)






        print("titles : ",titles)
        print("prices : ",prices)
        print("urls : ",urls)
        print("sold_dates : ",sold_dates)
        print("shipment_locations : ",shipment_locations)
        print("items_solds : ",items_solds)
        print("image_urls : ",image_urls)
        print("product_category : ", product_category)
        print("VERO : ", VERO)

        return (titles,prices,urls,sold_dates,shipment_locations,items_solds, image_urls, product_category, VERO)
    except Exception as e:
        print(e)
        # if some error occurs while capturing data
        print("Some error occurred on this store's page.")

        print("titles : ", titles)
        print("prices : ", prices)
        print("urls : ", urls)
        print("sold_dates : ", sold_dates)
        print("shipment_locations : ", shipment_locations)
        print("items_solds : ", items_solds)
        print("image_urls : ", image_urls)
        print("product_category : ", product_category)
        print("VERO : ", VERO)

        return (titles, prices, urls, sold_dates, shipment_locations, items_solds, image_urls,product_category, VERO)


if __name__ == '__main__':
    with open('names.txt') as f:
        namesofstore = [line.rstrip() for line in f]
    loc=f'Ebay_Scraper_{str(current_date_time)}'
    os.mkdir(loc)

    # this will add all the stores data into 1 big file, with 1 name only
    file_name = "OUTPUT"
    csvf = open(f'./{loc}/{file_name}.csv', 'w', newline='')
    writcsv = csv.writer(csvf)
    writcsv.writerow(['Store', 'Titles', 'USD Prices', 'Urls', 'Sold_dates', 'Shipment_location', 'Total Items_sold', 'Image Url', 'Category', 'VERO'])


    #today's date for the sold date list comparison
    todays_date=str(now.strftime("%Y-%m-%d"))
    print("------------------------------------------------------STATUS----------------------------------------------------------")
    #print('''Today's date : ''', todays_date)

    store_counter=0
    for name in namesofstore:
        print("STORE NUMBER : ", store_counter)
        print("STORE NAME : ", name)
        url_items_for_sale = f"https://www.ebay.com/sch/{name}/m.html?_nkw&_armrs=1&_ipg&_from&LH_Complete=1&LH_Sold=1&rt=nc&LH_AllListings=1&LH_PrefLoc=98&_udlo&_udhi&LH_ItemCondition=3"
        titles,prices,urls,sold_dates,shipment_locations,items_solds,image_urls, product_category,VERO=get_data(url_items_for_sale)

        #calling all required functions
        #using filter functions for 7 days, location usa only, price greater than 10
        #and updating the old lists
        list_required_index_for_7_days=required_index_for_7_days(sold_dates)

        titles,prices,urls,sold_dates,shipment_locations,items_solds,image_urls, product_category, VERO= final_list_of_items_with_only_usa_location(titles,prices,urls,sold_dates,shipment_locations,items_solds,list_required_index_for_7_days,image_urls, product_category, VERO)
        print("NEW FILTERED DATA TO WRITE IN CSV FILE :")
        print("\n","Titles : ",titles,"\n", "Prices : ", prices,"\n", "URLS : ", urls, "\n","SOLD Dates : ", sold_dates,"\n","Shipment Location : ", shipment_locations,"\n", "Items Solds : ", items_solds,"\n", "Image Urls : ", image_urls, "\n", "Category : ", product_category, "\n", "VERO : ", VERO)
        a=0
        for _ in titles:
            try:
                writcsv.writerow([name,titles[a],prices[a],urls[a],sold_dates[a],shipment_locations[a],items_solds[a],image_urls[a], product_category[a], VERO[a]])
                csvf.flush()
            except:
                pass
            a += 1
        store_counter += 1
        print("----------------------------------2--------------------XXX------------------------------------------------------------")

    csvf.close()
    print("PROCESS COMPLETED SUCCESSFULLY")


