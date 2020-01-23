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
        
        print ("Enter Name")
        name = input()
        print ("Enter Age")
        age = int(input())
        print ("Enter Requirement")
        req = input()
        print ("Enter the maximum fee")
        fee = int(input())
        
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
        
        print ("Do you want to check the list of apllication? Y/n")
        i = input()
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
        
        
        print ("Enter the id of the caretaker you chose:")
        c = int(input())
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
            
            print ("Enter Your Rating out of 5:")
            r = int(input())
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
        
        print ("Enter Name")
        name = input()
        print ("Enter Age")
        age = int(input())
        print ("Enter the maximum fee")
        fee = int(input())
        
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
        
        print ("Do you want to apply for one of the positions?Y/n")
        r = input()
        if r.capitalize() == "Y":
            print ("Enter the new oldie's id")
            id_o = int(input())
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
            print ("Enter the id of the Oldie you want to rate:")
            id = int(input())
            
            df_o = pd.read_csv("oldies.csv")
            df_o = df_o[df_o["id"] == id].values[0]
            user_o = Oldies(df_o[1:])
            
            print ("Enter Your Rating out of 5:")
            r = int(input())
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
    print ("Enter your option number")
    
    c = int(input())
    
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
    print ("Enter your option number")
    
    c = int(input())
    
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

print ("Are you new?Y/n")
i = input()

if i.capitalize() == 'Y':
    if user_type == "Oldies":
         """
         Initialize a new Oldie
         """
         
         print ("Enter your name")
         name = input()
         print ("Enter your age")
         age = input()
         print ("Enter your requirement")
         req = input()
         print ("Enter your fee")
         fee = input()
         
         df = pd.read_csv("oldies.csv")
         info = [len(df)+1, name , age, req, fee, "yes", [], 0, 0, []]
         df.loc[len(df),:] = info
         
         df.to_csv("oldies.csv")
         
    else:
         """
         Initialize a new caretaker
         """
         print ("Enter your name")
         name = input()
         print ("Enter your age")
         age = input()
         print ("Enter your fee")
         fee = input()
         
         df = pd.read_csv("caretaker.csv")
         info = [len(df)+1, name , age, fee, "yes", [], 0, 0, [], []]
         df.loc[len(df),:] = info
         
         df.to_csv("caretaker.csv")
        

else:

    print ("Please Enter your id to login")
    user_id = int(input())
    print ("\nRetreiving your info")
    if user_type == "Oldies":
        oldiesFunc(user_id)
    else:
        caretakerFunc(user_id)