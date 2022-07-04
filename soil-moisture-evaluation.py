import matplotlib.pyplot as plt
import numpy as np
import email.utils as eutils 
import time
import datetime
from datetime import datetime
#the import functions are used to invoking other modules such as matplotlib
#numpy, email.utils, time, & datetime


def read_file():
    '''
          The function reads the data from the given file.
          It returns a list containing the data.
          
          Returns:
                list: list of values read from the file.
    '''
    with open('/Users/adaezeaninweze/Desktop/Boxberg_Soil Moisture_MP2-2 and MP6-3_10 min_10 cm.txt') as f:
        lines = f.readlines()
        
    lines = lines[4:] 
    #The functions opens the textfile and reads the lines and returns a list containing the lines
   
    number=0            
    #number starting index for number of data points in lines list from the text file
    date=0              
    #date starting index for dates strings in the lines list
    under=0             
    #under starting index for soil moisture values under the panel in lines list 
    ref=0               
    #ref (reference value) starting index for reference values in the lines list
    begin=0            
    #begin index starting value needed for the loop
       
    for item in lines:
        #for loop to create a new lines list for data extracted in the text file which is now a list, starting from the 4th position in the list
        pos=item.find(" ")
        #This variable is assigned to spaces found in the lines list. This will be used as a reference in below
        number=item[:pos-3] 
         #This variable defines the number for number of data points accessed in the lines list ending at the space (pos)
        pos2=item.find(":")
        #This variable is assigned to search for colon in the line. it is created to detect time, referenced in below
        date=item[pos-2:pos2+3].replace(","," ").replace(" ","")
        #the commas will be replaced with a space and then the spaces will be removed with the second replace function
        if item[pos2-2:pos2+3].replace(","," ").replace(" ","") == '24:00':    
            #Some of the date strings are written as 24:00 but cannot be processed in python.
            #so it needs to be converted to 00:00 and incremented by an extra date
            #under this condition, python selects dates in the lines list with 24:00 and corrects it to the correct datetime format 
            day = date[0:2]
            mon = date[2:5]
            yy =  date[5:7]
            hours = date[7:9]
            mins = date[10:12]
            #first these variables accessed the date string dervived from lines list and assigns day, mon (month), yy (year), hours, and mins (minutes) 
            #based on their position in the date list with 24:00				 
            new_date_str = day+' ' + mon + ' ' + yy +' ' + hours + ":" + mins        
            # variable assigned for the sum of varibales (day, mon, yy, hours, mins) that will form a string to be converted to a datetime function below
            ntuple=eutils.parsedate(new_date_str)
            #this code corrects the 24:00 to  a tuple that is passed to the next variable below 
            timestamp=time.mktime(ntuple)
            # tuple is modified into a timestamp, special format of dates
    
            date = datetime.fromtimestamp(timestamp)
            #the timestamp is now converted to a datetime function
        else:
            date = item[pos-2:pos2+3].replace(","," ").replace(" ","")
            date = datetime.strptime(date, '%d%b%y%H:%M')
          #this condition is for dates that are not 24:00. the date string is now a datetime function
          
        if item[pos2+4:pos2+10]==" \t \n":
            # the following condition evaluates under string values in the lines list
            #the item scans for is a space or a new line (missing value) which is assigned none, no value at all 
            under=None
        else:
            under=item[pos2+4:pos2+10].replace(",",".")
            # under is variable for items in the lines list from the colon (pos2) to 6 spaces after
            # commas are used in the text file and has to be replaced to a period to be recognized as a number by python
            under = float(under) 
            # string value is floated 
        if item[pos2+11:pos2+17] == " \n" or item[pos2+11:pos2+17] =="": 
            # this condition is for cases where there is no value in under and no value in ref
            #under = float(under) 
            ref = None
            #ref is assigned none value
        else:
            #else condition for when there is value in the reference position 
            ref=item[pos2+11:pos2+17].replace(",",".")
            #commas are replaced to period in the string
            ref = float(ref)
            # string ref value is floated
        if item[pos2+4:pos2+6]==" \t" and item[pos2+4:pos2+10] !=" \t \n": 
            #condition when there is a ref value but missing under value 
            under=None
            #under is assgined none value
            ref = item[pos2+6:pos2+12].replace(",",".")
            #ref value is assigned as such
            ref = float(ref) 
            # string ref value is floated
        
        lines[begin]=[int(number), date, under, ref]
        #lines now becomes this new list with this ordering
        begin=begin + 1    # increments the loop each time  
    return lines

def user_input():
    '''
       The function allows the user to put in the values of the date in the format 
       of year, month, day, hours and minutes. The values are stored as a string
       
       Returns:
            string: representing the start date and the finish date of each dry period       
    '''
    date_input_start = [0,0,0,0,0]      
    # date_input_start assigned to this list which has 5 values already set but will be later changed
    date_input_start[0] = input ('Dry Period start year (yyyy): ')   
    #variable assigned to 0 index position of date_input_start for year   
    date_input_start[1] = input ('Dry Period start month (m / mm): ')    
    #variable assigned to 1 index position of date_input_start for month 
    date_input_start[2] = input ('Dry Period start day (d / dd): ') 
    #variable assigned to 2 index position of date_input_start for day
    date_input_start[3] = input ('Dry Period start hour (hh): ')
    #variable assigned to 3 index position of date_input_start for hour
    date_input_start[4] = input ('Dry Period start minutes (mm): ')
    #variable assigned to 4 index position of date_input_start for minutes 
    print()
    date_input_finish = [0,0,0,0,0]
    date_input_finish[0] = input ('Dry Period finish year (yyyy): ')
    #variable assigned to 0 index position of date_input_finish for year
    date_input_finish[1] = input ('Dry Period finish month (m / mm): ')
    #variable assigned to 1 index position of date_input_finish for month
    date_input_finish[2] = input ('Dry Period finish day (d / dd): ')
    #variable assigned to 2 index position of date_input_finish for day
    date_input_finish[3] = input ('Dry Period finish hour (hh): ')
    #variable assigned to 3 index position of date_input_finish for hour
    date_input_finish[4] = input ('Dry Period finish minutes (mm): ')
    #variable assigned to 4 index position of date_input_finish for minutes
    return (date_input_start, date_input_finish)    
     
def dry_period_plot(date_input_start, date_input_finish, lines):   
    '''
       The function is used to plot the graph of the dry periods based on values during the inputed time range
       
       Args:
         date_input_start = string
         date_input_finish = string
         lines = list
    '''
    x=[]
    #assign list for x values (date)
    y=[]
    #assign list for y values (under
    z=[]
    #assign list for y values (reference)

    filterfunc= []
     #empty list to append date input range to later make into a datetime [start time, end time] 
    filterfunc.append([datetime(int(date_input_start[0]),int(date_input_start[1]),int(date_input_start[2]),int(date_input_start[3]),int(date_input_start[4])), datetime(int(date_input_finish[0]),int(date_input_finish[1]),int(date_input_finish[2]),int(date_input_finish[3]),int(date_input_finish[4]))])
    #appends date input in an order that allows python to create a datetime value based on what the user inputed
    
    for items in lines:
        #values in the lines list will be used to extract under and reference values based on time range the user has inputed
        for items3 in filterfunc:
            #loop to append x, y, z values that will be plotted for dry period
            if items3[0] <= items[1] and items3[1] >= items[1]: 
                #condition to make sure time start date and end date are within availabe dates in lines list
                x.append(items[1])
                #start time will be added to x list until it reaches the ends list with dates from the lines list
                y.append(items[2])
                #under values corresponding from start time to end time appended to y list  
                z.append(items[3])
                #reference values corresponding from start time to end time appended to z list
                break
            else:
                pass
             #if the user start and end time are not found in the lines list it will pass

    under_start = y[0]
    #variable assigned to the first value of the y list which is for under the panel soil moisture at start time
    under_finish = y[-1]
    #variable assigned to the last value of the y list which is for reference soil moisture at the end of the dry period
    ref_start = z[0]
    #variable assigned to the first value of the z list which is for reference soil moisture at the start of the dry period
    ref_finish= z[-1]
    #variable assigned to the last value of the z list which is for reference soil moisture at the end of the dry period
    
    SM_decline_under = round(under_start - under_finish, 2)
    #variable that calcuates the soil moisture decline under the panel in the dry period 
    SM_decline_ref = round(ref_start - ref_finish, 2)
    #variable that calcuates the soil moisture decline at the reference in the dry period
    SM_rel_decline_under = round(((under_start - under_finish)/under_start) * 100, 2 )
    #variable that calcuates the soil moisture relative decline under the panel in the dry period
    SM_rel_decline_ref = round(((ref_start - ref_finish)/ref_start) * 100, 2) 
    #variable that calcuates the soil moisture relative decline at the reference in the dry period
    #all values are rounded by 2 decimal place
    
    print("Soil Moisture at 00:00 hrs at 100 mm depth under the panel is: ", under_start)
    print("Soil Moisture at 24:00 hrs at 100 mm depth under the panel is: ", under_finish)
    print()
    print("Soil Moisture at 00:00 hrs at 100 mm depth at reference area is: ", ref_start)
    print("Soil Moisture at 24:00 hrs at 100 mm depth at reference area is: ", ref_finish)
    print()
    print("The decline in soil moisture under the panel is: ", SM_decline_under)
    print("The decline in soil moisture at reference area is: ", SM_decline_ref)
    print()
    print("Relative decline in soil moisture under the panel is: ", SM_rel_decline_under)
    print("Relative decline in soil moisture at the reference area is: ", SM_rel_decline_ref)
    # prints the variables with comments about the information calculated and entered by the user


    fig, ax = plt.subplots()
    #for multiple plots (x,y) & (x,z)
    
    ax.plot(x, y, label = 'MP 2-1 at 100 mm')
    #list x and y are plotted for date and under values with label for plot
    ax.plot(x, z, label = 'MP 6-4 at 100 mm')
    #list x and z are plotted for date and referemce values with label for plot
    
    plt.xticks( fontsize = 7, rotation=90 )
        #add title to plot figure
    plt.title('SM during dry periods at 100 mm depth between under panel area (MP2.2) and reference area (MP 6.3)')
       #add title to plot
    plt.xlabel('Date')
           #add title to x axis
    plt.ylabel('Soil Moisture in %')
        #add title to y axis
    ax.legend()
        #sets legends

    plt.show()
    #visuallize the plot

def description():
    '''
		function to print instructions to the user
	'''
    text = """ 
    Analysis of Soil Moisture Data during Dry Periods and Evaluation of Gradient in Soil Moisture during the Respective Periods
    """
    text2 = """
    A dry period can be characterized as a time when there is no water for a long duration. 
    This period is identified by lack of rainfall, increased temperatures, and very little 
    or no humidity. When rain does not occur for 24 hours after a minimum period of 6 
    continuous days, this is defined as the dry period."""
    text3 = """
    Instructions: 
    Input dry period start date in this format (2/8/2019 or 23/12/2019 00:00)
    Input dry period end date in the format:
        2/8/19 24:00 is entered as 3/8/19 00:00
    """
    text4 = """
    Happy Evaluation!!!
    """
    print(text)
    print(text2)
    print(text3)
    print(text4)

def main(): 
    '''
    Function is call up all other functions
    
    Args:
        all functions created with their arguments if they have: 
        	read_file()
        	description()
        	date_input()
        	dry_period_plot()
    '''
    lines = read_file() 
    description()
    date_input_start, date_input_finish = user_input()
    dry_period_plot(date_input_start, date_input_finish, lines)
    
main()












