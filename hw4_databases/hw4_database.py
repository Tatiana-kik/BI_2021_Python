#!/usr/bin/env python
# coding: utf-8

# In[1]:


# HOMEWORK 4 - create a database, parsing some site
#              and put the data to the database
#


# In[2]:


import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3


# In[3]:


# For this task I parsed website 'https://melonpanda.com' of the 
# internet cosmetics shop. I'm creating 2 tables:
#     1. brands   - list of brands (id, name)
#     2. products - list of products (id, brand_id, name,
#                                     price, sold_out_flag)
#
# Analysis of the website's pages suggest that the list of brands and 
# the list of products are a JavaScript variables. And the values of 
# these variables are in JSON format. Therefore I wrote a function to 
# get JSON data by URI and variable names.


# In[4]:


# get JSON data by URI and JS variable name.
def get_json_value_by_js_variable_name(uri, var_name):

    # get requested page
    rep = requests.get(uri)

    # find script tags by using BeautifulSoup
    soup = BeautifulSoup(rep.text, 'html.parser')
    scripts = soup.find_all("script")

    # find variable in scripts,
    # JS the code has view: ... requested.var.name = [value]; ...
    p = re.compile(f'{var_name} = \[.*?\];')
    matches = p.findall(str(scripts))
    if not matches:
        print('Err:  could not find variable={var_name}.')
        return None

    # extract variable value - skip variable name and list symbol ';'
    json_str = matches[0][len(var_name) + 3 : -1]
    var_value = json.loads(json_str)

    return var_value


# In[6]:


# Now create DB and tables. Also we will clean them befor filling.
conn = sqlite3.connect('hw4.db')


# In[11]:


# create brands table
query = '''
            CREATE TABLE IF NOT EXISTS brands(
                    brand_id INTEGER PRIMARY KEY,
                    name TEXT
            )
        '''
conn.execute(query)      

# create product table
query = '''
            CREATE TABLE IF NOT EXISTS products(
                    product_id INTEGER PRIMARY KEY,
                    brand_id,
                    name TEXT,
                    price FLOAT,
                    sold_out BOOL
            )
        '''
conn.execute(query)

# clear tables before filling
conn.execute('DELETE FROM brands')
conn.execute('DELETE FROM products')
conn.commit()


# In[12]:


# and now we are parsing site and filling our 2 tables

# get list of brands
uri = 'https://melonpanda.com/ru/catalog/brands'
var = 'window.site.binding.brands'
brands = get_json_value_by_js_variable_name(uri, var)

# go through the brands
brand_id = 0
for brand in brands:

    brand_id += 1

    # since this is a learning project, collect info only about first 5 brands
    if brand_id > 5:
        break

    print(brand_id, brand['name'], brand['url'])

    # get list of products
    var = 'window.site.binding.products'
    products = get_json_value_by_js_variable_name(brand['url'], var)

    # go the products and prepare data for DB
    products_prepared = []
    for prod in products:

        #for k in prod:
        #    print(k, ':', prod[k])

        name = prod['name']
        prices = prod['prices']
        sold_out = prod['sold_out']

        # the field 'prices' is another one dict, get price in RUB
        price = float('nan')
        for pr in prices:
            if pr['currency'] == 'rub':
                price = pr['value']

        # store product in list
        products_prepared.append([brand_id, name, price, sold_out])


    # and now add data to DB

    # add brand to brand table
    query = f'''
                INSERT INTO
                brands(brand_id, name)
                VALUES({brand_id}, '{name}')
            '''
    conn.execute(query)

    # add products to product table
    query = '''
                INSERT INTO
                products(brand_id, name, price, sold_out)
                VALUES(?, ?, ?, ?)
            '''
    conn.executemany(query, products_prepared)

    # commit the result
    conn.commit()


# In[13]:


# example of using DB

# at first get all products with price > 5000
query = '''
            SELECT product_id, brand_id, name, price, sold_out
            FROM products
            WHERE price > 5000
        '''
res = conn.execute(query).fetchall()

print('Original result of SELECT:')
for i in res:
    print(i)

# update values - set zero price if product is sold out
query = '''
            UPDATE products
            SET price = 0
            WHERE sold_out == True
        '''
conn.execute(query)

# and make the same SELECT request once again to see the result
query = '''
            SELECT product_id, brand_id, name, price, sold_out
            FROM products
            WHERE price > 5000
        '''
res = conn.execute(query).fetchall()

print('\nResult of SELECT after UPDATE:')
for i in res:
    print(i)
    
# commit the changes to DB
conn.commit()    


# In[14]:


# finaly close the DB
conn.close()

