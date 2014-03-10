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

# Converts the HTML room snippet to the format used
# in the Study@Tagus application 
def convert_html_to_android(table):
    return convert_html_to_array(table, '\t','\n')


def convert_html_to_array(table, item_separator, line_separator):
    # Make soup for the table
    if table == None:
        print "stop"
    soup = BeautifulSoup.BeautifulSoup(table.prettify())
    rows = soup.findAll("tr")
    
    # For each tableRow (until the 25th, and the first doesn't count)
    matrix = ""
    for tableRow in rows:
        # Make soup for the tableRow, getting all 'td' elements
        moreSoup = BeautifulSoup.BeautifulSoup(tableRow.prettify())
        tableDivisions = moreSoup.findAll("td")
        
        # For each inner 'td'
        for cellElement in tableDivisions:
            # See if 'class' attribute is not 'period-empty-slot'
            if cellElement["class"] != "period-empty-slot":
                # Mark line with '1'
                matrix += "1"
            # ...if not...
            else:
                # Mark line with '0'
                matrix += "0"
            # Add tab
            matrix += item_separator
        
        # Add "\n"
        if len(matrix) > 0:
            matrix += line_separator
        
    return matrix

# Generates ruby commands to create the schedule in 
# this table on a Rails app, linked to the respective
# room.
def generate_rails_command(table, room):
  # Create the Room
  returnValue = 'ClassRoom.create name: ' + room

  # Call the android version to obtain a converted array
  convertedArray = convert_html_to_android(table)
  
  # Run through the array line-by-line
  for line in convertedArray.split('\n'):
    # Check if there are ones or zeroes
      # If so, discover where, and which hours they match
      # ...and build the command string
      'Occupation.create({time_start: , time_end: , weeknumber: , class_room_id: })'


# Gets all the names of the rooms with schedules
def get_room_names():
    # Define the fetching strings
    fenixScheduleUrl = "https://" + hostname + "/publico/findSpaces.do"
    fenixTagusPOSTData = "_request_checksum_=f67a3295c65e704ecd76a260bd9c1c154de2248f&"\
        "contentContextPath_PATH=%2Fconteudos-publicos%2Fpesquisa-de-espacos&"\
        "method=search&"\
        "net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1016610194%3AsearchType=SPACE&"\
        "net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1016610194%3AlabelToSearch=&"\
        "net_sourceforge_fenixedu_dataTransferObject_spaceManager_FindSpacesBean_1016610194_campuspostback=&"\
        "net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1016610194%3Acampus=net.sourceforge.fenixedu.domain.space.Campus%3A2465311230082&"\
        "net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1016610194%3Abuilding=net.sourceforge.fenixedu.domain.space.Building%3A2972117375196&"\
        "pt.ist.fenixWebFramework.renderers.components.state.LifeCycleConstants.VIEWSTATE_LIST=H4sIAAAAAAAAAL1Y32scRRyfXJLmkv5MWqpoS6u0WCrdTRt%2FtKZVk2uunl5N8NKWRhDndudy087NjjOzl4uiqA%2FVVwVFwT5Y6Jt%2FgCj6IIJPggqCTwWh6IOoDwUFf4Dfmd293fSu7dlq7mFvd%2FY735%2Bf74%2FZD35Gg0qizWdwEzuhpsyZkhIvl6nSrVe%2B2f7uF%2Fh8P%2BoroQFFnyctgRDqWxowV9h0RGgH6Jwa4bR1ilSLEjfIUiDPOpJwn0gileMFDRFwwrVylMaaOCcpWaqYu7ev7PiITf0wlEOjCygvAqWnsXd2AY2os1ScED6QLKAN5uEkZhQeacAX0ObQvikkbOclAbLBpiFZQENNqmiVkTIawVpLWg01URptLBvzXGOeexyLyTJa5wVck5YuMKyAYDQiYJgvunYJSMa8UIId%2BihwoNyK12imLLQLNrsdNrttm93UZtfa7BqbM2yMfD99VM%2Bhl1B%2FGa2tU98nvMICDSptyuhsogGbctTXaCyjagVM5IvwZhPlIsxqalgOltEahpeDUJunIfBJg2g8Wz1DPK3R%2Fb1Y0gh8Ai5rbwNRI0IGgkhNjWO3ZpSca68D1UCo4B492LuQE7ChBOZrqpcnW6LPYKxvJTIfw6quMYR388cbd9%2F1%2BOUP%2B1GuiEZYgP0i9nQgS2hY1yVR9YD5LfHIo8j8ckt5uPab21ZTooM9gdaCQzkl49ZC9ITSX0sIG7R1HSL6dAplUL5wsxmSCeXpz98Y7j%2F80%2Fkc6oc8kcSnEiIBsQW%2FhYzEsR0QWNftPSQpKOGKsMqoF2i0361R7lcE9ohy%2FOARAEE98I8ISQSWpEKw9OrR27lY8ZY1zv5sriMw%2FrYqwfwU1fUyrhI2H0T7Skct6Rgy1y03I0ujIQhpyLAEdx3qwV0WLU6FNgQjKTBfGz3mVv%2Fe8zU4CWqVBzSQFNazimoQrDXsNUquAccFcQpkUynGd0uiiZ6VSMUfny6e%2FW3vq%2FmcSbohTxIMaNTood7hX%2BIQfO6RQrR3cmU5iDXP5J5ZGYYV5dVJAz8JbGMgDKr2hgSm2UiCl7ekGZXm7KGxr54XDzz8Tg71lVHeJzUcsojNcKs71CELNNo5Z2FWbEfdQGSmpSWeFba2tRUYsAoMgPz9%2F8rBxv4%2F791x8fe32NYc2gQpQFUBg9W%2BzQbsz3K2vIDWKxvj0iIPIEUgyNWQ%2B%2B3sGIaMboKhRJqFAVt%2FrYXQWsKEaC3UZE9SkdRPWBrNLBUD2cBJKR2uEyZsKiQLzDxMycXxeCFvF54gy%2FHzNUuxWclDAvM0hiPNqOMFbcxubBpFj6%2FcZAOzvUuMzcJdHQHL6cQrkHRHZ4pTJ8rzcOeZfmeK%2BQYGUTmwk1HKGeWkG3qgKqd7hf1ptM1a6pjMd5QBgaNsojt6WYCoQYl9GhhOOzTg1b6ahzfdoHm4Z2jMSdqgmjYzPvnsde1e%2BvHK3hzwMrzvvIFn8tYza7MFPUt7%2BO2L0x2LL0n0LCfaUUEoPVIL5CKJlCV%2B6EDE8LzEXNWIjFSK%2FHEcc7xIpJNmyTQU013RbVQUCxLKlKTYOCbpMmMgT6INNltNjXJmeNjIvgTfD1bmpgozVs3dPQMBmpQd5zTKTYz3HObbrg6zcuyKiEO7nmU7Q3ddJm4tJObSpTehnuzvt7wHTRHK2q9t3qcTXrt9g0VQbpsUYBdPiaevGXlocAo6uGUxTyHUKVwTHmolFgq4IUI1F7%2BEzKzZ8qLRrl0vWMISj1aA4wr2ptS%2FeI2gmSUnidftnfHyrFCNtjQID%2FcpwgCi%2B4y9VbA3DuOaiKhbdhZvmJ1Q%2BQlXpu47NTuRQWdxjgYNTHmap79%2Bv%2BfSJ%2Fy7y7bVjMBkRSTHrORH08stZG7e0uavhYbugBLJz7x7RkOrMB2YQFvpZHBrnHeQxDuznheKaPaf8iAw6pgMwi5sb03e3YuEQ03xZpqAndURuY0B59WybxuMLqsm7I5M9kL26P9TVMjpKsXrniXoOwDKGTNeWGm9yu1ei6HsrD9w3wP3T%2Bzff2BifPzggX%2FZmXKdRffp%2F7DoToeU%2BXBi%2Fj%2FL7h2dZbcai4VWkym8cb3NJ29Xr2OK1uF3jrzZrcIf%2B49mm3NDg%2Bf%2Ben%2Frpzk0Aucw7GGfNKhXgnO0BKRpVCqDIDcjyE0Eub7tFq6mDeJ6mEFIsaxoGXo6lMSduooVnJNGEwc%2BRUA3AmcojcZvyN8q7yaAADYbo76XYeL0yCRq5eajDskcfDTanDleTgcBA78A0coxKRn407FYo%2Bp15HZEwc1Gwe1xwgQ1tkYgJBF5xup9PVpt9wGjYfs4F399gKPKuiU4AlbMAS3%2BOnEBpJm1U1fXGovACwBbAdCbzQ4XtfZkYSYTwIBzpql0IzhTdQT8O1NVBZ72dDRaRJ7YVTHmMZjrfHNUi6CN%2BuyU0R%2FQeLzorFASjaYjdhynL3fKl799749fYHP0cTGE41Cf4VA2l0mT6tcpYV7AwgYvJAcrlD1ljeo6IzW9M2QclJeLlLeM%2BcdubrYqGvLsp7MVZsdf4XaXIY5pGKuE89D14JycRNQwmIQ4tP4BooNt0w4WAAA%3D"
        
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
          # Build ruby command to create the room and the schedule for it
          generatedLine = generate_rails_command(table, roomName) + "\n" 

        #...and adding it to the output string
        output += generatedLine

    # Add the array of rooms and a couple of newlines
    if !androidParse:
      output = roomArray + " ]\n\n"
        
    # Write to file
    f = open(outfile, "w")
    f.write(output)
    f.close()
    
