'''
Created on Oct 8, 2012

@author: ravemir
'''

import os
from string import replace
import sys
#from reportlab.lib.validators import matchesPattern

#defaultFolder = '/media/storage/Tese/logs/'
#defaultFolder = '/home/ravemir/logs/29-10-2012/'
defaultFolder = 'C:\\Users\\Carlos\\Dropbox\\Tese\\Dissertacao\\Dados\\'

def main(arg1 = defaultFolder):
    # Open each log
    for filename in os.listdir(arg1):
        fullPath = arg1 + filename
        if os.path.isdir(fullPath):
            main(fullPath + os.sep)
        elif filename.endswith('.log') and os.path.isfile(fullPath):
            print "Opening '" + filename + "'..."
            log = open(arg1 + filename, 'r')
        
            # Create the defaultFolder to contain the new files
            convPath = arg1 + 'conv/'
            try:
                os.stat(convPath)
            except:
                os.mkdir(convPath)
                
            # Create corresponding 'accel' and 'loc' files 
            accel = open(convPath + filename + ".accel", 'w')
            info = open(convPath + filename + ".info", 'w')
            loc = open(convPath + filename + ".loc", 'w')
            mag = open(convPath + filename + ".mag", 'w')
            ori = open(convPath + filename + ".ori", 'w')
            steps = open(convPath + filename + ".step", 'w')
            
            # Declare log entry tags
            logTags = ['A,','I,','L,','M,','O,','S,'];
            
            # Read each line
            for line in log.readlines(): # FIXME: loading all lines at once spends alot of memory
                # Match the beginning of the line with the declared tags
                if line.startswith(logTags[0]):
                    # Write the rest of the line to the 'accel' filename
                    line = replace(line, logTags[0], '')
                    accel.write(line)
                # If the first character is 'I'
                elif line.startswith(logTags[1]):
                    # Write the rest of the line to the 'info' filename
                    line = replace(line, logTags[1], '')
                    info.write(line)
                elif line.startswith(logTags[2]):
                    # Write the rest of the line to the 'loc' filename
                    line = replace(line, logTags[2], '')
                    loc.write(line)
                elif line.startswith(logTags[3]):
                    # Write the rest of the line to the 'mag' filename
                    line = replace(line, logTags[3], '')
                    mag.write(line)
                elif line.startswith(logTags[4]):
                    # Write the rest of the line to the 'ori' filename
                    line = replace(line, logTags[4], '')
                    ori.write(line)
                elif line.startswith(logTags[5]):
                    # Write the rest of the line to the 'steps' filename
                    line = replace(line, logTags[5], '')
                    steps.write(line)
        
            # Close the files
            log.close()
            accel.close()
            info.close()
            loc.close()
            mag.close()
            ori.close()
            print "Done!"

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv)
    else:
        main()
    print 'Finished!'