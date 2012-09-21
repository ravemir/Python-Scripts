'''
Created on 21 de Set de 2012

@author: ravemir
'''

import urllib

def get_table_from_url(url):
    
    # Open the url, read the contents into a string, and close the file
    f = urllib.urlopen(url)
    s = f.read()
    f.close()
    
    # Get the 'timetable' element
    sched = s
    
    return sched

if __name__ == '__main__':
    pass