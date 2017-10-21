#!/usr/bin/python

# A script for creating the static HTML pages for the scales
# It checks a list of scale names to see if they have a corresponding Javascript file
# If they do a HTML page is created for them
# Then it creates Javascript files for the guidelines using org-mode encoded sources in the js/guidelines folder.
# It then offers to copy files to Android Studio Project assets folder
# created Dean Jenkins 8/Oct/2017

import os, shutil
from distutils.dir_util import copy_tree
import sys, cgi, re
import Orgnode

print "Making HTML files for the scales"

#### set up some variables ####
# path to Android Studio Project (modify as required)
path_to_android_app_folder = "/home/dean/AndroidStudioProjects/Eldercare/app/src/main/assets/"
# scales to be included
scales = ['wells','has-bled','cha2ds2-vasc','amt','frax','qfracture','abcd2','curb-65']
# guidelines to be included
guidelines = ['stroke']
# HTML template
scale_template = 'go-scales_template.html'
scalecounter = 0
scale_skipped = 0
guideline_template = 'go-guidelines_template.html'
guideline_template_js = 'go-guidelines_template.js'
guidelinecounter = 0
guideline_skipped = 0
js_swap_string = "XXXXXXXXXX.js"

#### do the scales ####
# read scale template
print "Using template '" + scale_template + "'"
f = open(scale_template)
template = f.read()
f.close()

# check scale template is OK
if template.find(js_swap_string) == -1:
    print "Fatal error: template swap string '" + js_swap_string + "' not found."
    sys.exit()

# create the scales files
for x in scales:
    msg = "   " + x + " "
    if os.path.isfile('js/scales/'+x+'.js'):
        scale = open("scale_" + x + ".html","w")
        scale.write(template.replace(js_swap_string,x + ".js",1))
        scale.close()
        msg = msg + "... done 'scale_" + x + ".html'"
        scalecounter = scalecounter + 1
    else:
        msg = msg + " ... scale skipped as no 'js/scales/"+x+".js'"
        scale_skipped = scale_skipped + 1
    print msg

# generate a report
report = "Finished. "

if scale_skipped == 0:
    report = report + ""
elif scale_skipped == 1:
    report = report + "1 scale skipped. "
else:
    report = report + str(scale_skipped) + " scales skipped. "

if scalecounter == 1:
    report = report + "1 scale created. "
else:
    report = report + str(scalecounter) + " scales done. "

print report

#### do the guidelines ####
# read guideline template HTML
print "Using template '" + guideline_template + "'"
f = open(guideline_template)
template = f.read()
f.close()

# check guideline template HTML is OK
if template.find(js_swap_string) == -1:
    print "Fatal error: template swap string '" + js_swap_string + "' not found."
    sys.exit()

# read guideline template JS
print "Using template '" + guideline_template_js + "'"
f = open(guideline_template_js)
template_js = f.read()
f.close()

# check guideline template JS is OK
if template_js.find(js_swap_string) == -1:
    print "Fatal error: template swap string '" + js_swap_string + "' not found."
    sys.exit()

def htmlentities(string):
    string = cgi.escape(string).encode('ascii', 'xmlcharrefreplace') # markup htmlentities
    string = re.sub(r'\[\[(.*?)\]\[(.*?)\]\]',r'<a href="\1">\2</a>',string) # find and code org-mod encoded hyperlinks
    return string

# create the guidelines files
for x in guidelines:
    msg = "   " + x + " "
    if os.path.isfile('js/guidelines/'+x+'.txt'):
        # get the guideline text file in org-mode format
        nodelist = Orgnode.makelist('js/guidelines/'+x+'.txt')
        guidelinehtml = ""
        for n in nodelist:
            # make HTML headings tags
            guidelinehtml += "<h" + str(n.Level()) + ">" # HTML Heading tag open
            guidelinehtml +=  htmlentities(n.Heading())
            guidelinehtml += "</h" + str(n.Level()) + ">\n" # HTML Heading tag close
            # if there is a body below a heading then make it in to HTML too
            bodylist = []
            # collect the list items
            for line in n.Body().split('\n'):
                if len(line) > 0:
                    bodylist.append(" <p>"+htmlentities(line)+"</p>\n")
            # only if there are list items make a HTML unordered list
            # (this forces ignoring of blank lines in the guideline file)
            if len(bodylist) > 0:
                #guidelinehtml += "<ul>" # not using lists at the moment (looks ugly)
                for item in bodylist:
                    guidelinehtml += item
                #guidelinehtml += "</ul>" # not using lists at the moment (looks ugly)
        # make guidelinehtml safe for javascript
        guidelinehtml = guidelinehtml.replace("'","\'")
        guidelinehtmllines = guidelinehtml.split("\n")
        # wrap the html into a Javascript document.write() lines
        jsinsert = ""
        for line in guidelinehtmllines:
            if line != "":
                jsinsert += "document.write('" + line + "');\n"
        # put the Javascript link into the HTML page
        guideline = open("guideline_" + x + ".html","w")
        guideline.write(template.replace(js_swap_string,"guideline_" + x + ".js",1))
        guideline.close()
        # create the Javascript source file
        guideline_js = open("js/guidelines/guideline_" + x + ".js","w")
        guideline_js.write(template_js.replace(js_swap_string,jsinsert,1))
        guideline_js.close()

        msg = msg + "... done 'guideline_" + x + ".html'"
        guidelinecounter = guidelinecounter + 1
    else:
        msg = msg + " ... guideline skipped as no 'js/guidelines/"+x+" .txt'"
        guideline_skipped = guideline_skipped + 1
    print msg

# generate a report
report = "Finished. "

if guideline_skipped == 0:
    report = report + ""
elif guideline_skipped == 1:
    report = report + "1 guideline skipped. "
else:
    report = report + str(guideline_skipped) + " guideline skipped. "

if guidelinecounter == 1:
    report = report + "1 guideline created. "
else:
    report = report + str(guidelinecounter) + " guidelines done. "

print report







# print reminder
print "remember to copy the files to the App(s)"

if os.path.isdir(path_to_android_app_folder):
    print "Android App folder path exists"    

    choice = raw_input("Copy to Android? y/n ") # python 2
    if choice == "y" or choice == "Y":
        print "You chose Yes!"
        print "Deleteing contents of " + path_to_android_app_folder
        for the_file in os.listdir(path_to_android_app_folder):
            file_path = os.path.join(path_to_android_app_folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        from_directory = os.curdir
        print "Copying from " + from_directory + " to " + path_to_android_app_folder
        copy_tree(from_directory, path_to_android_app_folder)
        # remove files that are not needed in the Android App assets folder
        shutil.rmtree(path_to_android_app_folder + ".git")
        os.unlink(path_to_android_app_folder + "go-scales.py")
        os.unlink(path_to_android_app_folder + "Orgnode.py")
        os.unlink(path_to_android_app_folder + "Orgnode.pyc")
        os.unlink(path_to_android_app_folder + scale_template)
        os.unlink(path_to_android_app_folder + guideline_template)
        os.unlink(path_to_android_app_folder + guideline_template_js)
    else:
        print "You chose No!"
else:
    if path_to_android_app_folder !="":
        print "Android App folder '" + path_to_android_app_folder + "' does not exist. Skipping."
    else:
        print "Android App folder not defined. Skipping."

raw_input("Hit ENTER to exit ") # python 2
