'''
here name is the field you want your values to assign to

url is the ip of your nodemcu followed by http://

path is the database whole path

firebase_link is the link given in the relatime-database tab something-somethingfirebaseio.com


Usage:


import this module as import firebase_simple


and use the functionality as firebase_simple.getting_values(pass the required arguments)


It's for learning usage only I'm not sure how this will work while handling large sets of data
'''
from firebase import firebase


''' Importing firebase library to the code this library is entirely based on this firebase library'''



def sendValues(name,read_content,firebase_link,path):

	database = firebase.FirebaseApplication(firebase_link,None) #authenticates to firebase

	data = {name : read_content} #stores the data in the dictionary

	result = database.patch(path,data)  #sends the data to your realtime database

'''getting_values function is used to send the data for the first time '''

def updateValues(name,firebase_link,path,data):

	database = firebase.FirebaseApplication(firebase_link,None) #Authentication to firebase

	result = database.put(path,name,data) #updates to firebase


"""update_values function is used to update the values in the existing database"""



def deleteValues(name,firebase_link,path):

	database = firebase.FirebaseApplication(firebase_link,None)# authentication factor
	
	result = database.delete(path,name) #deletes the entry to the firebase


"""delete_values function is used to remove certain values from the realtime database"""


"""Thanks for using this library"""