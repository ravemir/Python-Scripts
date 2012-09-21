'''
Created on 21 de Set de 2012

@author: ravemir
'''

import urllib

import BeautifulSoup
import re

def get_table_from_url(url):
    
    # Open the url and read the contents into a string
    f = urllib.urlopen(url)
    s = f.read()
    f.close()
    
    # Get the 'timetable' table element
    soup = BeautifulSoup.BeautifulSoup(s)
    sched = soup.find("table", {"class": "timetable"})
#    if sched != None
#        soup.find("table", {"class": "timetable"})
    
    return sched


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
            # ...if not
            else:
                # Mark line with '0'
                matrix += "0"
            # Add tab
            matrix += "\t"
        
        # Add "\n"
        if len(matrix) > 0:
            matrix += "\n"
                
        
    return matrix


def get_room_names():
    # Get the relevant page list
#    f = urllib.urlopen("https://fenix.ist.utl.pt/publico/findSpaces.do",
#                       '_request_checksum_:f67a3295c65e704ecd76a260bd9c1c154de2248f&contentContextPath_PATH:%2Fconteudos-publicos%2Fpesquisa-de-espacos&method:search&net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1082671433%3AsearchType:SPACE&net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1082671433%3AlabelToSearch:&net_sourceforge_fenixedu_dataTransferObject_spaceManager_FindSpacesBean_1082671433_campuspostback:&net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1082671433%3Acampus:net.sourceforge.fenixedu.domain.space.Campus%3A2465311230082&net.sourceforge.fenixedu.dataTransferObject.spaceManager.FindSpacesBean%3A1082671433%3Abuilding:net.sourceforge.fenixedu.domain.space.Building%3A2972117375196&pt.ist.fenixWebFramework.renderers.components.state.LifeCycleConstants.VIEWSTATE_LIST:H4sIAAAAAAAAALVXy28bRRifOHHjpI80SZUiVGiQgoRA2c2DlpbSh%2BPExeDQCKetGlSJ8e44nmY8O8zMOk4RFXCouHDgAAKJHjggLvwBCCROSJyQAIkLB06ISwUXJJCAA9%2FMru11nbSmLXtY7cx%2B8z1%2B33M%2B%2FRWllUTjV3AdO6GmzMlKibeKVOnGG98%2F9MHX%2BEY%2F6iugAUWvkoZACPVtDsB7GA6dFNoBOqdCOG1cJOW8xDWyGcgNRxLuE0mkcrygJgJOuFaO0lgT5wIlmyXz9d7vhz9n2V8GU2h0DWVEoPQC9jbWgPMGFeeFDyRraJ9ZXMCMwpIGfA2Nh%2FZPrsl2VRIgS9cNyRoarFNFy4wU0TDWWtJyqInSaKRozHONee4yFieKaI8XcE0aOsewAoLRiIBhvu7aLSAZ80IJduhF4EC5Fa%2FRUlFoF2x2u2x2Wza7bZtda7NrbE6wMfL99lK9gq6h%2FiLaXaW%2BT3iJBRpU2p%2FQ2XgDDqWor9FYQtUSmMjX4c9%2BykWY1NSwTBfRLoa3glCb1SBgUiManytfIZ7W6EgvltQCnwBkrWMgaljIQBCpqQF2IqHkSmsfqAZCBd%2Foqd6FnIcDBTBfU711Igq0vr7OyHwWq6rG4N7xL0YefeS5nz%2FrR6k8GmYB9vPY04EsoCFdlURVA%2BY3xOkzyDyZzQy8d5vPRl2iYz0FrQ0O5RQMrLlohdpPQwjrtD1dIvp0O5RB%2BdzdZkjClZe%2Bemeo%2F5mbN1KoH%2FJEEp9K8AT4FnALGYl9OyCwrtpvwA6UcEVYZtQLNJp1K5T7JYE9ohw%2FOA1BUA38k0ISgSUpESy9avR3JVa8ITQ6WCaYX6S6WsRlwlaDiK6waO0eQ%2BZ94G54azQILgwZlgDP8R7gsdHhlGhNMJIIxJ%2B%2B0z9%2B8vZNAAVqkwc0kAQWSUU1CNYazholdwFQQRzyydSJ2TQkmu9Zibb45YX8xh%2BPv5lJmSQb9CTBEH0aPd17uBc4OJt7JBedPdGZ%2FrHmiVwzO0Owo7wqqeEXgG3s%2BLRqHWiGpX2iKt0AlA%2B0M6ido8fHvr0qjp56P4X6iijjkwoOWcRmqLF9aCMTFpMrNqzyLa%2BbEFlqaInPCVvLWgoMtNrE7H8C2Nj%2F9xOHP%2F7zXTaRQvsh5KnKYbDat9GP%2FXOcba2hvcr6uLDOA0gJcHI55H4rG4Ygg%2BtgKJFmY8DWW2shtJKwSbQbarAnqWjWS9gaTWzlA1nDzdI5VCVM2FRobjCzyMr1mXgjYzeeJ1vxesfSa3YykLC87cPhetThglbMjtSNosudh6xjDm3jY7Mx2eWwlG6iAkm3uJTPni%2Buwpdn%2Bpsp3vsYeGVuklHKGeVku%2BiBV%2FussI9Gh6yljsl8R5kgcJRNdEdvCRCVltingeH0sAb%2F21%2Br8KeLeSRuqmd7oLbaKUSj1PxMz9oevFVb5dgdEWu4lyUL3D0rOaBtXLUnhlY7SGoPYiG16xSiP55ALnGiHRWE0iOVQK6TKFuIHzpQTBV0B8tulRKZyJomDxVZtow5XgeCHK6JUK3EPyEKKjaUNZqaetUSFni0Axw72Juy8toOyJqt6SaoD3SD6lmhGh2oER5OK8IgaqeN7WWwPcZ6V0R0zyCnuvF76T7itxBS5sNg9X8i%2BGA3guVYLERQAsMYukzzbzd4jTNvZQvbFf6zO2ICtQavSsxVhciowHQi0K7vCzAGXB9MX%2F%2Fno4kvU2gYuiz2sE9q1CvAVCShTGlUKIIgNyHIbQpy%2FaCGKXc1rRHXwwyQxxKm1tDToSRu9hZW0AVHm3a%2BSEA3Ah1So5k78rfKu02%2FAZuRKNISTJwemUTJY0Z0kmhrGo0nhoeFIGCACxB1Vo9mOW8XPY3Kt5Hb5QU36QW30wtT0WckKSdhzJEUGxmgxkQUKyQiT1g93aPV9hwwGrLLlXiWhEa0ZxMafMm033jWvAzSzN5F0EATvmQaVfsacxliX0DonUr2%2FEqr4Qula062rABYTy9aBSLDp0rGGgb10Td9N56z%2B%2Bx00h9QP55sIe%2Fnnjx6ZH52dm5%2BZubYHEgatdONcYsTu%2BWbSfn6Dx%2F%2B9Rscjm6GIfQ2aB7omkQv36eU2NEZzSvCGMxLEu1rK7fEw1ryJ9iSLq1kc0umHtymznkBC2s8FzVtQ1ZJ9vBRXWWkoidDxgFNuU55w8B%2F9o4jF8xshCvjNqdi704wEzp5Q568iHX4Ib7TPbbzkKsI3JnhmL3MwSVONP4FsjD7JF8QAAA%3D')
#    s = f.read()
#    f.close()

    f = open("page.html", "r")
    html = f.read()
    f.close()

    roomNames = []
    p = re.compile(r'( - [a-zA-Z])')
    
    soup = BeautifulSoup.BeautifulSoup(html)
    tagList = soup.findAll("span")
    
    
    for tag in tagList:
        if len(tag.findChildren()) > 0:
            room = p.split(tag.findParent(name='tr').findAll('a')[3].text)[0]
            print "Found room with schedule: '" + room + "'"
            # Apparently the Fenix crew has a different numbering scheme for some rooms 
            if room[0] == '1' and (room[4] != '6' or (room[5] == '5' or room[5] == '3')):
                room = ' ' + room
            roomNames.append(room)

    return roomNames


if __name__ == '__main__':
    # Get all the room names with schedules
    roomNameList = get_room_names()
#    roomNameList = ["0 - 13",
#                    "0 - 15",
#                    "0 - 17"]
    output = ""
    
    # Run through the 'roomName' list
    for roomName in roomNameList:
        print "Grabbing '" + roomName + "'"
        table  = get_table_from_url("https://fenix.ist.utl.pt/publico/viewRoom.do?method=roomViewer&roomName=" + roomName +"&contentContextPath_PATH=/conteudos-publicos/pesquisa-de-espacos&")
        
        # Convert table into android array
        androidArray = convert_html_to_android(table)
        androidArray = roomName + "\n" + androidArray
        
        output += androidArray
    # Write to file
    file = open("conv-tables.txt", "w")
    file.write(output)
    file.close()
    
#    print output