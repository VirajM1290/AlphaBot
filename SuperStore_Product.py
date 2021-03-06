# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 00:41:42 2018

@author: Monika Asawa
"""

import pandas as pd
import numpy as np

from ProductRecommender import recommendProducts

TOP_HOW_MANY = 3

#----------------------------
'Grab the data from last quarter only'
def provide_recent_quarter_data():
    
    ordersDf = pd.read_csv('SuperStoreData.csv', index_col = ['Order Date'], parse_dates = True)

    ordersDf = ordersDf.loc[ordersDf['Category'] == 'Furniture']

    ordersDf = ordersDf.sort_index()
    
    last_date = ordersDf.last_valid_index()
    
    from datetime import timedelta
    date_120_days_ago  = last_date - timedelta(days=120)
    
    recent_quarter_data = ordersDf.loc[date_120_days_ago : last_date]
    
    print("No of records in recent quarter", np.shape(recent_quarter_data))
    
    return recent_quarter_data

#----------------------------
recent_quarter_data = provide_recent_quarter_data()
#----------------------------

'I want to find top 3 sub categories in Furniture Category'
def recommend_selling_prodCat():
    
    sub_cat_freq = pd.DataFrame(recent_quarter_data.groupby('Sub-Category')['Quantity'].sum())
    
    sub_cat_freq = sub_cat_freq.sort_values(by="Quantity", ascending =False)
    
    top_3_sub_cat = sub_cat_freq[:TOP_HOW_MANY]
    
    
    response = 'Hi' + "\n" + 'What would you like to buy today? '
    for i in top_3_sub_cat.index.tolist():
        response += "\n" + i
        #response.append(i)
        
#==============================================================================
#     text = {}
#     text['text'] = response
#         
#     text_2  = {}
#     text_2['text'] = text
#==============================================================================
    
    #response = response[1:]
    print(response)
    
    return response
#----------------------------


def suggest_selling_prodNames(selected_sub_category):

    recent_data = recent_quarter_data.loc[recent_quarter_data['Sub-Category'] == selected_sub_category]
    
    #print("No of records in recent_data for selected sub category is ",np.shape(recent_data))
    
    product_freq = pd.DataFrame(recent_data.groupby('Product Name')['Quantity'].sum())
    
    #print("No of products in frequency count",np.shape(product_freq))
    
    product_freq = product_freq.sort_values(by="Quantity", ascending =False)
    
    #print("No of products in frequency count",np.shape(product_freq))
        
    top_3_product_names = product_freq[:TOP_HOW_MANY]
    
    print("top_3_product_names",top_3_product_names)
    
    top_3_prodNames = top_3_product_names.index.tolist()
    
    response =  'Here you go!' + "\n" + 'Look out our top ' +selected_sub_category
    
    print(response)
    
    for i in top_3_prodNames:
        print(i)
        response += "\n\n" + i
        
    print("response ::", response)
    
    return response


def loadProducts():

    ordersDf = pd.read_csv('SuperStoreData.csv', index_col = ['Order Date'], parse_dates = True)

    ordersDf = ordersDf.loc[ordersDf['Category'] == 'Furniture']
    
    Products = pd.DataFrame(ordersDf, columns=['Sub-Category','Product Name'],index =None)
    
    Products.columns = ['Product_Category','Product_Name']
     
    return Products

'This function will generate the product category as entity types'
def loadProductCat():
    
    grouped = loadProducts()
    
    grouped = grouped.loc[grouped['Product_Category'] == "Bookcases"]
    
    ProductsEn = grouped.Product_Category.unique().tolist()
     
    return ProductsEn

'This function will generate the product names entities'
def loadProductNames(selected_sub_category):
    
    Products = loadProducts()
    
    Products_sb = Products.loc[Products['Product_Category'] == selected_sub_category]
    
    ProductNamesEn = Products_sb.Product_Name.unique().tolist()
     
    return ProductNamesEn


def check_if_product_selected(parameters):
    
    params = {}
    error_response = ""
    
    tableSelection = parameters.get('Tables')
    chairSelection = parameters.get('Chairs')
    furnishingsSelection = parameters.get('Furnishings')
    bookcaseSelection = parameters.get('Bookcases')
    
    if(len(tableSelection)==0 and len(chairSelection)==0 and len(furnishingsSelection)==0 and len(bookcaseSelection)==0):
        print("why are going in here")
        error_response = 'Please specify the correct product name you would like to buy'
        
    params['TableSelection'] = parameters.get('Tables')
    params['ChairSelection'] = parameters.get('Chairs')
    params['FurnishingsrSelection'] = parameters.get('Furnishings')
    params['BookcasesSelection'] = parameters.get('Bookcases')
    
    print(params)
    
    return error_response.strip(), params 


def recommendProductsNames(params):
    
    selectedProducts = []
    
    if(params.get('TableSelection')):
        
        print("Check 1",params.get('TableSelection'))
        
        selectedProducts = selectedProducts + params.get('TableSelection')
    
    if(params.get('ChairSelection')):
        
        print("Check 1",params.get('ChairSelection'))
        
        selectedProducts = selectedProducts + params.get('ChairSelection')
        
    if(params.get('FurnishingsrSelection')):
        
        print("Check 1",params.get('FurnishingsrSelection'))
        
        selectedProducts = selectedProducts + params.get('FurnishingsrSelection')
    
    if(params.get('BookcasesSelection')):
        
        print("Check 1",params.get('BookcasesSelection'))
        
        selectedProducts = selectedProducts + params.get('BookcasesSelection')
            
    #selectedProducts = selectedProducts[3:]
        
    print("No of products selected :",len(selectedProducts))
    print(selectedProducts)
    
    recProducts = recommendProducts(selectedProducts)
    
    response =  'Great Choice!' + "\n"
    
    print(response)
    
    if(len(recProducts)>0 and len(selectedProducts)>0):
        
        selProducts =''
        
        for i in selectedProducts:
            print(i)
            selProducts += ", "+ i 
        selProducts = selProducts[1:]
        print(selProducts)
        
        
        response += 'People who bought ' + selProducts + ' also bought '
    
        print(response)
        
        for i in recProducts:
            print(i)
            response += "\n\n" + i
            
    elif(len(selectedProducts)>0):
        print("Couldn't find any recommendations for the selected productset")
        response += 'Anything else for today?'
            
    print("response ::", response)
    
    return response