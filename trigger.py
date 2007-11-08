#!/usr/bin/env python
# File name: trigger.py

import os
from main import *
import cPickle as pickle

''' Executed at every booting of fluxbox. It creates the data file(s) keeping track of the ExecMenuItems
in the current menu '''

itemdata = 'itemlist.data'

item_list = ListExecItemsFromDesktop('')

f = file(itemdata, 'w')
pickle.dump(item_list, f)                # dump the object to a file
f.close()

del item_list
