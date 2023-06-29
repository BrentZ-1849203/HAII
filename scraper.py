import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import time
main_url = 'https://dagelijksekost.een.be/'
url = main_url + 'az-index'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'lxml')
recipe_links = []

# Get all links in site to recipes
for recipe in soup.find_all('ul', class_='az-letter__links'):
    recipe_links += recipe.find_all('a')

recipe_names = []
ingredient_list = []
units = []


# recipe_links = ["https://dagelijksekost.een.be/gerechten/gebakken-zalm-met-limoenrijst-en-wokgroenten"]
# Go through all links and get other stuff


for link in recipe_links:
    # Required to not get kicked out as too many requests are made in a short time span
    time.sleep(0.2)
    # print(main_url + link.get("href"))
    # Get html
    try:
        response = requests.get(main_url + link.get("href"))
        
        # response = requests.get(recipe_links[0])
        # Parse using beautifulSoup
        recipe_site = BeautifulSoup(response.content, 'lxml')

        # spans = recipe_site.find_all("span")
        # Parse response
        titles = recipe_site.find('h1', class_="dish-metadata__title headline-1")
        recipe_names.append(titles.contents[0].strip())

        print(titles.contents[0].strip())
        script_tag = recipe_site.find("script", {"type": "application/ld+json"})
        # Find the div for ingredients
        products = recipe_site.find('div', class_="ingredient-list__part")
        # Change erroneous line endings
        json_data = re.sub(r"[\x00-\x1F\x7F-\x9F]", "", script_tag.string)
        # Parse to JSON
        json_data = json.loads(json_data)
        # Get list of ingredients for 4 people.
        ingredients = json_data["recipeIngredient"]

        ingrs = []
        uts = []
        # Run over data and parse content.
        for i in ingredients:
            i = i.strip()
            splitted = i.split("  ")

            pattern = r"^\d+"

            match = re.search(pattern, splitted[0])
            
            if match:
                matched_string = match.group(0)
                split_again = splitted[0].split(" ")

                if(len(split_again) > 1):

                    first_stuff = split_again[0] + " " + split_again[1]

                    second_stuff = split_again[2:]

                    # print(split_again, splitted)
                    if len(split_again[2:]) == 0:
                        uts.append(first_stuff)
                        if(len(splitted) == 1):
                            ingrs.append(split_again[1])
                        else:
                            ingrs.append(splitted[1])
                    else:
                        uts.append(first_stuff)
                        ingrs.append(" ".join(second_stuff))

                else:
                    uts.append(split_again[0])
                    ingrs.append(splitted[1])
            else:
                try:
                    ingrs.append(splitted[1])
                    uts.append(splitted[0])
                except:
                    pass
                    # print(splitted)
        ingredient_list.append(" ".join(ingrs))
        units.append(" ".join(uts))

        df = pd.DataFrame({"recipe_name":recipe_names, "ingredients": ingredient_list, "units":units})
        df.to_csv("jeroen_meus.csv", mode="a", header=False, index=False)
        print(df)
        recipe_names = []
        ingredient_list = []
        units = []
    except e as e:
        print(e)
        print(main_url + link.get("href"))






   

    

    # print(response.content)
