#!/usr/bin/python
'''
A script that fetches the timetables of every room in Taguspark,
and outputs a format adequate to be read from the Study@Tagus 
application.

Depends on the BeautifulSoup library for advanced HTML parsing.

@author: ravemir
@organization: NEERCI
@since: 21/09/2012
@change: 23/04/2013
'''
import sys
import urllib
import BeautifulSoup
import re
import getopt
from bunch import Bunch

import pdb

global hostname 
hostname = "fenix.tecnico.ulisboa.pt"

# Grabs the 'timetable' element from the specified URL
def get_table_from_url(url):
    
    # Open the URL and read the contents into a string
    f = urllib.urlopen(url)
    s = f.read()
    f.close()
    
    # Get the 'timetable' table element
    soup = BeautifulSoup.BeautifulSoup(s)
    sched = soup.find("table", {"class": "timetable"})
    
    return sched

# Get the start and slot time from the given table
def get_start_and_slot_from_table(table):
  sp = BeautifulSoup.BeautifulSoup(table.prettify())

  # This table's starting time-interval is a table header element, of id 'hour0'
  first_slot = sp.find('th', id='hour0').contents[0]

  # Compute the start and slot times by splitting 
  # and calculating the appropriate elements
  start_time = datetime.strptime(first_slot.split('-')[0], '\n %H:%M')
  slot_time = datetime.strptime(first_slot.split('-')[1]  ,"%H:%M\n ") - start_time # TODO Refactor this code section to be prettier

  return start_time, slot_time

# Converts the HTML room snippet to the format used
# in the Study@Tagus application 
def convert_html_to_android(table):
    return convert_html_to_array(table, '\t','\n')


# Converts the HTML timetable into an array of occupations
# By default, occupation is determined by 0's and 1's, but
# lambda expressions may be specified to customize this behavior
def convert_html_to_array(table, item_separator, line_separator,\
                          occupied_function=(lambda i,j: 1), empty_function=(lambda i,j:0)):
    # Make soup for the table
    if table == None:
        print "stop"
    soup = BeautifulSoup.BeautifulSoup(table.prettify())
    rows = soup.findAll("tr")
    
    # For each tableRow (until the 25th, and the first doesn't count)
    matrix = ""
    for (i,tableRow) in enumerate(rows):
        # Make soup for the tableRow, getting all 'td' elements
        moreSoup = BeautifulSoup.BeautifulSoup(tableRow.prettify())
        tableDivisions = moreSoup.findAll("td")
        
        # For each inner 'td'
        for (j,cellElement) in enumerate(tableDivisions):
            # See if 'class' attribute is not 'period-empty-slot'
            if cellElement["class"] != "period-empty-slot":
                # Mark line acoording to the occupied function
                matrix += str(occupied_function(i,j))
            # ...if not...
            else:
                # Mark line with the empty function 
                matrix += str(empty_function(i,j))
            # Add separator 
            matrix += item_separator
        
        # Add a line separator
        if len(matrix) > 0:
            matrix += line_separator
        
    return matrix

# Generates ruby commands to create the schedule in 
# this table on a Rails app, linked to the respective
# room.
def generate_rails_command(table, room, start_time, slot_time):
  # Create the Room
  #returnValue = 'ClassRoom.create name: ' + room # No longer needed (this only builds the array; the for actually creates, afterwards)

  # Call the android version to obtain a converted array
  convertedArray = convert_html_to_android(table)


  # This function takes the table's start time, and 
  # calculates the respective start and end times 
  # through the line index and the slot period. Column
  # numbers are used to calculate the weekday, and 
  # an hardcoded 'class_id' variable is written.
  occupied_function = (lambda i,j: '{ time_start: ' + str(start_time + (i*slot_time)) + ', time_end: ' + str(start_time + ((i+1)*slot_time)) + ', weeknumber: ' + str(j) + ', class_room_id: class_id }')

  # Should call convert_html_toArray with:
  empty_function = (lambda i,j: '')
  bunch_of_functions = Bunch(occupied_function, empty_function)

  convertedArray = convert_html_to_array(table, ',\n  ', '', bunch_of_functions.occupied_function, bunch_of_functions.empty_function)
  # ',\n  ' as the item separator (each item should break the line and tab)
  # '' as a line separator (each item is an item on the array, already)
  # A function factoring in the number of line, column, period interval,
  # this table's start time and the room name
  # A function returning an empty string 
  

# Gets all the names of the rooms with schedules
def get_room_names():
    # Define the fetching strings
    fenixScheduleUrl = "https://" + hostname + "/publico/findSpaces.do"
    fenixTagusPOSTData = "_request_checksum_=f67a3295c65e704ecd76a260bd9c1c154de2248f&"\
        "contentContextPath_PATH=%2Fconteudos-publicos%2Fpesquisa-de-espacos&"\
        "method=search&"\
        "net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A607828615%3AsearchType=SPACE&"\
        "net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A607828615%3AlabelToSearch=&"\
        "net_sourceforge_fenixedu_dataTransferObject_spaceManager_FindSpacesBean_607828615_campuspostback=&"\
        "net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A607828615%3Acampus=net.sourceforge.fenixedu.domain.space.Campus%3A2465311230082&net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A607828615%3Abuilding=net.sourceforge.fenixedu.domain.space.Building%3A2972117375196&pt.ist.fenixWebFramework.renderers.components.state.LifeCycleConstants.VIEWSTATE_LIST=H4sIAAAAAAAAALVXy28bRRifOE7jpI80SZUiVGiQUgmBspsmtPRBKYmTFINDIpy2alAlxrvjeJLx7DAz6zhFVMChPXMAgUQPHLjxB6AicULihARI%2FAeIC4ILEkg8JL6ZXXvXddKatqwUZ2fmm%2B%2F5%2Bx772S%2BoT0k0uoHr2Ak1Zc6slHi7SJVuvPP9Yx99jW%2F1op4Cyip6jTQEQqhnK2t%2B4dI5oR2gcyqE08ZlUl6UuEa2ArnpSMJ9IolUjhfURMAJ18pRGmviXKJkq2TePvjt6G02%2B1N%2FBg2voZwIlJ7D3uYaGlSbVFwUPpCsoQNmcQkzCksa8DU0GtqTfJPtqiRA1lc3JGuov04VLTNSRINYa0nLoSZKo6GiMc815rlLWJwton1ewDVp6DzDCgiGIwKG%2Bbprt4BkxAsl2KHngQPlVrxGC0WhXbDZ7bDZbdnsJja71mbX2JxiY%2BT7yVK9ga6j3iLaW6W%2BT3iJBRpUOpjS2UQDLmWor9FIStUSmMjX4eQg5SJMa2pY9hXRHoa3g1CbVT%2F4pEY0Xi5vEE9rdKIbS2qBT8BlrWsgalDIQBCpqXHsWErJldY%2BUGVDBe%2Fo2e6FXIQLBTBfU719NgJaT087Ml%2FEqqoxhHf0i6FjT7z04%2Be9KLOIBlmA%2FUXs6UAW0ICuSqKqAfMb4vwLyDy5rRz87jWvjbpEp7oCrQWHcgrGrflohZKnIYQN2r4OET06gTIon7%2FfDEmF8spX7w30PvfzrQzqhTyRxKcSIgGxBb%2BFjMSxzQqsq%2FYdfAdKuCIsM%2BoFGh13K5T7JYE9ohw%2FOA8gqAb%2BOSGJwJKUCJZeNTpdiRVvCI0Olwnml6muFnGZsNUgoivMW7tHkPk9dD%2B8NeqHEIYMS3DP6S7cY9HhlGhNMJIA8ebwBbf8z5PfgVOgNnlAA0lgPamoBsFaw12j5B5wVBBDPp06MZ4bEs10rUQifmlucfP3p97NZUyS9XuSYECfRme6h3uBQ7C5R%2FLR3bPt6R9rnso1szMAO8qrkhp%2BBdjGge9TrQtNWNrHVmnUAC8fSjIoydHTI99eEyef%2FzCDeooo55MKDlnEZqCxM7SRgcX4ioXVYivqBiILDS3xsrC1rKVA1iqQBfnH%2F5ODjf1%2FPX300z%2FeZ2MZdBAgT1Ueg9W%2BRT%2F2lznbXkP7lY1xYZ0HkBIQ5HLI%2FVY2DEAG18FQIs1G1tZbayG0krBJtBdqsCepaNZL2BpObS0GsoabpXOgSpiwqdDcYGYxK9en4o2c3XiZbMfrXUuv2clBwvIkhoP1qMMFLcwO1Y2iS%2B2XbGCO7BBjszHeEbCMbnoFkm5%2BYXH2YnEV3jzT30zxPsAgKtPjjFLOKCc7oQf%2BkrvCPhodsZY6JvMdZUDgKJvojt4WIKpPYp8GhtPjGvBqj1bhpIN5JG6ia3ugttopRKPMzFTX2h6%2BU1vl2B0Ra7ifpQvcAyuZ1RZXycTQagdp7UEspHadAvrjCeQKJ9pRQSg9UgnkOomyhfihA8VUQXew7FYpkamsafJQkWVLmON1IMjjmgjVSnwIKKhYKGs0MfGmJSzwaAc4trE3ZeWtXTxrtiabTn2k06meFarRoRrh4aQiDFA7aWwvg%2B2xr%2FdERA%2Fs5Eyn%2F157iP6bCynzYbD6Pz34aKcHy7FYQFDKh7Hrcs3TTuc1Js7cvrlT4b%2Bwq0%2Bg1uBVibmqEBkVmHYPJPV9DsaAG%2F19N%2F7%2BZOzLDBqELos97JMa9QowFUkoUxoViiDITQlym4JcP6hhyl1Na8T1MAPPYwlTa%2BjpUBJ39g5W0AWHm3a%2BSkA3Ah1So6l78rfKu824AZuhCGkpJk6XTKLkMSM6SbU1jUZTw8NcEDDwCxC1V49mOU%2BKnkblu8jtiIKbjoLbHoWJ6DWSlJcw5kiKjQxQYyzCConIU1ZPdmm1vQeMBuxyJZ4loRHt24IGXzLtN541r4I0s3cZNNCEL5hGlXzGXAXsC4DecrrnV1oN39QCwICzUVe6FmyUHQH%2FndmyAk97et5qFHliomTMY1AwfdOII2ijHjuu9AbUj0ddKATTz5w8MXP8%2BPTM1NSpaRA9bMcdEycnjtM34%2FLtHz7%2B81e4HH0qhtDsoJug6xK9%2FpByZNfoxJrDzIxg2DyQKLfAw1r6EGzpK63M5hdMgbhL4fMCFtZ4PurihqySburDuspIRY%2BHjIM35TrlDROPC%2FecwWCII1yZODoV%2BzEFQ6KzaMjTX2ZtcYg%2F8o4VwXEJrsqE8xC%2BgSG%2FY4gZBvBJJxr%2FAoQQU7FtEAAA"        

    # Get the page with the room list (includes POST data)
    f = urllib.urlopen(fenixScheduleUrl, fenixTagusPOSTData)
    html = f.read()
    f.close()
    
    # Get the room list table
    soup = BeautifulSoup.BeautifulSoup(html)
    that = soup.find('table', {'class': 'tab_lay mtop05'})
    html = that.prettify()
    
    # Initialize the rooms dictionary and the regex...
    roomUrls = {}
    p = re.compile(r'( - [a-zA-Z])')
    
    # Get all the 'span' items inside the table...
    soup = BeautifulSoup.BeautifulSoup(html)
    tagList = soup.findAll("span")
    
    # ...for each one of them...
    for tag in tagList:
        # ...check if they have inner tags (if not, this table row has no schedule)
        if len(tag.findChildren()) > 0:
            # ...get the row, fetch all the 'a' tags and access the 4th's text
            # content, splitting it so we get only the room name...
            room = p.split(tag.findParent(name='tr').findAll('a')[4].text)[0]
            print "Found room with schedule: '" + room + "'"
            
            # ...and save the corresponding URL, using the roomName as the key
            roomUrls[room] = "https://" + hostname + tag.contents[1]['href'] 

    return roomUrls

# Main Method
if __name__ == '__main__':
    outfile = "conv-tables.txt"
    androidParse = False

    # Specify available options ('-h' and '-a')
    opts, args = getopt.getopt(sys.argv[1:], "ha")

    # Parse the arguments
    for (opt, arg) in opts:
      if opt == '-h':
        print 'PyGetRoomSched [-a (output to android format)]'
        sys.exit()
      elif opt == '-a':
        outfile = "android-conv-tables.txt"
        androidParse = True
        print "Printing android version to file"
    # Get all the room names with schedules, and their URLs
    roomNameList = get_room_names()
    
    # Initialize output string and the room filter
    output = ""
    roomFilter = ['0 - 65','0 - 67','0 - 69',
                  '1 - 14','1 - 26','1 - 28',
                  '1 - 31','1 - 32',
                  'A1','A2','A3','A4','A5']
    
    # Filter the specified rooms...
    for room in roomFilter:
        roomNameList.pop(room)
        print "Filtering out room '" + room + "'"

    # Run through the 'roomNameList'...
    roomArray = 'rooms = [ ' 
    for (roomName, roomUrl) in roomNameList.items():
        # ...opening every link and saving its schedule table...
        table  = get_table_from_url(roomUrl)
        

        # ...converting the table into the Android format...
        if androidParse:
          generatedLine = convert_html_to_android(table)
          generatedLine = roomName + "\n" + generatedLine
        else:
          # Add room to array
          roomArray += roomName + ', '
          
          # Get this table's staring time and slot time
          start_time, slot_time = get_start_and_slot_time_from_table(table)

          pdb.set_trace()

          # Build ruby command to create the room and the schedule for it
          generatedLine = generate_rails_command(table, roomName, start_time, slot_time) + "\n" 

        #...and adding it to the output string
        output += generatedLine

    # Add the array of rooms and a couple of newlines
    if not androidParse:
      output = roomArray + " ]\n\n"
        
    # Write to file
    f = open(outfile, "w")
    f.write(output)
    f.close()
    
