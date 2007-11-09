#!/usr/bin/env python
## Filename : onremove.py

import os
import cPickle as pickle
from main import *

''' Executed when a  .desktop file is removed, generally on removal of a package '''

itemdata = 'itemlist.data'

f = file(itemdata)
item_list = pickle.load(f) 

init_string, end_string, dic = ParseFluxboxMenu('')

old_file_list = item_list[:]

new_file_list = ListExecItemsFromDesktop('')

for x in old_file_list:
	if x not in new_file_list:
		item = x						# Get the removed ExecMenuItem
		#print item.label
		break
	


#removed_file = getdiff(old_file_list, new_file_list)
#
#item = removed_file[0]				# Get the removed ExecMenuItem
			
item_list.remove(item)			# Update item_list for next iteration of daemon
f = file(itemdata, 'w')
pickle.dump(item_list, f)                # dump the object to a file
f.close()
			
	
	
init_string, end_string, dic = ParseFluxboxMenu('')
Sort = is_sorted(dic[item.submenu].members)
dic[item.submenu].RemoveFromSubMenu(item)

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