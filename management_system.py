#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 01:36:59 2019

@author: nilesh
"""

import mysql.connector,random,re,datetime,os,time
from  prettytable import PrettyTable
#creating database
try:
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="")
    mycursor=mydb.cursor()
    mycursor.execute("CREATE DATABASE mydatabase")
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="mydatabase")
    mycursor=mydb.cursor()
    mycursor.execute("CREATE TABLE test (uid VARCHAR(15) PRIMARY KEY, fname VARCHAR(20), lname VARCHAR(20), mo_number VARCHAR(10), email VARCHAR(50))")
except:
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="mydatabase")
    mycursor=mydb.cursor()

#defining functions

#validation of email
def isValidEmail(email):
    if len(email) > 7:
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) != None:
            return True
    return False

#unique Id generator
def uidgenerator():
    d=datetime.date.today()
    x=d.strftime("%Y%m")
    rand_num=random.randint(10000,99999)
    gen_uid="SGVU"+str(x)+str(rand_num)
    return gen_uid

#Insert function
def insert():
    fname=input("\n\nEnter First Name: ")
    while True:
        if len(fname)==0:
            fname=input("Cannot be empty...\nEnter First Name: ")
        else:
            break
    lname=input("Enter Surname: ")
    while True:
        if len(lname)==0:
            lname=input("Cannot be empty...\nEnter Surname: ")
        else:
            break
    mo_number=input("Enter Your Mobile Number")
    while True:
        if mo_number.isnumeric() and len(mo_number)==10:
            break
        else:
            mo_number=input("Invalid Number...\nEnter a Valid Number: ")
    email=input("Enter Email: ")
    #checking email validity
    while True:
        if isValidEmail(email):
            break
        else:
            email=input("Invalid Email..\nEnter a valid Email: ")
            
    uid=uidgenerator()
    sql= "INSERT INTO test (uid,fname,lname,mo_number,email) VALUES (%s,%s,%s,%s,%s)"
    values=(uid,fname,lname,mo_number,email)
    try:
        mycursor.execute(sql,values)
        mydb.commit()
        print("\n\tRow inserted\n\n\tUnique ID is: "+uid)
        input('\n\nPress Any Key to return to Main Menu..')
    except:
        uid=uidgenerator()
        values=(uid,fname,lname,mo_number,email)
        mycursor.execute(sql,values)
        mydb.commit()        
        print("\n\tRow inserted\n\n\tUnique ID is: "+uid)
        input('\n\nPress Any Key to return to Main Menu..')

#searching Record
def search():
    adr = input("\n\nEnter the Unique ID: ")
    sql = "SELECT * FROM test WHERE uid = "+"'"+str(adr)+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    x1=PrettyTable()
    x1.field_names=['UID','First Name','Surname','Mobile','Email']
    for x in myresult:
        x1.add_row(x)
        print(x1)
        input('\n\nPress Any Key to return to Main Menu..')
    if len(myresult)==0:
        print("NO RECORD FOUND...")
        input('\n\nPress Any Key to return to Main Menu..')
        return

#showing all records
def showall():
    sql="SELECT * FROM test"
    mycursor.execute(sql)
    myresult=mycursor.fetchall()
    x1=PrettyTable()
    x1.field_names=['UID','First Name','Surname','Mobile','Email']
    for x in myresult:
        x1.add_row(x)
    print(x1)
    input('\n\nPress Any Key to return to Main Menu..')

#deleting record
def delete():
    del_uid=input("\n\nEnter UID to delete: ")
    sql = "SELECT * FROM test WHERE uid = "+"'"+str(del_uid)+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print("\nUID: ",x[0],"\nName: ",x[1],x[2],"\nMobile Number: ",x[3],"\nEmail: ",x[4],"\n\n")
    choice=input("Are you sure you want to delete it.(y/n)")
    if choice=='y' or choice=='Y':
        sql = "DELETE FROM test WHERE uid = "+"'"+str(del_uid)+"'"
        mycursor.execute(sql)
        mydb.commit()
        print("Record Deleted..")
        input('\n\nPress Any Key to return to Main Menu..')
    else:
        print("Deletation Cancelled")
        input('\n\nPress Any Key to return to Main Menu..')

#updating database record
def edit():
    edit_uid=input("\n\nEnter UID of Person to edit: ")
    #searching for record
    search_sql = "SELECT * FROM test WHERE uid = "+"'"+str(edit_uid)+"'"
    mycursor.execute(search_sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print("\nUID: ",x[0],"\nName: ",x[1],x[2],"\nMobile Number: ",x[3],"\nEmail: ",x[4],"\n\n")
    if len(myresult)==0:
        print("NO RECORD FOUND...")
        return
    
    edit_field=input("\n1.First Name\n2.Surname\n3.Mobile Number\n4.Email\n5.Return to Main Menu\nWhich Field you want to edit:")
    if edit_field=='1':
        new_content=input("Enter New Name: ")
        while True:
            if len(new_content)==0:
                new_content=input("Cannot be empty...\nEnter First Name: ")
            else:
                break
        sql = "UPDATE test SET fname = '"+str(new_content)+"' WHERE uid = "+"'"+str(edit_uid)+"'"
        mycursor.execute(sql)
    elif edit_field=='2':
        new_content=input("Enter New Surname: ")
        while True:
            if len(new_content)==0:
                new_content=input("Cannot be empty...\nEnter Surname: ")
            else:
                break
        sql = "UPDATE test SET lname = '"+str(new_content)+"' WHERE uid = "+"'"+str(edit_uid)+"'"
        mycursor.execute(sql)
    elif edit_field=='3':
        new_content=input("Enter New Mobile Number: ")
        while True:
            if new_content.isnumeric() and len(new_content)==10:
                break
            else:
                new_content=input("Invalid Number...\nEnter a Valid Number: ")
        sql = "UPDATE test SET mo_number = '"+str(new_content)+"' WHERE uid = "+"'"+str(edit_uid)+"'"
        mycursor.execute(sql)
    
    elif edit_field=='4':
        new_content=input("Enter New Email: ")
        while True:
            if isValidEmail(new_content):
                break
            else:
                new_content=input("Invalid Email..\nEnter a valid Email: ")
        sql = "UPDATE test SET email = '"+str(new_content)+"' WHERE uid = "+"'"+str(edit_uid)+"'"
        mycursor.execute(sql)
    elif edit_field=='5':
        return
    else:
        print("Enter a valid option...")
    mydb.commit()
    mycursor.execute(search_sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print("\nUID: ",x[0],"\nName: ",x[1],x[2],"\nMobile Number: ",x[3],"\nEmail: ",x[4],"\n\n")
    print("Database Updated")
    input('\n\nPress Any Key to return to Main Menu..')


while True:
    print("====================================================================================")
    print("                             UNIQUE ID MANAGEMENT                                   ")
    print("====================================================================================\n")
    print("  Made by: NILESH BHADANA\t\t\t\n           B.Tech. 4 Sem")
    print("------------------------------------------------------------------------------------\n\n")
    print("1. Insert New\n2. Edit Record\n3. Search Record\n4. Delete Record\n5. Show All Records\n6. Exit")
    main_choice=input("Enter Your Choice: ")
    if main_choice=='1':
        insert()
    elif main_choice=='2':
        edit()
    elif main_choice=='3':
        search()
    elif main_choice=='4':
        delete()
    elif main_choice=='5':
        showall()
    elif main_choice=='6':
        break
    else:
        print("Enter a Valid Choice.")
        time.sleep(0.8)
    
    os.system('clear')
