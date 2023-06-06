"""Scale ticket system for Ohio Foundation Seeds."""

# Imports
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import sys
from PyQt5 import QtWidgets
import datetime
import csv


def window():
    """Open a window to take in user inputs."""
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    win.setGeometry(1200, 300, 720, 720)
    win.setWindowTitle("OFS Ticketing System")
    win.show()
    sys.exit(app.exec_())


# window()

# Collect Scale Ticket Number
tickets = []
suppliers = []
with open("tickets.csv") as t:
    csv_reader = csv.reader(t, delimiter=',')
    for i, row in enumerate(csv_reader):
        tickets.append(int(row[0]))
        suppliers.append(str(row[1]))
t.close()

# rint(suppliers)
scale_ticket = max(tickets)+1

# Read in data and verify its correctness

verified = ("no")
# while verified is no, it will reprompt

while verified == "no":
    # Ask and Read in data

    # Read in the current date and time
    date = datetime.datetime.now()
    date_str = f"{date.day}/{date.month}/{date.year}"
    txtdate = f"{date.day}_{date.month}_{date.year}"
    time = f"{date.hour}:{date.minute}"
    print(date_str)

    # Read in seed
    seed = str(input("Please Enter the Seed Type: "))
    seed = seed.lower()

    # Check to make sure seed is valid type
    seed_check = False
    while seed_check is False:
        if (seed != "barley" and seed != "wheat" and seed != "oats"
           and seed != "soybeans" and seed != "soybean"):
            print("Invalid Seed type provided.")
            seed = str(input("Please Enter the Seed Type: "))
            seed = seed.lower()
        else:
            seed_check = True

    # Read in the variety
    variety = input("Please enter variety code: ")

    # Read in the supplier
    supplier = input("Please enter supplier: ")

    # Read in load number
    load_num = input("Please enter load number: ")

    # Read in weights
    weight_check = False
    while weight_check is False:
        gross_weight = float(input("Please enter gross weight in lbs: "))

        tare_weight = float(input("Please enter Tare weight in lbs: "))

        if gross_weight <= tare_weight:
            print("Gross weight cannot be less than tare weight.")
        else:
            weight_check = True

    net_weight = gross_weight - tare_weight

    # Read in wagon ID
    wagon = input("Please enter the Truck/Wagon ID: ")

    # Read in destination, and check to make sure it is viable
    destination = input("Please enter destination: ")

    # Read in moisture level
    moisture = float(input("Please enter Moisture percentage: "))

    # read in FM level
    foreign_matter = float(input("Please enter FM percentage: "))

    # read in cleanout
    cleanout = float(input("Please enter the cleanout percentage: "))

    # Read in test weight
    test_weight = float(input("Please enter Test Weight: "))

    # Calculate the Bushels
    if seed == "wheat" or seed == "soybeans":
        gross_bushels = net_weight / 60.0
    elif seed == "barley":
        gross_bushels = net_weight / 48.0
    elif seed == "oats":
        gross_bushels = net_weight / 32.0

    gross_bushels = round(gross_bushels, 2)

    # if FM is greater than 1%
    # then:  Gross Bushels - (FM-1%)*Gross Bushels = Net Bushels
    if foreign_matter > 1.0:
        foreign_matter_percent = foreign_matter / 100.0
        net_bushels = (gross_bushels
                       - gross_bushels * (foreign_matter_percent - 0.01))
    else:
        net_bushels = gross_bushels

    # Net Bushels = Net Bushels(100% - cleanout)
    cleanout_percent = cleanout/100.0
    net_bushels = round(net_bushels * (1.0 - cleanout_percent), 2)

    # print data for verification
    print()
    print("Please read in the following information and verify it is correct:")
    print()
    print("Load #:        ", load_num)
    print("Load of:       ", seed, variety)
    print("From:          ", supplier)
    print("Wagon/Truck ID:", wagon)
    print("To:            ", destination)
    print("% Moisture:    ", moisture)
    print("% FM:          ", foreign_matter)
    print("% Cleanout:    ", cleanout)
    print("Test Weight:   ", test_weight)
    print("Gross Weight:  ", gross_weight, "lbs")
    print("Tare Weight:   ", tare_weight, "lbs")
    print("Net Weight:    ", net_weight, "lbs")
    print("Gross Units:   ", gross_bushels, "BU")
    print("Net Units      ", net_bushels, "BU")
    print()

    print("If this information is correct, please enter your name:")
    print("If this information is not correct, please enter no:")
    verified = input()

# Print information to file
# Try to make this a PDF

ticket = canvas.Canvas(f"{scale_ticket}_{supplier}_{txtdate}.pdf",
                       pagesize=letter)
# Draw boxes
ticket.setLineWidth(.5)
ticket.setStrokeColorRGB(0.2, 0.5, 0.3)
ticket.rect(15, 685, 580, 90, stroke=1, fill=0)
ticket.rect(15, 15, 580, 670, stroke=1, fill=0)

# Write header
ticket.setLineWidth(.3)
ticket.setStrokeColorRGB(0.0, 0.0, 0.0)
ticket.setFont('Times-Roman', 18)
ticket.drawString(30, 750, "Ohio Foundation Seeds, Inc.")
ticket.setFont('Times-Roman', 12)
ticket.drawString(30, 730, "11491 Foundation Road, PO Box 6")
ticket.drawString(30, 715, "Croton, Ohio 43013")
ticket.drawString(30, 700, "Phone: 740-893-2501")
ticket.drawString(475, 730, "Date:")
ticket.drawString(510, 730, f"{date_str}")
ticket.line(505, 727, 580, 727)
ticket.drawString(475, 715, "Time:")
ticket.drawString(510, 715, f"{time}")
ticket.line(505, 712, 580, 712)
ticket.drawString(475, 700, "Ticket Number:")
ticket.drawString(560, 700, f"{scale_ticket}")
ticket.line(555, 697, 580, 697)

# Write load information
ticket.drawString(30, 655, "Load #:")
ticket.drawString(130, 655, f"{load_num}")
ticket.line(120, 652, 260, 652)
ticket.drawString(30, 640, "Commodity:")
ticket.drawString(130, 640, f"{seed} {variety}")
ticket.line(120, 637, 260, 637)
ticket.drawString(30, 625, "From:")
ticket.drawString(130, 625, f"{supplier}")
ticket.line(120, 622, 260, 622)
ticket.drawString(330, 640, "Wagon/Truck ID:")
ticket.drawString(430, 640, f"{wagon}")
ticket.line(420, 637, 560, 637)
ticket.drawString(330, 625, "To:")
ticket.drawString(430, 625, f"{destination}")
ticket.line(420, 622, 560, 622)

# write weights
ticket.drawString(30, 595, "Weights:")
ticket.drawString(30, 580, "Gross Weight:")
ticket.drawString(130, 580, f"{gross_weight} lbs")
ticket.line(120, 577, 260, 577)
ticket.drawString(30, 565, "Tare Weight:")
ticket.drawString(130, 565, f"{tare_weight} lbs")
ticket.line(120, 562, 260, 562)
ticket.drawString(30, 550, "Net Weight:")
ticket.drawString(130, 550, f"{net_weight} lbs")
ticket.line(120, 547, 260, 547)

# write test values
ticket.drawString(330, 595, "Test Weight:")
ticket.drawString(430, 595, f"{test_weight}")
ticket.line(420, 592, 560, 592)
ticket.drawString(330, 580, "% Moisture:")
ticket.drawString(430, 580, f"{moisture}")
ticket.line(420, 577, 560, 577)
ticket.drawString(330, 565, "% FM:")
ticket.drawString(430, 565, f"{foreign_matter}")
ticket.line(420, 562, 560, 562)
ticket.drawString(330, 550, "% Cleanout:")
ticket.drawString(430, 550, f"{cleanout}")
ticket.line(420, 547, 560, 547)

# write final values
ticket.drawString(330, 505, "Gross Units:")
ticket.drawString(430, 505, f"{gross_bushels} BU")
ticket.line(420, 502, 560, 502)
ticket.drawString(330, 490, "Net Units:")
ticket.drawString(430, 490, f"{net_bushels} BU")
ticket.line(420, 487, 560, 487)
ticket.drawString(330, 460, "Completed By:")
ticket.drawString(430, 460, f"{verified}")
ticket.line(420, 457, 560, 457)

ticket.save()

# append scale ticket and supplier information to tickts.csv
with open("tickets.csv", "a") as t:
    t.write(f"\n{scale_ticket}, {date_str}, {supplier}, {variety}")
t.close()
