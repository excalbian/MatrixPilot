'''
Use mavgen.py matrixpilot.xml definitions to generate
C and Python MAVLink routines for sending and parsing the protocol
This python script is soley for MatrixPilot MAVLink implementations

Copyright Pete Hollands 2011, 2012, 2014
Released under GNU GPL version 3 or later
'''

import os, sys, glob, re
from shutil import copy
from pymavlink.generator.mavgen import mavgen 

# allow import from the parent directory, where mavutil.py is
# Under Windows, this script must be run from a DOS command window 
# sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
sys.path.insert(0, os.path.join(os.getcwd(), '..'))

class options:
    """ a class to simulate the options of mavgen OptionsParser"""
    def __init__(self, lang, output, wire_protocol, error_limit,validate):
        self.language = lang
        self.wire_protocol = wire_protocol
        self.output = output
        self.error_limit = error_limit
        self.validate = validate

def remove_include_files(target_directory):
    search_pattern = target_directory+'/*.h'
    print "search pattern is", search_pattern
    files_to_remove = glob.glob(search_pattern)
    for afile in files_to_remove :
        try:
            print "removing", afile
            os.remove(afile)
        except:
            print "error while trying to remove", afile

def copy_include_files(source_directory,target_directory):
    search_pattern = source_directory+'/*.h'
    files_to_copy = glob.glob(search_pattern)
    for afile in files_to_copy:
        basename = os.path.basename(afile)
        print "Copying ...", basename
        copy(afile, target_directory)

def remove_xml_files(target_directory):
    search_pattern = target_directory+'/*.xml'
    print "search pattern is", search_pattern
    files_to_remove = glob.glob(search_pattern)
    for afile in files_to_remove :
        try:
            print "removing", afile
            os.remove(afile)
        except:
            print "error while trying to remove", afile

def copy_xml_files(source_directory,target_directory):
    search_pattern = source_directory+'/*.xml'
    files_to_copy = glob.glob(search_pattern)
    for afile in files_to_copy:
        basename = os.path.basename(afile)
        print "Copying ...", basename
        copy(afile, target_directory)


########### Generate MAVlink files for C and Python from XML definitions
protocol = "1.0" #
xml_directory = '../../message_definitions/v'+protocol

xml_file_name = "matrixpilot.xml"

print "This script is intended to be used by MatrixPilot developers."
print "Use it if if you have altered matrixpilot.xml and would like to regenerate mavlink messages."
print "It will generate both the C header files and the Python the python parser."
print ""

#Check to see if python directory exists ...
print "xml file to use for generation is", xml_file_name     
xml_file_base = re.sub("\.xml","", xml_file_name)
target_directory = "../../../../../MAVLink/include"
source_xml_file = xml_directory+"/"+xml_file_name

print "About to remove all old generated files in",target_directory
print "OK to continue ?[Yes / No]: ",
line = sys.stdin.readline()
if line == "Yes\n" or line == "yes\n" \
   or line == "Y\n" or line == "y\n":
    print "Proceeding"
    remove_include_files(target_directory+'/common')
    remove_include_files(target_directory+'/matrixpilot')
    print "Finished removing C include files for", xml_file_base
else :
    print "Your answer is No. Exiting Program"
    sys.exit()
    

opts = options(lang = "C", output=target_directory, \
               wire_protocol=protocol, error_limit=200, validate=True)
args = []
args.append(source_xml_file)
print "About to generate C include files"
mavgen(opts, args)


opts = options(lang = "python", \
               output="../dialects/"+"v10/"+xml_file_base+".py", \
               wire_protocol=protocol, error_limit=200,validate=True)
print "About to generate python parsers and save them into ../dialects/v10/ directory"
mavgen(opts,args)

print "All C headers and Python parsers now generated"       
        
##### End of Main program to generate MAVLink C and Python files ####

##### Copy new XML message definitions to main trunk directories
source_directory = "../../message_definitions/V1.0"
target_directory = "../../../../../MAVLink/message_definitions"
if os.access(source_directory, os.R_OK):
    if os.access(target_directory, os.W_OK):
        print "Preparing to copy over xml message definitoin files to MatrixPilot main codebase..."
        print "About to remove files in ",target_directory
        print "OK to continue ?[Yes / No]: ",
        line = sys.stdin.readline()
        if line == "Yes\n" or line == "yes\n" \
           or line == "Y\n" or line == "y\n":
            print "passed"
            try:
                print "removing xml files in", target_directory
                remove_xml_files(target_directory)
            except:
                print "error while trying to remove files in ", target_directory
            print "Copying xml files from ", source_directory
            copy_xml_files(source_directory, target_directory) 
            print "Finished copying over xml files"
        else :
            print "Your answer is No. Exiting Program"
            sys.exit()
    else :
       print "Cannot find " + target_directory 
       sys.exit() 
else:
    print "Could not find files to copy at", source_directory
    print "Exiting Program."
    sys.exit()
print "MatrixPiklot MAVLink generation script has finished"


