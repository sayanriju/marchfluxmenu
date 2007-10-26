#!/usr/bin/env python
# File name: pickling.py

import os
from main import *
import cPickle as pickle
# OR import pickle

filedata = 'filelist.data'      # the files where we will persistently store the object
itemdata = 'itemlist.data'

file_list = GetLatestFiles('')
item_list = ListExecItemsFromDesktop(file_list)



# Write to the file
f = file(filedata, 'w')
pickle.dump(file_list, f)                # dump the object to a file
f.close()

f = file(itemdata, 'w')
pickle.dump(item_list, f)                # dump the object to a file
f.close()

del item_list,file_list

