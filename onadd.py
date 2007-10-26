#!/usr/bin/env python
import os
import cPickle as pickle
from main import *

''' Run when a new desktop file is added (on installtion of a new package) '''

itemdata = 'itemlist.data'
filedata = 'filelist.data'

f = file(itemdata)
item_list = pickle.load(f) 
f.close()

new_file_list = GetLatestFiles('')
for filename in new_file_list:
	if fnmatch.fnmatch(filename,'*.desktop'):
		item = ParseDesktopFile(filename)
		a = ((filename, item.label))
		item_list.append(a)				# Update item_list for next iteration of daemon

		break
	else:
		continue

menu_list = ParseMenuFile()

item.CreateMenuLine().replace('\n','')

for var in menu_list:
	if item.submenu == var[0]:
		line_to_add = var[1] + 1
		break

filename = os.path.expanduser('~/.fluxbox/menu')
f = file(filename,'r')

text = f.read()
lines = text.split('\n')
lines.insert(line_to_add + 1, '   \t' + item.CreateMenuLine())
f.close()

f = file(filename,'w')
text = ''
for l in lines:
	text += l + '\n'
f.write(text)
f.close()

# Getting ready for next iteration of daemon loop
f = file(filedata, 'w')
pickle.dump(new_file_list, f)                # dump the object to a file
f.close()

f = file(itemdata, 'w')
pickle.dump(item_list, f)                # dump the object to a file
f.close()


