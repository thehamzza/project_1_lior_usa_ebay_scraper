import regex as re
from datetime import datetime, timedelta, date
import os

titles=['0.Magnum PI Cross Of Lorraine ', '1.Natural Amazonite  Horn Chain', '2.Palm Tree Garation', '3.Vibrating Body', '4.Clay Baki', '5.Tube Glass Bottle', '6.Audible Ribbon', '7.Retro Ancient']
prices=['$14.97', '$16.89', '$11.25', '$9.89', '$8.49', '$9.89', '$7.48 to $10.09', '$13.99 to $15.38']
urls=['https://www.ba~F', 'https0dlWFdVJRL', 'httash=0AAOSwzVtf~A9P', 'https://wwwm/itms8a6yDy', 'https://ww9eXrpfbgKh', 'https:/0b:g:h5HfK', 'https://www.itm/1ox', 'https://ww/1b5Sa0']
sold_dates=['2022-01-25', '2022-01-16', '2022-01-24', '2022-01-04', '2022-01-20', '2022-12-20', '2022-01-19', '2022-01-24']
shipment_locations=['0, usA', '1, Usa', '2, us', '3, usa', '4, USA', '5, uSa', '6, UsA', '7, uSA']
items_solds=['17', '7', '3', '16', '2', '2', '3', '2']
VERO=['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh']


def required_index_for_7_days(my_list):
    #today's date for the sold date list comparison
    todays_date=date.today()
    print('''Today's date : ''', str(todays_date))

    #finding last 7 days' dates
    last_seven_days = [str(todays_date), 'a', 'b', 'c', 'd', 'e', 'f', ]
    for i in range(1, 7, 1):
        last_seven_days[i] = str(todays_date - timedelta(days=i))

    print("last 7 days:", last_seven_days)
    print("Sold dates: ",my_list)

    required_indexes_day_0=[i for i, e in enumerate(my_list) if str(last_seven_days[0]) in e.lower()]
    required_indexes_day_1=[i for i, e in enumerate(my_list) if str(last_seven_days[1]) in e.lower()]
    required_indexes_day_2=[i for i, e in enumerate(my_list) if str(last_seven_days[2]) in e.lower()]
    required_indexes_day_3=[i for i, e in enumerate(my_list) if str(last_seven_days[3]) in e.lower()]
    required_indexes_day_4=[i for i, e in enumerate(my_list) if str(last_seven_days[4]) in e.lower()]
    required_indexes_day_5=[i for i, e in enumerate(my_list) if str(last_seven_days[5]) in e.lower()]
    required_indexes_day_6=[i for i, e in enumerate(my_list) if str(last_seven_days[6]) in e.lower()]

    all_required_indexes_for_7_days=(required_indexes_day_0 + required_indexes_day_1 + required_indexes_day_2 + required_indexes_day_3 + required_indexes_day_4 + required_indexes_day_5 + required_indexes_day_6)

    return all_required_indexes_for_7_days


#calling the function and string indexes in a variable
#list_required_index_for_7_days=required_index_for_7_days(sold_dates)



#maximum value=min idk why
def find_max_price(price):
    numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)
    #print(rx.findall(price))
    p=min(rx.findall(price))
    return p

def index_required_for_prices_greater_than_10(prices):
    new_prices=prices
    #keeping max price of (range of prices) items
    for i in range (len(prices)):
        new_prices[i]=find_max_price(prices[i])

    prices=new_prices

    #index of element having price >=10
    index_greater_than_10 = []
    for i in range(0, len(prices)) :
        if (float(prices[i]) >= 10.00):
            index_greater_than_10.append(i)

    return index_greater_than_10
#--------------------------------------------------------

def final_list_of_items_with_only_usa_location(titles,prices,urls,sold_dates,shipment_locations,items_solds,list_required_index_for_7_days,image_urls, product_category, VERO):

    all_indexes = [*range(0, len(shipment_locations), 1)]

    print("All Required Indexes for 7 days: ", list_required_index_for_7_days)

    index_greater_than_10=index_required_for_prices_greater_than_10(prices)
    print("Index Greater than 10 : ", index_greater_than_10)

    required_indexes_location=[i for i, e in enumerate(shipment_locations) if 'united states' in e.lower()]
    print("Required Indexes of Location: ", required_indexes_location)

    #intersection of price index and location index
    all_indexes_to_keep=set(index_greater_than_10).intersection(set(required_indexes_location))
    #final intersection with 7 days indexes
    all_indexes_to_keep=list((all_indexes_to_keep).intersection(set(list_required_index_for_7_days)))

    print("All indexes to keep : ", all_indexes_to_keep)

    index_to_pop= list(set(all_indexes)-set(all_indexes_to_keep))
    print("All indexes to pop : ", index_to_pop)

    titles = [titles[x] for x in all_indexes_to_keep]
    prices = [prices[x] for x in all_indexes_to_keep]
    urls = [urls[x] for x in all_indexes_to_keep]
    sold_dates = [sold_dates[x] for x in all_indexes_to_keep]
    shipment_locations = [shipment_locations[x] for x in all_indexes_to_keep]
    items_solds = [items_solds[x] for x in all_indexes_to_keep]
    image_urls = [image_urls[x] for x in all_indexes_to_keep]
    product_category = [product_category[x] for x in all_indexes_to_keep]
    VERO = [VERO[x] for x in all_indexes_to_keep]

    return (titles,prices,urls,sold_dates,shipment_locations,items_solds, image_urls, product_category, VERO)

#old vero function was not suitable
# def vero_forbidden_words_function(title, vero_word):
#     directory = os.getcwd()
#     vero_file_location= directory+"\VERO.txt"
#
#     forbidden_words=[]
#     with open(vero_file_location, encoding='utf8') as f:
#         for line in f:
#             forbidden_words.append(line.strip())
#
#     for i in range (0, len(forbidden_words)):
#         if forbidden_words[i] in title.casefold():
#             print("Forbidden Word :", forbidden_words[i])
#             vero_word=forbidden_words[i]
#         else:
#             pass
#
#     return vero_word


def vero_forbidden_words_function(title, vero_word):
    directory = os.getcwd()
    #vero_file_location= directory+"\VERO.txt"
    #for linux
    vero_file_location= directory+"/VERO.txt"

    forbidden_words=[]
    with open(vero_file_location, encoding='utf8') as f:
        for line in f:
            forbidden_words.append(line.strip())

    # To break the sentence in words
    s = title.split(" ")

    for index in range (0, len(forbidden_words)):
        for i in s:
            # Comparing the current word
            # with the word to be searched
            if (i.lower() == forbidden_words[index].lower()):
                vero_word=forbidden_words[index]
            else:
                pass
    return vero_word
