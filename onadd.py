# /usr/bin/env python
## Filename : onadd.py

import os
from main import *
import cPickle as pickle

''' Executed when a .desktop file is added, generally on installtion of a new package '''

itemdata = 'itemlist.data'

new_file_list = GetLatestFiles('')
for filename in new_file_list:
	if fnmatch.fnmatch(filename,'*.desktop'):
		try:
			item = ParseDesktopFile(filename)	# Parse the newest .desktop file
			break
		except:
			pass
	else:
		continue

init_string, end_string, dic = ParseFluxboxMenu('')
Sort = is_sorted(dic[item.submenu].members)
dic[item.submenu].AppendToSubMenu(item)

list = sortdic(dic)

string = init_string
for m in list :
	if m.label not in submenu_dict.keys():
		#continue
		pass
	if m.population != 0:
		if m.label == item.submenu:
			m.GenerateSubMenu(Sort = Sort)
		else:
			m.GenerateSubMenu(Sort = is_sorted(m.members))
		string += m.body
		string += '\n'


string += end_string

filename = os.path.expanduser('~/.fluxbox/menu')
f = file(filename,'w')
f.write(string)
f.close()

## Updating item list for next iteration of daemon

item_list = ListExecItemsFromDesktop('')

f = file(itemdata, 'w')
pickle.dump(item_list, f)                # dump the object to a file
f.close()

#print len(item_list)


