import requests
import re
from bs4 import BeautifulSoup

# Currently testing for rathbone
URL = "https://menus.sodexomyway.com/BiteMenu/Menu?menuId=16872&locationId=97451005&whereami=http://lehigh.sodexomyway.com/dining-near-me/rathbone"

pageHTML = requests.get(URL)
if (pageHTML.status_code != 200):
    print(f'Status code returned: {pageHTML.status_code}')
    exit(1)


soup = BeautifulSoup(pageHTML.content, 'html.parser')
dates = soup.find("ul", {"id" : "bite-menu-dates"}).find_all("li", class_="bite-date")
meals = ['breakfast', 'brunch', 'lunch', 'dinner']


with open('output.html', 'w+', encoding='utf-8') as file:
    for date in dates:
        file.write(
            '########------------------------- %s ------------------------########\n'
            % date.text.replace("\r","").replace("\n","").replace(" ", "")
        )
        for meal in meals:
            if not soup.select(f'#{date["id"]}-day .{meal}'): #Certain days don't have breakfast/brunch
                continue

            file.write(f'//////----------------- {meal} ---------------//////\n')
            menuLabelString = f'#{date["id"]}-day .{meal} .bite-menu-course:nth-of-type(1)'
            menuInfoString = f'#{date["id"]}-day .{meal} .bite-menu-item:nth-of-type(1)'
            menuLabel = soup.select(menuLabelString)[0]
            menuInfo = soup.select(menuInfoString)[0]
            
            #Iterate through every menu category (Ex. Globowl, Diner, Simple Servings)
            while (menuLabel is not None):
                file.write(f'|---------- {menuLabel.h5.text} ----------|\n')
                
                foods = menuInfo.find_all(class_="get-nutritioncalculator") #Food name list
                caloriesList = menuInfo.find_all(class_="get-nutrition") #Calories info list

                #Iterate through every food item
                for index, food in enumerate(foods):
                    file.write(food.string + '\n') #Write food name
                    
                    #Find allergy/special diet info and (if it exists) list it out
                    allergenList = food.find_next_sibling('div')
                    for allergen in allergenList.findChildren("img" , class_="icon-allergen"):
                        file.write(f'--> {allergen["alt"]}\n')
                    
                    file.write(caloriesList[index].string + '\n') #Write calorie amount
                
                #Move to next menu category
                menuInfo = menuInfo.find_next_sibling('ul')
                menuLabel = menuLabel.find_next_sibling('div')



# list = soup.select('''#menuid-21-day .bite-menu-item .get-nutritioncalculator,
#                    #menuid-21-day .bite-menu-item .get-nutrition''')



# with open('output.html', 'w+', encoding='utf-8') as file:
#     for index, item in enumerate(list):
#         file.write(item.string + '\n')
        
#         # print (item['class'])
#         if (item['class'][0] == 'get-nutritioncalculator'):
#             # print(str(item))
#             # print(str(item.find_next_sibling('div')))
            
#             allergenList = item.find_next_sibling('div')
#             for allergen in allergenList.findChildren("img"):
#                 file.write(str(allergen['alt']) + '\n')
            
                  
#         if (index != 0 and index % 2 != 0):
#             file.write('\n')
