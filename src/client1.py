import time
import json
import urllib.request
import random

random.seed(11)


fs = "http://elnux1.cs.umass.edu:35402/"

while True:
    
    print("Enter 1 for search")
    print("Enter 2 for lookup")
    print("Enter 3 to buy a book")
    
    choice = input("Enter your choice: ")
    #Provide search options and call search on frontend
    if choice == '1': 
        print()
        #TODO: Get these books from the catalogserver through a query at startup 
        row = ["distributed systems", "graduate school"]
        print("Possible search terms are \n {} \n {}".format("1. distributed systems", "2. graduate school"))
        operation = "search "
        category = int(input("Please enter the category number you would like to search: "))
        if (category-1) >= len(row) or (category - 1)< 0:
            print("Category doesn't exist! Try again!")
            continue
        else:
            operation += row[category - 1]
    elif choice == '2':
        #Call lookup on front end server with book ID
        print()
        operation = "lookup "
        id_num = input("Please input the ID of the book you want to if you don't know the id please search for the category: ")
        operation += id_num
    
    elif choice == '3':
        #Call buy on front end server
        print()
        operation = "buy "
        buy = input("Please input the ID of the book that you want to buy followed by the quantity if you want to buy more than 1 book (eg. - 1 10): ")
        operation += buy
    else:
        print("Wrong choice entered!")
        continue

    operation = operation.replace(' ', '%20')
    #print(operation)
    response = urllib.request.urlopen(fs+operation)

    if choice == '1':
        #Print search results 
        print()
        print("Search results returned: ")
        print("{0: <2} {1: <10}".format("ID", "Book Name"))
        ret = response.read().decode()
        if(ret==str({"items":{}})):
            print("no result")
        else:
            result = json.loads(ret)
            answer = result["items"]
            for row in answer.keys():
                print("{0: <2} {1: <10}".format(answer[row], row))
            print()

    elif choice == '2':
        #print lookup results 
        print()
        print("{0: <2} {1: <50} {2: <30} {3: <5} {4: <5}".format("ID","Book Name","Category", "Stock", "Price"))
        ret = response.read().decode()
        if(ret==str({"items":{}})):
            print("no result")
        else:
            result = json.loads(ret)
            
            for row in result['items']:
                print("{0: <2} {1: <50} {2: <30} {3: <5} {4: <5}".format(row[0],row[1],row[2], row[3] ,row[4]))
            print()

    elif choice == '3':
        #print buy results 
        print()
        print(response.read().decode())
        print()

