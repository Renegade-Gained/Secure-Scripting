#!/usr/bin/python

############################################
##
##  Programmer:     Samuel Sommerschield
##
##  Created:        11/24/21
##  Last Modified:  11/25/21
##
##  Course:         CSC 326 800
##  Due Date:       12/1/21
##
############################################
##
##  Functional Description:
##
##      Take in a file name and path.
##      Load in data from the file.
##      If arguments were provided, use
##      custom dates.
##      Else, use beginning and ending date.
##
##      Print highest high, lowest low,
##      dates, trending up/down
##
##      Print a Histogram with max amount of
##      #'s being 50
##
############################################
##
## Expected Arguments:
##
## Default Execution
## $ python3 AnalyzeCryptoPrice.py
##
## Custom Date Range
## $ python3 AnalyzeCryptoPrice.py date date
##
############################################

# Libraries
import sys

from datetime import datetime
from datetime import date

import csv

############################################
#
#   Initialize Variables
#
############################################

startDate = 0
endDate = 0

highest = 0
lowest = 0

# counter for element
count = 0

# Initialize lists
# Direct from file
dates = []
prices = []

# post processing
processedDates = []
processedPrices = []

# date of generation
today = datetime.today()

# output formatting
separator = "#########################################################"
pound = "#"
newline = "\n"

############################################
#
#   Get Initial Data
#
############################################

# Get file location
file=input("Enter file and path: ")

# An Attempt Will be Made
try:

    # Open the file, read only
    data = open(file, "r")

    # Get the column names from the file
    columnHeaders = data.readline().split(',')

    # Find the column numbers of relevant data
    for element in range(len(columnHeaders)):

        # find date column
        if(columnHeaders[element] == 'date'):
            dateColumn = element

        # find price column
        if(columnHeaders[element] == 'PriceUSD'):
            priceColumn = element

    # grab the rest of the data
    lines = data.readlines()

    # iterate over all data
    for stuff in lines:

        # Get the date column
        dates.append(stuff.split(',')[dateColumn])

        # Get the price column
        prices.append(stuff.split(',')[priceColumn])

        # If there isn't a price but a day, set to 0
        # instead of empty string
        if (prices[count] == ""):
            prices[count] = "0"

        # increment the counter
        count += 1

    # check for command line args
    if(len(sys.argv) > 1):

        # an attempt will be made
        try:

            # set start and end dates to command line args
            startDate = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
            endDate = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()

            # if args are backwards, invert them
            if(startDate > endDate):

                holdDate = startDate
                startDate = endDate
                endDate = holdDate

        # if not enough args, throws error
        except IndexError:

            # let user know
            print("Not Enough Arguments")
            print("Using Default Values")

            # set default to first and last date in file
            startDate = dates[0]
            endDate = dates[(len(dates)-1)]

            # lets user know what dates will be used
            print("")
            print("Start Date: ", startDate)
            print("End Date: ", endDate)

    # else no command line args
    else:

        # start and end date are first and last date in list
        startDate = datetime.strptime(dates[0], '%Y-%m-%d').date()
        endDate = datetime.strptime(dates[(len(dates)-1)], '%Y-%m-%d').date()

    # Close the file
    data.close()

# FileNotFoundError Exception
except FileNotFoundError:

    print("Unable to Find File:", file)
    sys.exit("Exiting...")

# ValueError Exception
except ValueError:

    print("Error Parsing File:", file)
    sys.exit("Exiting...")
    
# Default Error
except:

    print("Default Error")
    sys.exit("Exiting...")

############################################
#
#   Data Processing
#
############################################

# get coin shorthand from filename
identifier = file.split('.')
designation = identifier[0]

# reset count for new loop
count = 0

# process data and remove parts we do not need
if(startDate != datetime.strptime(dates[0], '%Y-%m-%d').date()) or (endDate != datetime.strptime(dates[(len(dates)-1)], '%Y-%m-%d').date()):
        for date in dates:
            element = datetime.strptime(date, '%Y-%m-%d').date()

            # if in range
            if(startDate <= element) and (endDate >= element):

                # add data to processed lists
                processedDates.append(date)
                processedPrices.append(prices[count])

            # increment counter
            count+=1

# else processed lists = original lists
else:
    processedDates = dates
    processedPrices = prices

# reset counter
count = 0

# for all the remaining dates
for element in range(len(processedDates)):

    # until a price > 0 is found, count < 1
    # count = 1 when a price > 0 is found
    if(count < 1):
        
        if(float(processedPrices[element])) > 0:
            
            lowest = float(processedPrices[element])
            highest = float(processedPrices[element])
            
            highDay = processedDates[element]
            lowDay = processedDates[element]

            count+=1

    # if current day's price is the higher
    # it's the new high
    if(float(processedPrices[element]) > highest):
        
        highest = float(processedPrices[element])
        highDay = processedDates[element]

    # if current day's price is the lowest
    # it's the new low
    if(float(processedPrices[element]) < lowest):
        
        lowest = float(processedPrices[element])
        lowDay = processedDates[element]

# an attempt will be made
try:

    # if up
    if( float(processedPrices[0]) < float(processedPrices[(len(processedPrices) -  1)]) ):

        # find the difference in value
        diff = float(processedPrices[(len(processedPrices) - 1)]) - float(processedPrices[0])

        # Find the first value that is not 0
        for i in range(len(processedPrices)-1):

            # if element is 0, found
            if (float(processedPrices[i]) > 0):
            
                original = float(processedPrices[i])

                # get me outta here
                break

        # if it's still 0, can't divide by 0
        if (original == 0):
        
            timePeriodChange = "Increase \t\t$" + "%.2f" % diff + newline + pound + "\tPercent Increase: \t" + "Not a Number"

        # else it worked
        else:

            percent = diff / original * 100
            timePeriodChange = "Increase: \t\t+$" + "%.2f" % diff + newline + pound + "\tPercent Increase: \t+" + "%.2f" % percent + "%"

    # else if down
    elif( float(processedPrices[0]) > float(processedPrices[(len(processedPrices) - 1)]) ):

        # find the difference in value
        diff = float(processedPrices[0]) - float(processedPrices[(len(processedPrices)-1)] )

        # Find the first value that is not 0
        for i in range(len(processedPrices)-1):

            # if element is 0, found
            if (float(processedPrices[i]) > 0):
            
                original = float(processedPrices[i])

                # get me outta here
                break
        
        # if it's still 0, can't divide by 0
        if (original == 0):
        
            timePeriodChange = "Decrease: \t\t$" + "%.2f" % diff + newline + pound + "\tPercent Decrease: \t" + "Not a Number"

        # else it worked
        else:

            percent = diff / original * 100
            timePeriodChange = "Decrease: \t\t-$" + "%.2f" % diff + newline + pound + "\tPercent Decrease: \t-" + "%.2f" % percent + "%"

    # else neither 
    else:
        timePeriodChange = "Growth: No Change"

# default catch - all

except:

    # I'm not recovering from out of bounds dates
    sys.exit("Bad Dates")

# minutes formatting
if(today.minute < 10):
    minuteString = "0" + str(today.minute)
else:
    minuteString = str(today.minute)

############################################
#
#   Print Relevant Data
#
############################################

print(newline)

print(separator)
print(pound)

print(pound, "\t" + designation.upper())
print(pound)
print(pound, "\t" + "File: \t\t" + file)
print(pound, "\t" + "Generated: \t" + str(today.date()), str(today.hour) + ":" + minuteString)

print(pound)
print(separator)
print(pound)

print(pound, "\tStarting Date of Slice:\t" + str(startDate))
print(pound, "\tEnding Date of Slice:\t" + str(endDate))

print(pound)
print(separator)
print(pound)

print(pound, "\tDate of Highest Value:\t" + str(highDay))
print(pound, "\tValue:\t\t\t$" + "%.2f" % highest)

print(pound)

print(pound, "\tDate of Lowest Value:\t" + str(lowDay))
print(pound, "\tValue:\t\t\t$" + "%.2f" % lowest)

print(pound)
print(separator)
print(pound)

print(pound, "\t" + timePeriodChange)

print(pound)
print(separator)

print(newline)
print(newline)
print(newline)

############################################
#
#   Create a Visual Aid
#
############################################

# reset counter
counter = 0

# Output formatting
print("  Date", "\t\tPrice")

# create histogram
for i in range(len(processedDates)):

    # scale data for human eyeballs
    scaled =  (float(processedPrices[i]) / highest) * 50

    # Guarantee that if the value is not 0, it shows up
    if( scaled > 0 and scaled < 1):
        scaled = 1

    # reset bar "length"   
    bar = ""

    # create bars
    for i in range (int(scaled)):
        bar = bar + pound

    # print bars
    print(processedDates[counter], ":", bar)

    counter+=1

############################################
#
#   Output Data to a CSV File
#
############################################

# reset counter
counter = 0

# custom file name
writeFile = designation.upper() + "." + str(today.date()) + ".ProcessedData.csv"

# open file to output to
with open(writeFile, 'w', newline='') as csvfile:

    # create the writer
    writer = csv.writer(csvfile, delimiter=',')

    # column headers
    writer.writerow(['Date', 'PriceUSD'])

    # for each item in each list
    for i in range(len(processedDates)):

        # get current item from each list
        writeString = [str(processedDates[counter]), str(processedPrices[counter])]

        # write them to csv file
        writer.writerow(writeString)

        # increment counter
        counter += 1
