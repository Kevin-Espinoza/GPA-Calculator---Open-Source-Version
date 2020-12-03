#****************************************************************************************************************************
#  Program name: "GPA Calculator".  This program takes in a user's transcripts and saves the data to an SQL 
#  Database. The calculated GPA will be outputted in the UI and the terminal. Copyright (C) 2020 Kevin Espinoza                                                                           *
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License  
#  version 3 as published by the Free Software Foundation.                                                                    
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied         
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.     
#  A copy of the GNU General Public License v3 is available here:  <https://www.gnu.org/licenses/>.                            
#****************************************************************************************************************************

#****************************************************************************************************************************
#  Author information:
#  Author name: Kevin Espinoza
#  Author email: k.espinoza1012@csu.fullerton.edu
#  Repository: <https://github.com/kespinoza1012/GPA-Calculator---Open-Source-Version>
#  GPA Calculator
#  Due Date: 2020-Dec-03
#
#  Purpose:
#  The purpose of this file is to save a user's transcripts to a
#  database in MySQL and output their calculated GPA.
#
#  This file:
#  File name: 254_01_FinalProject_OpenSource_Version1.0.py
#  Language: Python 3
#*****************************************************************************************************************************





# Libraries
import mysql.connector
import tkinter as tk
import sqlite3


# NOTE: Line 314 is missing the password for your MySQL server, please enter your server's password

#==========================================================================================#
#==  WINDOW 1  ==  WINDOW 1  ==  WINDOW 1  ==  WINDOW 1  ==  WINDOW 1  ==  WINDOW 1  ======#
#==========================================================================================#

# Create a Loop
root = tk.Tk()
root.title("GPA Calculator")


# This list will save the user input Name 
# A list is used because a bug would cause variables to clear its contents
name = []


# The Save button will save the data the user input and
# will cause a second window to pop up, quitting the first
def destroy_root():
    name.append(nameEntry.get())
    root.destroy()


# Box to get user Name
nameLabel = tk.Label(text="\nPlease enter your Name: ", anchor="w")
nameEntry = tk.Entry(root, width=27)


# Button to save user's name + Destroy current window
saveButton = tk.Button(root, text="Save", command=destroy_root)

# Put all objects in a grid for tidiness
nameLabel.grid(row=0, column=0)
nameEntry.grid(row=0, column=1)
saveButton.grid(row=1, column=0)



# Run the Loop
root.mainloop()

#==========================================================================================#
#==  WINDOW 1  ==  WINDOW 1  ==  WINDOW 1  ==  WINDOW 1  ==  WINDOW 1  ==  WINDOW 1  ======#
#==========================================================================================#







#==========================================================================================#
#==  WINDOW 2  ==  WINDOW 2  ==  WINDOW 2  ==  WINDOW 2  ==  WINDOW 2  ==  WINDOW 2  ======#
#==========================================================================================#

# Dictionary of all Courses that will be saved
courses = dict()

# Create a new Loop
root = tk.Tk()
root.title("GPA Calculator")


# Create a connection to a DataBase
connection = sqlite3.connect('CourseDatabase.db')
# Create cursor
cursor = connection.cursor()


# If the table already exists, drop it and create a new one
try:
    cursor.execute("DROP TABLE Courses")
    cursor.execute("""CREATE TABLE Courses (
    className text,
    letterGrade text,
    numOfUnits text
    )""")

except:
    # If the table doesn't already exist, make it
    cursor.execute("""CREATE TABLE Courses (
    className text,
    letterGrade text,
    numOfUnits text
    )""")


# Function to save data to Database
def save():
    # Create a connection to a DataBase
    connection = sqlite3.connect('CourseDatabase.db')
    # Create cursor
    cursor = connection.cursor()

    # Insert into table
    cursor.execute("INSERT INTO Courses VALUES (:className, :letterGrade, :numOfUnits)",
        {
            'className': className.get(), 
            'letterGrade': letterGrade.get(),
            'numOfUnits': numOfUnits.get()
        }
    )

    # Commit Changes
    connection.commit()
    # Close Connections
    connection.close()

    # Clear the text boxes
    className.delete(0, tk.END)
    letterGrade.delete(0, tk.END)
    numOfUnits.delete(0, tk.END)


# Function to return the student's list of classes w/ all its data
def query():
    # Create a connection to a DataBase
    connection = sqlite3.connect('CourseDatabase.db')
    # Create cursor
    cursor = connection.cursor()

    # Returns Database to a variable named transtripts
    cursor.execute("SELECT * FROM Courses")
    transcripts = cursor.fetchall()


    # i in this case will represent each class in transcripts
    printRecords = ""
    for i in transcripts:
        printRecords += str(i[0]) + ": " + str(i[1]) + ", " + str(i[2]) + " credits \n"
        # Save all data into the courses dict: className = [letterGrade, numOfUnits]
        courses[str(i[0])] = [str(i[1]), float(i[2])]

    # Label that prints the records
    queryLabel = tk.Label(root, text=printRecords)
    queryLabel.grid(row=7, column=0)


    # Commit Changes
    connection.commit()
    # Close Connections
    connection.close()



# Info
label1 = tk.Label(root, text="Welcome: " + name[0])
label2 = tk.Label(root, text="Fill out the information boxes below and click save when you are done. ")
label3 = tk.Label(root, text="Note, all invalid letter grades will be counted as an F. ")
label1.grid(row=0, column=0)
label2.grid(row=1, column=0)
label3.grid(row=2, column=0)

# Labels for each data section for classes
className = tk.Label(root, text="Class Name: ")
className.grid(row=3, column=0)
letterGrade = tk.Label(root, text="Letter Grade: ")
letterGrade.grid(row=4, column=0)
numOfUnits = tk.Label(root, text="Units: ")
numOfUnits.grid(row=5, column=0)

# Entries for each data section for classes
className = tk.Entry(root, width=30)
className.grid(row=3, column=1)
letterGrade = tk.Entry(root, width=30)
letterGrade.grid(row=4, column=1)
numOfUnits = tk.Entry(root, width=30)
numOfUnits.grid(row=5, column=1)


# Save Button
saveButton = tk.Button(root, text="Save", command=save)
saveButton.grid(row=6, column=0, columnspan=2)

# Query Button
queryButton = tk.Button(root, text="Show Transcripts", command=query)
queryButton.grid(row=6, column=1, columnspan=2)

# Calculate Button
calculateButton = tk.Button(root, text="Calculate GPA", command=root.destroy)
calculateButton.grid(row=6, column=2, columnspan=2)

# Commit Changes
connection.commit()
# Close Connections
connection.close()

# Run the Loop
root.mainloop()
#==========================================================================================#
#==  WINDOW 2  ==  WINDOW 2  ==  WINDOW 2  ==  WINDOW 2  ==  WINDOW 2  ==  WINDOW 2  ======#
#==========================================================================================#




#==========================================================================================#
#==  WINDOW 3  ==  WINDOW 3  ==  WINDOW 3  ==  WINDOW 3  ==  WINDOW 3  ==  WINDOW 3  ======#
#==========================================================================================#

# Create a new Loop
root = tk.Tk()
root.title("GPA Calculator")

# Initialize GPA to zero
gpa = 0.0



# Calculate and return the correct amout of credits earned by letter grade
def pointsEarned(letterGrade):
    if letterGrade == 'A'or letterGrade == 'a': 
        return 4.0
    elif letterGrade == 'B' or letterGrade == 'b': 
        return 3.0
    elif letterGrade == 'C' or letterGrade == 'c':
        return 2.0
    elif letterGrade == 'D' or letterGrade == 'd': 
        return 1.0
    else: 
        return 0.0
    



# Calculate the total credits possible and save to a variable
totalCredits = 0.0
for x in courses.items():
    totalCredits += x[1][1]



# Algorithm to Calculate the GPA:
# Total Credits Possible = x[1][1]
# Total Credits Earned = pointsEarned(x[1][0])
for x in courses.items():
    gpa += (x[1][1] * pointsEarned(x[1][0]))
gpa /= totalCredits

# Round the number of decimal places by 2
gpa = round(gpa, 2)


print("GPA: " + str(gpa))


# Label to output final GPA 
className = tk.Label(root, text="\nFinal GPA: " + str(gpa))
className.grid(row=0, column=0)

# GPA to SQL Message 
className = tk.Label(root, text="\nYour transcripts will now be saved to an SQL File. Thank You. \n")
className.grid(row=1, column=0)

# Button to close the program
window3Close = tk.Button(root, text="Close", command=root.destroy)
window3Close.grid(row=2, column=0)



# Run the Loop
root.mainloop()

#==========================================================================================#
#==  WINDOW 3  ==  WINDOW 3  ==  WINDOW 3  ==  WINDOW 3  ==  WINDOW 3  ==  WINDOW 3  ======#
#==========================================================================================#




#==========================================================================================#
#==  SQL  ==  SQL  ==  SQL  ==  SQL  ==  SQL  ==  SQL  ==  SQL  ==  SQL  ==  SQL  =========#
#==========================================================================================#

# Create an sql database and write it to an sql file
sql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="Transcripts"
)

# Create a cursor to navigate the database
mysql_cursor = sql_db.cursor()


# Create the Database called TranscriptDB
# If it exists, drop it and recreate it
mysql_cursor.execute("DROP DATABASE IF EXISTS Transcripts")
mysql_cursor.execute("CREATE DATABASE Transcripts")
mysql_cursor.execute("USE Transcripts")
mysql_cursor.execute("CREATE TABLE Transcript (courseName VARCHAR(50) PRIMARY KEY, letterGrade CHAR, totalUnits FLOAT)")



# Insert entire courses dictionary to the SQL Database 
for x in courses.items():
    mysql_cursor.execute("INSERT INTO Transcript (courseName, letterGrade, totalUnits) VALUES (%s, %s, %s)", (x[0], x[1][0], x[1][1]))
    sql_db.commit() # Save all changes

#==========================================================================================#
#==  SQL  ==  SQL  ==  SQL  ==  SQL  ==  SQL  ==  SQL  ==  SQL  ==  SQL  ==  SQL  =========#
#==========================================================================================#
