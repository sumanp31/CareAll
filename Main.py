#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 10:14:00 2020

@author: suman
"""

import pandas as pd


class Oldies():
    # Initialize the class object
    def __init__(self, info):
        self.name = info[0]
        self.age = int(info[1])
        self.req = info[2]
        self.fee = int(info[3])
        self.avl = info[4]
        self.caretaker = info[5]
        self.rating = float(info[6])
        self.No_of_rating = int(info[7])
        self.app_list = info[8]
    
    # Function to update the profile
    def updateProfile(self, id):
        
        print ("Updating your profile")
        df = pd.read_csv("oldies.csv", index_col = 0)
        
        name = input("Enter Name")
        age = int(input("Enter Age"))
        req = input("Enter Requirement")
        fee = int(input("Enter the maximum fee"))
        
        #Update class variales
        self.name = name
        self.age = age
        self.req = req
        self.fee = fee
        
        #Update CSV file
        df.loc[id, "Name"] = name
        df.loc[id, "Age"] = age
        df.loc[id, "Requirement"] = req
        df.loc[id, "Fee"] = fee
        df.to_csv("oldies.csv")
    
    #Function to check the list of Applicants
    def appList(self):
        
        i = input("Do you want to check the list of apllication? Y/n ")
        if i.capitalize() == "Y":
            df_c = pd.read_csv("caretaker.csv", index_col = 0)
            df_c.drop(["id of Oldies", "No of Ratings"], axis=1, inplace = True)
            if self.app_list == '[]':
                print ("There is no applications")
            else:
                self.app_list = [self.app_list.strip('][').split(', ')][0]
                self.app_list = [int(x) for x in self.app_list]
                df_c = df_c.loc[self.app_list, :]
                
                print (df_c)
    #Function to Choose caretaker
    def chooseCaretaker(self, id):
        if self.app_list == '[]':
             return None

        c = int(input("Enter the id of the caretaker you chose:"))
        l = self.caretaker
        df = pd.read_csv("oldies.csv", index_col = 0)
        print ("Adding Caretaker to your profile")
        l = df.loc[id, "id of Caretaker"]
        if l == '[]':
            l = [c]
        else:
            l = [l.strip('][').split(', ')][0]
            l = [int(x) for x in l]
            l = l + [c]
        self.caretaker = l
        df.loc[id, "id of Caretaker"] = str(list(set(l)))
        df.to_csv("oldies.csv")
        
        
        df_c = pd.read_csv("caretaker.csv", index_col = 0)
        
        if df_c.loc[c, "Avaibility"] == "yes":
            print ("Sending response to the caretaker")
            l = df_c.loc[c, "id of Oldies"]
            if l == '[]':
                l = [id]
            else:
                l = [l.strip('][').split(', ')][0]
                l = [int(x) for x in l]
                l = l + [id]
            df_c.loc[c, "id of Oldies"] = str(list(set(l)))
            if len(l) == 4:
                df_c.loc[c, "Avaibility"] = "no"
            
            l = df_c.loc[c, "Response"]
            if l == '[]':
                l = [id]
            else:
                l = [l.strip('][').split(', ')][0]
                l = [int(x) for x in l]
                l = l + [id]
            df_c.loc[c, "Response"] = str(list(set(l)))
        else:
            print ("The caretaker is at maximum capacity")
            
        df_c.to_csv("caretaker.csv")
        
    #Function to Rate the caretakers
    def rate(self):
        
        if self.caretaker == "None":
            print("\nNo Caretaker to Rate")
        else:
            df_c = pd.read_csv("caretaker.csv")
            df_c = df_c[df_c["id"] == int(self.caretaker)].values[0]
            user_C = Caretaker(df_c[1:])
            
            r = int(input("Enter Your Rating out of 5: "))
            user_C.rating = ((float(user_C.rating) * user_C.No_of_rating) + r) / (user_C.No_of_rating+1)
            user_C.No_of_rating = user_C.No_of_rating +1
            df_c = pd.read_csv("caretaker.csv", index_col = 0)
            df_c.loc[int(self.caretaker), "Rating"] = user_C.rating
            df_c.loc[int(self.caretaker), "No of Ratings"] = user_C.No_of_rating
            df_c.to_csv("caretaker.csv")
            
        
class Caretaker():
    #Initialize the class object
    def __init__(self, info):
        self.name = info[0]
        self.age = int(info[1])
        self.fee = int(info[2])
        self.avl = info[3]
        self.oldies = info[4]
        self.rating = float(info[5])
        self.No_of_rating = int(info[6])
        self.list_of_app = info[7]
        self.Response = info[8]
        
    #Function to update the profile
    def updateProfile(self,id):
        print ("Updating your profile")
        df = pd.read_csv("caretaker.csv", index_col = 0)
        
        name = input("Enter Name")
        print ()
        age = int(input())
        print ()
        fee = int(input("Enter the maximum fee"))
        
        #Update class variales
        self.name = name
        self.age = age
        self.fee = fee
        
        #Update CSV file
        df.loc[id, "Name"] = name
        df.loc[id, "Age"] = age
        df.loc[id, "Fee"] = fee
        df.to_csv("caretaker.csv")
    
    #Function to apply for a position
    def app(self, id):
        print ("This is the list of all the oldies in need of care")
        df_o = pd.read_csv("oldies.csv")
        df_o = df_o[df_o["Avaibility"] == 'yes']
        df_o.drop(["No of Ratings", "list of Application", "id of Caretaker"], axis=1, inplace = True)
        print (df_o)
        
        r = input("Do you want to apply for one of the positions?Y/n")
        if r.capitalize() == "Y":
            id_o = int(input("Enter the new oldie's id"))
            df = pd.read_csv("caretaker.csv", index_col = 0)
            l = df.loc[id, "list of application"]
            print ("Updating list of Application")
            if l == str('[]'):
                l = [id_o]
            else:
                l = [l.strip('][').split(', ')][0]
                l = [int(x) for x in l]
                l = l + [id_o]
            df.loc[id, "list of application"] = str(list(set(l)))
            df.to_csv("caretaker.csv")
            
            print ("Sending application to oldie")
            df_o = pd.read_csv("oldies.csv", index_col = 0)
            l = df_o.loc[id_o, "list of Application"]
            if l == str('[]'):
                l = [id]
            else:
                l = [l.strip('][').split(', ')][0]
                l = [int(x) for x in l]
                l = l + [id]
            df_o.loc[id_o, "list of Application"] = str(list(set(l)))
            df_o.to_csv("oldies.csv")
            
            
            
    #Function to Check for response
    def checkeRes(self):
        print ("These are the new oldies added to your schedule:", self.Response)
    
    def rate(self):
        if self.oldies == "None":
            print("\nNo Caretaker to Rate")
        else:
            print ("Here is the list of Oldies you take care of:", self.oldies)
            id = int(input("Enter the id of the Oldie you want to rate: "))
            
            df_o = pd.read_csv("oldies.csv")
            df_o = df_o[df_o["id"] == id].values[0]
            user_o = Oldies(df_o[1:])
            
            r = int(input("Enter Your Rating out of 5: "))
            user_o.rating = ((float(user_o.rating) * user_o.No_of_rating) + r) / (user_o.No_of_rating+1)
            user_o.No_of_rating = user_o.No_of_rating +1
            df_o = pd.read_csv("oldies.csv", index_col = 0)
            df_o.loc[id, "Rating"] = user_o.rating
            df_o.loc[id, "No of Ratings"] = user_o.No_of_rating
            df_o.to_csv("oldies.csv")
    
    
def oldiesFunc(id):
    """
    All functions regarding Oldies
    """
    
    df = pd.read_csv("oldies.csv")
    df = df[df["id"] == id].values[0]
    
    user = Oldies(df[1:])
    print ("Name: " + user.name)
    print ("Age: " + str(user.age))
    print ("Requirement: " + user.req)
    print ("Fee: " + str(user.fee))
    print ("Name of Caretaker: " + user.caretaker)
    print ("Rating: " + str(user.rating))
    
    print ("\nList of operations:")
    print ("1. Update Profile")
    print ("2. Choose an Applicant")
    print ("3. Rate your Caretaker")
    
    c = int(input("Enter your option number"))
    
    if c == 1:
        user.updateProfile(id)
    elif c == 2:
        user.appList()
        user.chooseCaretaker(id)
    else:
        user.rate()
        
        
def caretakerFunc(id):
    """
    All functions regarding caretakers
    """
    
    df = pd.read_csv("caretaker.csv")
    df = df[df["id"] == id].values[0]
    
    user = Caretaker(df[1:])
    print ("Name: " + user.name)
    print ("Age: " + str(user.age))
    print ("Fee: " + str(user.fee))
    print ("id of oldies: " + user.oldies)
    print ("Rating: " + str(user.rating))
    
    print ("\nList of operations:")
    print ("1. Update Profile")
    print ("2. Apply for caretaking position")
    print ("3. Check for application acceptance")
    print ("4. Rate your Oldie")

    c = int(input("Enter your option number"))
    
    if c == 1:
        user.updateProfile(id)
    elif c == 2:
        user.app(id)
    elif c == 3:
        user.checkeRes()
    else:
        user.rate()
        


print ("Welcome to the caretaking service")

print ("Are you an oldie or caretaker?\nType 'O' for oldie.\nType 'C' for caretaker.")

#Add details
u = input()
if u.capitalize() == "O":
    user_type = "Oldies"
elif u.capitalize() == "C":
    user_type = "Caretaker"

print ("Welcome " + user_type)

i = input("Are you new?Y/n")

if i.capitalize() == 'Y':
    if user_type == "Oldies":
         """
         Initialize a new Oldie
         """
         name = input("Enter your name")
         age = input("Enter your age")
         req = input("Enter your requirement")
         fee = input("Enter your fee")
         
         df = pd.read_csv("oldies.csv", index_col = 0)
         info = [len(df)+1, name , age, req, fee, "yes", [], 0, 0, []]
         df.loc[len(df),:] = info
         
         df.to_csv("oldies.csv")
         
    else:
         """
         Initialize a new caretaker
         """
         name = input("Enter your name")
         age = input("Enter your age")
         fee = input("Enter your fee")
         
         df = pd.read_csv("caretaker.csv", index_col = 0)
         info = [len(df)+1, name , age, fee, "yes", [], 0, 0, [], []]
         df.loc[len(df),:] = info
         
         df.to_csv("caretaker.csv")
        

else:

    user_id = int(input("Please Enter your id to login"))
    print ("\nRetreiving your info")
    if user_type == "Oldies":
        oldiesFunc(user_id)
    else:
        caretakerFunc(user_id)