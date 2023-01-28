# Imports
import sys
from PyQt5 import QtWidgets
import datetime
import csv

def window():
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    win.setGeometry(1200, 300, 720, 720)
    win.setWindowTitle("OFS Ticketing System")
    win.show()
    sys.exit(app.exec_())

window()

# Collect Scale Ticket Number
tickets =  []
suppliers = []
with open("tickets.csv") as t:
    csv_reader = csv.reader(t, delimiter=',')
    for i, row in enumerate(csv_reader):
        tickets.append(int(row[0]))
        suppliers.append(str(row[1]))
t.close()
#print(suppliers)
Scale_Ticket = max(tickets)+1

# Read in data and verify its correctness

Verified = ("no") # while this is no it will reprompt 

while(Verified == "no"):
    # Ask and Read in data

    #Read in the current date and time
    date = datetime.datetime.now()
    Date = str(str(date.day) +"/"+ str(date.month) + "/" + str(date.year))
    txtdate = str(str(date.day) +"_"+ str(date.month) + "_" + str(date.year))
    Time = str(str(date.hour) + ":" + str(date.minute))
    print(Date)
    
    # Read in seed
    Seed = str(input("Please Enter the Seed Type: "))
    Seed = Seed.lower()
    
    # Check to make sure seed is valid type
    Seed_check = False
    while(Seed_check == False):
        if (Seed != "barley" and Seed != "wheat" and Seed != "oats" and Seed != "soybeans" and Seed != "soybean"):
            print("Invalid Seed type provided.")
            Seed = str(input("Please Enter the Seed Type: "))
            Seed = Seed.lower()
        else:
            Seed_check = True
    
    #Read in the variety
    Variety = input("Please enter variety code: ")

    #Read in the supplier
    Supplier = input("Please enter supplier: ")

    #Read in load number
    Load_Num = input("Please enter load number: ")

    #Read in weights
    weight_check = False
    while(weight_check == False):
        Gross_W = float(input("Please enter gross weight in lbs: "))

        Tare_W = float(input("Please enter Tare weight in lbs: "))
        
        if (Gross_W <= Tare_W):
            print("Gross weight cannot be less than tare weight.")
        else:
            weight_check = True

    Net_W = Gross_W - Tare_W

    # Read in wagon ID
    Wagon = input("Please enter the Truck/Wagon ID: ")

    # Read in destination, and check to make sure it is viable
    Destination = input("Please enter destination: ")

    # Read in moisture level
    Moisture = float(input("Please enter Moisture percentage: "))

    # read in FM level
    FM = float(input("Please enter FM percentage: "))
    
    # read in cleanout
    Cleanout = float(input("Please enter the cleanout percentage: "))
    
    # Read in test weight
    TW = float(input("Please enter Test Weight: "))
    
    #Calculate the Bushels
    if (Seed == "wheat" or Seed == "soybeans"):
        Gross_B = Net_W/60
    elif(Seed == "barley"):
        Gross_B = Net_W/48
    elif(Seed == "oats"):
        Gross_B = Net_W/32
        
    Gross_B = round(Gross_B, 2)
    
    #  if FM is greater than 1% then:  Gross Bushels - (FM-1%)*Gross Bushels = Net Bushels
    if (FM > 1.0):
        Abs_FM = FM/100.0
        Net_B = Gross_B - Gross_B*(Abs_FM-0.01)
    else:
        Net_B = Gross_B
        
    #  Net Bushels = Net Bushels(100% - cleanout)
    Abs_Cleanout = Cleanout/100.0
    Net_B = round(Net_B*(1.0-Abs_Cleanout), 2)
    
    
    #print data for verification
    
    print()
    print("Please read in the following information and verify it is correct: ")
    print()
    print("Load #:        ", Load_Num)
    print("Load of:       ", Seed, Variety)
    print("From:          ", Supplier)
    print("Wagon/Truck ID:", Wagon)
    print("To:            ", Destination)
    print("% Moisture:    ", Moisture)
    print("% FM:          ", FM)
    print("% Cleanout:    ", Cleanout)
    print("Test Weight:   ", TW)
    print("Gross Weight:  ", Gross_W, "lbs")
    print("Tare Weight:   ", Tare_W, "lbs")
    print("Net Weight:    ", Net_W, "lbs")
    print("Gross Units:   ", Gross_B, "BU")
    print("Net Units      ", Net_B, "BU")
    print()

    Verified = input("If this information is correct, please enter your name: \nIf this information is not correct, please enter no: ")

# Print information to file
# Try to make this a PDF

with open(str(Scale_Ticket) + "_" + str(Supplier) + "_" + str(txtdate) + '.txt', 'w') as ticket:
    ticket.write("Ohio Foundation Seeds, Inc. \n")
    ticket.write("11491 Foundation Road, PO Box 6 \n")
    ticket.write("Croton, Ohio 43013 \n")
    ticket.write("Phone: 740-893-2501 \n")
    ticket.write("\n")
    ticket.write("Ticket Number:  "+ str(Scale_Ticket)+ "\n")
    ticket.write("Date:           "+ str(Date) + " " + str(Time) + "\n")
    ticket.write("\n")
    ticket.write("Load #:         "+ str(Load_Num)+ "\n")
    ticket.write("Load of:        "+ str(Seed) + " " +str(Variety)+ "\n")
    ticket.write("From:           "+ str(Supplier)+ "\n")
    ticket.write("Wagon/Truck ID: "+ str(Wagon)+ "\n")
    ticket.write("To:             "+ str(Destination)+ "\n")
    ticket.write("\n")
    ticket.write("% Moisture:     "+ str(Moisture)+ "\n")
    ticket.write("% FM:           "+ str(FM)+ "\n")
    ticket.write("% Cleanout:     "+ str(Cleanout)+ "\n")
    ticket.write("Test Weight:    "+ str(TW)+ "\n")
    ticket.write("Gross Weight:   "+ str(Gross_W) + " lbs"+ "\n")
    ticket.write("Tare Weight:    "+ str(Tare_W) + " lbs"+ "\n")
    ticket.write("Net Weight:     "+ str(Net_W) + " lbs"+ "\n")
    ticket.write("\n")
    ticket.write("Gross Units:    "+ str(Gross_B) + " BU"+ "\n")
    ticket.write("Net Units:      "+ str(Net_B) + " BU"+ "\n")
    ticket.write("\n")
    ticket.write("Verified By:    "+ str(Verified)+ "\n")             
ticket.close()

# append scale ticket and supplier information to tickts.csv
with open("tickets.csv", "a") as t:
    t.write("\n"+str(Scale_Ticket) + ", " + str(Supplier))
t.close()