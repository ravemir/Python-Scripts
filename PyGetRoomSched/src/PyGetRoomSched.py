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
            matrix += "\t"
        
        # Add "\n"
        if len(matrix) > 0:
            matrix += "\n"
        
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
    fenixScheduleUrl = "https://fenix.ist.utl.pt/publico/findSpaces.do"
    fenixTagusPOSTData = '_request_checksum_=f67a3295c65e704ecd76a260bd9c1c154de2248f&' \
        'contentContextPath_PATH=%2Fconteudos-publicos%2Fpesquisa-de-espacos&' \
        'method=search&' \
        'net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1082852714%3AsearchType=SPACE&'\
        'net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1082852714%3AlabelToSearch=&'\
        'net_sourceforge_fenixedu_dataTransferObject_spaceManager_FindSpacesBean_1082852714_campuspostback=&'\
        'net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1082852714%3Acampus=net.sourceforge.fenixedu.domain.space.Campus%3A2465311230082&'\
        'net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1082852714%3Abuilding=net.sourceforge.fenixedu.domain.space.Building%3A2972117375196&'\
        'pt.ist.fenixWebFramework.renderers.components.state.LifeCycleConstants.VIEWSTATE_LIST=H4sIAAAAAAAAALVXy28bRRifOHFjp480SZUiVGiQglSBspsHLS2ltIkTF4NDIpy2alAlxrvjeJLx7DAz6zhFVMChHDhxAIEEBw7c%2BAMQSJyQOCEBEv8B4oLgggQSD4lvZtf2uk5a0xYf1juz33yP3%2FecT39BaSXR2CauYyfUlDnzUuKdIlW68cb3D33wNf6oH%2FUV0ICi10lDIIT6tgfgOQSHzgntAJ1TIZw2rpByXuIa2Q7kliMJ94kkUjleUBMBJ1wrR2msiXOZku2SeXvvt%2BOfs%2FmfBlNoZB1lRKD0Ava21oHzFhWXhA8k6%2BiQWVzGjMKSBnwdjYX2S67Jdk0SIEvXDck6GqxTRcuMFNEQ1lrScqiJ0mi4aMxzjXnuMhZni%2BiAF3BNGjrHsAKCkYiAYb7h2i0gGfVCCXboReBAuRWv0VJRaBdsdrtsdls2u22bXWuza2xOsDHy%2FfZSvYJuoP4i2l%2Blvk94iQUaVDqc0Nl4Aw6lqK%2FRaELVEpjIN%2BDLYcpFmNTUsEwX0T6Gd4JQm9UgYFIjGq%2BUN4mnNTrZiyW1wCcAWesYiBoSMhBEamqAHU8oudraB6qBUME7erJ3IZfgQAHM11TvnI0Cra%2BvMzKfxaqqMbh37IvhRx957sfP%2BlEqj4ZYgP089nQgCyirq5KoasD8hjh%2FAZlfZjsDz%2F3mtVGX6HRPQWuDQzkFA2suWqH2ryGEddqBLhF9uh3KoHzubjMk4cqrX72T7X%2F6549SqB%2FyRBKfSvAE%2BBZwCxmJfTsgsK7ad8AOlHBFWGbUCzSacSuU%2ByWBPaIcPzgPQVAN%2FHNCEoElKREsvWr0dTVWvCE0OlommF%2BhulrEZcLWgoiusGjtHkXmeeRueGs0CC4MGZYAz5ke4LHR4ZRoTTDSDsS3Ri665X9OfAegQG3ygAaSwCKpqAbBWsNZo%2BQ%2BACqIQz6ZOnE8NySa61mJtvjlhfzW74%2B9mUmZJBv0JMEQfRo91Xu4Fzg4m3skF50925n%2BseaJXDM7WdhRXpXU8AvANnZ8WrUONMPS%2FqIq3QCUj7QzqJ2jZ0a%2FvS5OPfN%2BCvUVUcYnFRyyiE22sXtoIxMWE6s2rPItr5sQWWpoiVeErWUtBQZabWLmPwFs7P%2Fr8eOf%2FPEuG0%2BhwxDyVOUwWO3b6Mf%2BCmc76%2Bigsj4ubPAAUgKcXA6538qGLGRwHQwl0mwM2HprLYRWEjaJ9kMN9iQVzXoJWyOJrXwga7hZOrNVwoRNheYGM4t5uTEdb2TsxvNkJ17vWXrNTgYSlrd9OFSPOlzQitnhulF0ufOQdcyxXXxsNia6HJbSTVQg6RaX8vOXimvw5pn%2BZor3IQZemZ1glHJGOdkteuDRPivsT6Nj1lLHZL6jTBA4yia6o3cEiEpL7NPAcHpYg%2F%2FtpzX40sU8EjfZsz1QW%2B0UolFqbrpnbY%2Feqq1y7I6INTzIkgXunpUc0Dau2hNDqx0ktQexkNp1CtEfTyBXOdGOCkLpkUogN0iULcQPHSimCrqDZbdGiUxkTZOHiixbxhxvAEEO10SoVuOPEAUVG8oaTU6%2BagkLPNoBjh3sTVl5bQ9kzdZUE9QHukH1rFCNjtQID6cUYRC1U8b2MtgeY70vIrpnkFPd%2BL10H%2FFbCCnzYbD6PxF8sBvBciwWIiiBYQxdpvm1G7zGhbfTm7sV%2Fot7YgK1Bq9JzFWFyKjAdCLQru8LMAbcHEzf%2FPvj8S9TaAi6LPawT2rUK8BUJKFMaVQogiA3IchtCnL9oIYpdzWtEdfDDJDHEqbW0NOhJO78LaygC4407XyRgG4EOqRG03fkb5V3m34DNsNRpCWYOD0yiZLHjOgk0dY0GksMDwtBwAAXIOqsHs1y3i56GpVvI7fLC27SC26nFyaj10hSTsKYIyk2MkCN8ShWSESesHqqR6vtOWCUtcvVeJaERnRgGxp8ybTfeNa8BtLM3hXQQBO%2BZBpV%2BxpzDWJfQOitJHt%2BpdXwTS2AGHA260rXgs2yI%2BDfmS8rQNrTi1ajCInJkjGPQcH0TSOOB%2B8%2BO670B9SPR10oBLNPnDo5NzMzOzc9fXoWRI%2FYccf4yYn99M2EfP2HD%2F%2F8FQ5HV8UQmh10E3RDopfvU47s6Z3mnWEUBiiJDrWVW%2BJhLfkRbEmXVudzS6ZA3KbweQELazwXdXFDVkk29RFdZaSiJ0LGAU25QXnD%2BOPiHWcwGOIIV8aPTsVepmBIdPKGPHkz6%2FBDfMk7sffUqwhcouGYvd3BrU40%2FgXcnRlGcBAAAA%3D%3D'
        
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
            roomUrls[room] = "https://fenix.ist.utl.pt" + tag.contents[1]['href'] 

    return roomUrls

# Main Method
if __name__ == '__main__':
    outfile = "conv-tables.txt"
    androidParse = False
    opt, arg = getopt.getopt(args, "ha")
    # Parse the arguments
    for opt in opts:
      if opt == '-h':
        print 'PyGetRoomSched [-a (output to android format)]'
      elif opt == '-a':
        outfile = "android-conv-tables.txt"
        androidParse = True

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

    # Generate Room array
    roomArray = ''
    for (room,url) in roomNameList.items():
      # ...
      roomArray += 'ClassRoom.create(name: ' + room + '),'

    roomArray = 'rooms = [ ' + roomArray + ' ]'

    # Run through the 'roomNameList'...
    for (roomName, roomUrl) in roomNameList.items():
        # ...opening every link and saving its schedule table...
        table  = get_table_from_url(roomUrl)
        
        # ...converting the table into the Android format...
        if androidParse:
          generatedLine = convert_html_to_android(table)
          generatedLine = roomName + "\n" + generatedLine
        else:
          # Build ruby command to create the room and the schedule for it
          generatedLine = generate_rails_command(table, roomName) + "\n" 

        #...and adding it to the output string
        output += generatedLine
        
    # Write to file
    f = open(outfile, "w")
    f.write(output)
    f.close()
    
