#
# walk the enron tree and put it into the db
# 
import os, sys
import email

from itest.models.tinydb.contact import Contact
from itest.models.tinydb.email import Email

import dateutil #pip install python-dateutil


base=os.path.normpath("C:\khz\devel\enron\maildir")
d=base
#peoples_dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
peoples_dirs = [o for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
#print(peoples_dirs)

for d in peoples_dirs:
    depth = 0   
    d= os.path.join(base,d)
    absd=os.path.join(d, "inbox")  # take inbox only
    print(50*"-")
    for directory, dirnames, filenames in os.walk(absd):        
        print(str(d) + " Folders: " + str(dirnames))
        #print(directory)
        print("  emails : " + str(len(filenames)))
        depth += 1
        #print("  filenames : " + str(filenames[0:5]))
        for f in filenames:
            mailfile = open(os.path.join(directory, f), "r")
            msg = email.message_from_file(mailfile)
            em = Email()
            em.setup_from_msg(msg)
            print(em)
            c = Contact()
            c.email_address = em._from
            print(c)
        if depth >0:    # folder scan depth (0 == only one, inbox only)
            break
