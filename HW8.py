#Rachel Sondergeld rsond@umich.edu

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cur.execute('SELECT name, rating, category_id, building_id FROM restaurants')
    fulltable = cur.fetchall()
    cur.execute('SELECT category, id FROM categories')
    categorygroup = cur.fetchall()
    cur.execute('SELECT building, id FROM buildings')
    buildingsgroup = cur.fetchall()
    conn.commit()

    
    restaurant_dictionary_list = []
    counter = 0
    for the_tuple in fulltable:
        new_dict = {}
        new_dict['name'] = the_tuple[0]
        new_dict['category'] = the_tuple[2]
        new_dict['building'] = the_tuple[3]
        new_dict['rating'] = the_tuple[1]
        restaurant_dictionary_list.append(new_dict)
    
    for dictionary in restaurant_dictionary_list:
        category_number = dictionary.get('category')
        for category in categorygroup:
            if category[1] == category_number:
                dictionary['category'] = category[0]

    for dictionary in restaurant_dictionary_list:
        building_number = dictionary.get('building')
        for building in buildingsgroup:
            if building[1] == building_number:
                dictionary['building'] = building[0]

    return restaurant_dictionary_list
        

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute('SELECT categories.category, categories.id FROM categories')
    categories = cur.fetchall()
    conn.commit()

    cur.execute('SELECT category_id, COUNT(*) as COUNT FROM restaurants GROUP BY CATEGORY_ID')
    number = cur.fetchall()
    conn.commit()

    restaurant_categories_dictionary = {}
    counter = 0
    for category in categories:
        restaurant_categories_dictionary[category[0]] = number[counter][1]
        counter += 1

    sorted_restaurant_categories_dictionary= dict(sorted(restaurant_categories_dictionary.items()))
    descending_restaurant_categories_dictionary = dict(sorted(restaurant_categories_dictionary.items(),
                           key=lambda item: item[1],
                           reverse=False))
    
    #creating bar chart
    restaurants = list(descending_restaurant_categories_dictionary.keys())
    count = list(descending_restaurant_categories_dictionary.values())

    plt.barh(restaurants, count, color=['darkred', 'darkmagenta', 'darkslategray', 'darkgoldenrod', 'darkblue', 'darkslateblue', 'darkcyan', 'darkorange', 'darkgrey', 'darkturquoise'])
    plt.title('Number of Restaurants on South University of Each Category')
    plt.xlabel('Number of Restaurants')
    plt.ylabel('Restaurant Categories')
    plt.tight_layout()
    plt.show()

    return sorted_restaurant_categories_dictionary

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cur.execute('SELECT category_id, AVG(rating) AS average_rating_per_category FROM restaurants GROUP BY category_id')
    average_rating_by_category = cur.fetchall()
    cur.execute('SELECT category, id FROM categories')
    category_and_id_key = cur.fetchall()
    conn.commit()
    #print(average_rating_by_category)

    category_dict = {}
    for tuple in category_and_id_key:
        category_dict[tuple[1]] = tuple[0]
    
    average_rating_list = []
    for tuple in average_rating_by_category:

        value = category_dict.get(tuple[0])
        if tuple[0] == value:
            print(tuple[0])
            print(value)
            average_rating_list.append(category_dict[value])
            average_rating_list.append(tuple[1])
    print(average_rating_list)


#Try calling your functions here
def main():
    get_restaurant_data('South_U_Restaurants.db')
    barchart_restaurant_categories('South_U_Restaurants.db')
    highest_rated_category('South_U_Restaurants.db')

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
