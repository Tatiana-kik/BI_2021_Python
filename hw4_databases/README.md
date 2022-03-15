# HW4:  DATABASES

HW4 requires to create DB and fill it from some WEB site.
This HW report contains JupyterNotebook and python scripts with the same content.

## 1. Overview

For this task I parsed website 'https://melonpanda.com' of the internet cosmetics shop.
I created 2 tables:
1. brands   - list of brands (id, name)
2. products - list of products (id, brand\_id, name, price, sold\_out\_flag)

Analysis of the website's pages suggest that the list of brands and the list of 
products are a JavaScript variables. And the values of these variables are in JSON 
format. Therefore I wrote a function to get JSON data by URI and variable names.

After this I went through the website pages, parsing and filling the tables.

Finaly I am showing an example of using my DB by executing SELECT and UPDATE
requests.

## 2. Requirements

Code was tested on Ubuntu 20.04, Python 3.8.10.
Necessary modules are listed in requirements.txt file.
To intstall them need to run `pip install -r requirements.txt`.

## 3. Execution

To check the HW report please execute JupyterNotebook script step by step.

**NOTE:** The processing of all brand pages takes too much time, so I reduced the number 
of brand pages to 5. You can change this limitation by modifying the code.