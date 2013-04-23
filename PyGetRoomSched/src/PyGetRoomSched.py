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

# Gets all the names of the rooms with schedules
def get_room_names():
    # Get the page with the room list (includes POST data)
    f = urllib.urlopen("https://fenix.ist.utl.pt/publico/findSpaces.do",
                        '_request_checksum_=f67a3295c65e704ecd76a260bd9c1c154de2248f&'+
                        'contentContextPath_PATH=%2Fconteudos-publicos%2Fpesquisa-de-espacos&'+
                        'method=search&'+
                        'net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A764323587%3AsearchType=SPACE&'+
                        'net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A764323587%3AlabelToSearch=&'+
                        'net_sourceforge_fenixedu_dataTransferObject_spaceManager_FindSpacesBean_764323587_campuspostback=&net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A764323587%3Acampus=net.sourceforge.fenixedu.domain.space.Campus%3A2465311230082&'+
                        'net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A764323587%3Abuilding=net.sourceforge.fenixedu.domain.space.Building%3A2972117375196&'+
                        'pt.ist.fenixWebFramework.renderers.components.state.LifeCycleConstants.VIEWSTATE_LIST=H4sIAAAAAAAAALVXzW8bRRSfOEnjpC1pkipFqNAgBQmBspsPWlpKWxInLgaHRjht1aAexrtje5rx7DAz62yKQMChN5A4gECiBw6oF%2F4ABBInJE5IgMSFAyfEpYILEkjAgTeza3tdJ61pYQ%2Brndk37%2BP3PueTX9CgkmjiCm5gJ9SUOYtS4u0iVTp647sHP%2FgKX%2B9HfQU0oOhVEgmEUN%2FWALxH4NApoR2gcyqE0%2BgiKeclrpOtQG46knCfSCKV4wV1EXDCtXKUxpo4FyjZKpmv93478hlb%2FHkog8Y2UFYESi9hb3MDOG9ScV74QLKB7jOLC5hRWNKAb6CJ0P7JNdmuSwJkgw1DsoGGGlTRMiNFNIK1lrQcaqI0Gi0a81xjnruKxcki2ucFXJNI5xhWQDAWEzDMq67dApJxL5Rgh14GDpRb8RqtFIV2wWa3y2a3ZbPbttm1NrvG5hQbI99vL9XL6DXUX0R7a9T3CS%2BxQINKB1I6G2%2FAoQz1NRpPqVoCE3kV%2FhygXIRpTQ3LwSLaw%2FB2EGqzGgJM6kTjc%2BUrxNMaHe3FknrgE4CsdQxEjQgZCCI1NcBOppRca%2B0D1UCo4Bs92buQ83CgAOZrqrdPxoHW19cZmc9iVdMY3Dvx%2BegjDz%2F306f9KJNHIyzAfh57OpAFNKxrkqhawPxInHkGmSe7lYX3XvMZNSQ63lPQ2uBQTsHAmotXqP1EQlin7esS0afboQzK5%2B42Q1KuvPTlO8P9T9%2B8nkH9kCeS%2BFSCJ8C3gFvISOLbAYF1zX4DdqCEK8Iyo16g0ZxbodwvCewR5fjBGQiCWuCfEpIILEmJYOnV4r9rieKR0OhQmWB%2BkepaEZcJWw9iusKytXscmffBu%2BGt0RC4MGRYAjwneoDHRodTonXBSCoQf%2FxW%2F3DjrZsACtQmD2ggCSySimoQrDWcNUruAaCCJOTTqZOwiSRa6FmJtvjVpfzm74%2B9mc2YJBvyJMEQfRo91Xu4Fzg4m3skF5892Zn%2BieapXDM7w7CjvBqp4xeAbeL4QdU60AxL%2B8RVOgKUD7YzqJ2jJ8a%2FuSqOnX4%2Fg%2FqKKOuTCg5ZzGY42jm0kQmLqTUbVvmW102IrERa4nPC1rKWAgOtNjH3rwA29v%2F1%2BJGP%2F3iXTWbQAQh5qnIYrPZt9GP%2FHGfbG2i%2Fsj4uVHkAKQFOLofcb2XDMGRwAwwl0mwM2HprLYRWEjaJ9kIN9iQVzXoJW2OprXwg67hZOodrhAmbCs0NZhaLsjqbbGTtxvNkO1nvWnrNThYSlrd9ONKIO1zQitnRhlF0tfOQdczhHXxsNqa6HJbRTVQg6ZZX8ovni%2Bvw5Zn%2BZor3fQy8Mj%2FFKOWMcrJT9MCrfVbYR6PD1lLHZL6jTBA4yia6o7cFiBqU2KeB4fSQBv%2FbX%2Bvwp4t5LG66Z3ugttopRKPMwmzP2h66VVvl2B2RaLifpQvcPSs5oG1ctSeGVjtIaw9iIbUbFKI%2FmUAucaIdFYTSI5VAVkmcLcQPHSimCrqDZbdOiUxlTZOHii1bxRxXgSCH6yJUa8lPiIKKDWWNpqdfsYQFHu8Axw72pqy8uguyZmumCer93aB6VqhGB%2BuEhzOKMIjaGWN7GWxPsN4TE90zyJlu%2FF76D%2FFbCinzYbD6PxF8oBvBciIWIiiFYQJdtvm3G7xo5u0b%2FTsV%2FrO7YgK1Bq9LzFWFyLjAdCLQru9LMAZcGxq89vdHk19k0Ah0Wexhn9SpV4CpSEKZ0qhQBEFuSpDbFOT6QR1T7mpaJ66HGSCPJUytoadDSdzFW1hBFxxr2vkiAd0IdEiNZu%2FI3yrvNv0GbEbjSEsxcXpkEiePGdFJqq1pNJEaHpaCgAEuQNRZPZrlvF30NCrfRm6XF9y0F9xOL0zHn7GknIQxR1JsZIAak3GskJg8ZfVMj1bbc8Bo2C7XklkSGtG%2BLWjwJdN%2Bk1nzMkgzexdBA034imlU7WvMZYh9AaF3Ot3zK62GL5SuO4tlBcB6etkqEBs%2BXTLWMKiPvum7yZzdZ6eT%2FoD6yWQLeT%2F%2FxLGjC3Nz8wuzs8fnQdKYnW6MW5zELV9Pyde%2F%2F%2FDPX%2BFwfDMMobdB80A29W5TUryAhXWei%2FujIauk2%2BWYrjFS0VMh46C4rFIeGUvP3nG6gfGIcGUQcir2mgLjl5M35Ok7T4fJyfXp0d3nSUXgegrH7L0J7ksi%2Bgd36MlGyg8AAA%3D%3D')
    html = f.read()
    f.close()
    
    # Get the room list table
    soup = BeautifulSoup.BeautifulSoup(html)
    html = soup.find('table', {'class': 'tab_lay mtop05'}).prettify()
    
    
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
    for (roomName, roomUrl) in roomNameList.items():
        # ...opening every link and saving its schedule table...
        table  = get_table_from_url(roomUrl)
        
        # ...converting the table into the Android format...
        androidArray = convert_html_to_android(table)
        androidArray = roomName + "\n" + androidArray
        
        #...and adding it to the output string
        output += androidArray
        
        
    # Write to file
    f = open("conv-tables.txt", "w")
    f.write(output)
    f.close()
    
