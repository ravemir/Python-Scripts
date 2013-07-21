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
            fileNames = [convPath + filename + ".accel",
                         convPath + filename + ".info",
                         convPath + filename + ".loc",
                         convPath + filename + ".mag",
                         convPath + filename + ".ori",
                         convPath + filename + ".step",
                         convPath + filename + ".world",
                         convPath + filename + ".pos"]; 
            accel = open(fileNames[0], 'w')
            info = open(fileNames[1], 'w')
            loc = open(fileNames[2], 'w')
            mag = open(fileNames[3], 'w')
            ori = open(fileNames[4], 'w')
            steps = open(fileNames[5], 'w')
            world = open(fileNames[6], 'w')
            pos = open(fileNames[7], 'w')
            
            # Declare log entry tags
            logTags = ['A,','I,','L,','M,','O,','S,','W,', 'P,'];
            
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
                elif line.startswith(logTags[6]):
                    # Write the rest of the line to the 'steps' filename
                    line = replace(line, logTags[6], '')
                    world.write(line)
                elif line.startswith(logTags[7]):
                    # Write the rest of the line to the 'steps' filename
                    line = replace(line, logTags[7], '')
                    pos.write(line)
        
            # Close the files
            log.close()
            accel.close()
            info.close()
            loc.close()
            mag.close()
            ori.close()
            world.close()
            steps.close()
            pos.close()
            
            # Clear all the empty files (smaller than 1KB)
            for f in fileNames:
                if os.path.getsize(f) < 1 * 1024:
                    os.remove(f)
                    print "...removed " + f
            
            print "Done!"

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv)
    else:
        main()
    print 'Finished!'