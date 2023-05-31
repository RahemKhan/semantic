import pandas as pd
import json
import io
import uuid
import sys
from datetime import datetime
import os
import time
from owlready2 import *
pizza_onto = get_ontology("file://cw_onto_woi.owl").load() # load ontology into python object
class PopulateOntology:
    # def __init__(self, g, endpoint):
    #         self.graph = g
    #         self.endpoint = endpoint
    def subClasses(self, classes):
        for c in classes:
            #print(pizza_onto.c_.subclasses())
            if c.subclasses():
                lst.extend(list(c.subclasses()))
            if c not in lst:
                lst.append(c)
        #return _list
    pizza_list = list(pizza_onto.Pizza.subclasses())
    def subClassesPizza(self, classes):
        for c in classes:
            #print(pizza_onto.c_.subclasses())
            if c.subclasses():
                pizza_list.extend(list(c.subclasses()))

            if c not in pizza_list:
                pizza_list.append(c)
        #return _list    
    def current_milli_time(self):
        return round(time.time() * 1000)   
    
    def createDataset(self, df):
        for index, data in df.iterrows(): # iterate through data
            cat = data["categories"].split(",")
            for c in cat:
                print("****************************************")
                c_name = c.strip().lower().replace(" ", "")
                if c_name == "pizzaplace":
                    c_name = "restaurant"
                for l in lst:
                    if c_name == l.name.strip().lower():
                        instance = l(data["name"].strip().replace(" ", "_").replace("'","").replace("(", "").replace(")", ""))  #resturant/subclasses instance
                        instance.restaurantName = [data["name"]]
                        break
                    elif c_name in l.name.strip().lower():
                        print(">>>>>>>>>> else part")
                        instance = l(data["name"].strip().replace(" ", "_").replace("'","").replace("(", "").replace(")", ""))
                        instance.restaurantName = [data["name"]]
                        break
                #print("cat:name __________>>>",c_name)


            item = data["menu item"]
            item_flag = True

            #print("****************************************")

            i_name = item.strip().lower().replace("pizza", "").replace(",","").strip()
            print("i-name------------------>>>>>>>",i_name)    # pizza instance
            for lp in pizza_list:
                print("********** lp.name >>>>>>>>>>>> ", lp.name.strip().lower().replace("pizza", ""))
                if i_name == lp.name.strip().lower().replace("pizza", ""):
                    pizza_instance = lp(data["menu item"].strip().replace(" ", "_").replace(",","").replace("'","").replace("(", "").replace(")", "")+str(self.current_milli_time()))
                    pizza_instance.itemName = [data["menu item"]]
                    #instance.restaurantName = [data["name"]]
                    item_flag = False
                    break
                elif i_name in lp.name.strip().lower().replace("pizza", ""):
                    #print(">>>>>>>>>> else part")
                    
                    pizza_instance = lp(data["menu item"].strip().replace(" ", "_").replace(",","").replace("'","").replace("(", "").replace(")", "")+str(self.current_milli_time()))
                    pizza_instance.itemName = [data["menu item"]]
                    item_flag = False
                    #instance.restaurantName = [data["name"]]
                    break
            if item_flag:
                pizza_instance = pizza_onto.Pizza(data["menu item"].strip().replace(" ", "_").replace(",","").replace("'","").replace("(", "").replace(")", "")+str(self.current_milli_time()))
                pizza_instance.itemName = [data["menu item"]]
                    

                #print("cat:name __________>>>",c_name)
            item_value = pizza_onto.ItemValue(str(data["item value"]).strip().replace("'","").replace("(", "").replace(")", ""))
            item_currency = pizza_onto.Currency(str(data["currency"]).strip().replace("'","").replace("(", "").replace(")", ""), "")
            item_value.amountCurrency.append(item_currency)
            item_value.amount = [data["item value"]]
            pizza_instance.hasValue.append(item_value)
            instance.servesMenuItem.append(pizza_instance)
            address = pizza_onto.Address(data["address"].replace(",","").replace(" ","_").replace("'","").replace("(", "").replace(")", ""))
            address.firstLineAddress = [data["address"]]
            instance.hasAdress.append(address)

            city = pizza_onto.City(data["city"].replace(" ", "_").replace("'","").replace("(", "").replace(")", ""))
            instance.hasCity.append(city)

            state = pizza_onto.State(data["state"].replace(" ", "_").replace("'","").replace("(", "").replace(")", ""))
            instance.hasState.append(city)

            # country = pizza_onto.Country(data["country"])
            # instance.locatedInCountry.append([country])    

            #pizza_instance.hasLocation.append(hasAdress, hasCity, hasState)
            #pizza_instance.locatedIn.append(locatedInAdress, locatedInCity, locatedInCountry, locatedInState)
            #print(index ,data)

po = PopulateOntology()
df = pd.read_csv('IN3067-INM713_coursework_data_pizza_500.csv') # read excel file and store it in panda's data fraem
#classes_list = []
lst = list()
lst.append(pizza_onto.Restaurant)
lst.extend(list(pizza_onto.Restaurant.subclasses()))
pizza_list = list(pizza_onto.Pizza.subclasses())
po.subClasses(lst)
po.subClassesPizza(pizza_list)
po.createDataset(df)
pizza_onto.save(file = "cw_onto.owl", format = "rdfxml")
