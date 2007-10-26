#!/usr/bin/env python
import os
import cPickle as pickle
from main import *

''' Run when a desktop file is deleted (on removal of a package) '''

itemdata = 'itemlist.data'
filedata = 'filelist.data'

f = file(filedata)
file_list = pickle.load(f) 
f.close()

f = file(itemdata)
item_list = pickle.load(f) 
f.close()


new_file_list = GetLatestFiles('')
for filename in file_list:
	if filename not in new_file_list:
		if fnmatch.fnmatch(filename,'*.desktop'):
			c = -1
			for var in item_list:
				c += 1
				if var[0] == filename:
					line_to_remove = var[1]
					item_list.pop(c)			# Update item_list for next iteration
					break					
			break
		
filename = os.path.expanduser('~/.fluxbox/menu')
f = file(filename,'r')

text = f.read()
lines = text.split('\n')
for i in range(0,len(lines)):
	if line_to_remove in lines[i]:
		lines.pop(i)
		break


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

