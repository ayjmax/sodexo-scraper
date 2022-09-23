import requests
import string
from bs4 import BeautifulSoup

# Meals of the day
meals = ['breakfast', 'brunch', 'lunch', 'dinner']
# Tuple represents ( menuID, locationID )
dineHalls = {'rathbone' : (16872, 97451005), 'resident-dining' : (16870, 97451001), 'brodhead' : (16871, 97451004)}

def scrapeDineHall(dineHall: str, URL: str):
    pageHTML = requests.get(URL)
    if (pageHTML.status_code != 200):
        print(f'Status code returned: {pageHTML.status_code}')
        exit(1)
    
    soup = BeautifulSoup(pageHTML.content, 'html.parser')
    dates = soup.find("ul", {"id" : "bite-menu-dates"}).find_all("li", class_="bite-date")
    outputFile = f'{dineHall}.txt'
    
    with open(outputFile, 'w+', encoding='utf-8') as file:
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


for dineHall, ids in dineHalls.items():
    menuId, locationId = ids
    URL = f"https://menus.sodexomyway.com/BiteMenu/Menu?menuId={menuId}&locationId={locationId}&whereami=http://lehigh.sodexomyway.com/dining-near-me/{dineHall}"
    
    print(f'{menuId}, {locationId}')
    print(URL)
    
    scrapeDineHall(dineHall, URL)


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
