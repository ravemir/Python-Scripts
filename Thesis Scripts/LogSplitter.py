'''
Created on Oct 8, 2012

@author: ravemir
'''

import os
from dircache import listdir
from string import replace
#from reportlab.lib.validators import matchesPattern

#folder = '/media/storage/Tese/logs/'
#folder = '/home/ravemir/logs/29-10-2012/'
folder = 'C:\\Users\\Carlos\\Dropbox\\Tese\\Dissertacao\\Dados\\29-10-2012\\'

# Open each log
for filename in os.listdir(folder):
    if filename.endswith('.log'):
        print "Opening '" + filename + "'..."
        log = open(folder + filename, 'r')
    
        # Create the folder to contain the new files
        convPath = folder + 'conv/'
        try:
            os.stat(convPath)
        except:
            os.mkdir(convPath)
            
        # Create corresponding 'accel' and 'loc' files 
        accel = open(convPath + filename + ".accel", 'w')
        loc = open(convPath + filename + ".loc", 'w')
        
        # Read each line
        for line in log.readlines(): # FIXME: loading all lines at once spends alot of memory
            # If the first character is 'A'
            if line[0] == 'A':
                # Write the rest of the line to the 'accel' filename
                line = replace(line, 'A, ', '')
                accel.write(line)
            # If the first character is 'L'
            if line[0] == 'L':
                # Write the rest of the line to the 'loc' filename
                line = replace(line, 'L, ', '')
                loc.write(line)
    
        # Close the files
        accel.close()
        loc.close()
        log.close()
print "Done!"