#!/usr/bin/env python
##Fluxbox Menu Generator

''' Functions as sort of a daemon which watches /usr/share/applications for addition/removal of .desktop
files (traditionally during install/remove of pacakges) and updates the fluxbox menu accordingly.'''

import os, fnmatch
from main import *


def countfile(pathname):
	pathname = '/usr/share/applications/'
	i = 0
	for var in os.listdir(pathname):
		i += 1	
	return i


file_list = GetLatestFiles('')					## Chronological list of .desktop files
start_count = countfile('')
item_list = ListExecItemsFromDesktop(file_list)			## Logs all the ExecMenuItem entries in current menu

print item_list
while True:							## Daemon infinite loop starts
	count = countfile('')

#	if start_count < count:			# File has been added
#		new_file_list = GetLatestFiles('')
#		for filename in new_file_list:
#			if fnmatch.fnmatch(filename,'*.desktop'):
#				item = ParseDesktopFile(filename)
#				a = ((filename, item.label))
#				item_list.append(a)				# Update item_list for next iteration
#
#				break
#			else:
#				continue
#
#		menu_list = ParseMenuFile()
#
#		item.CreateMenuLine().replace('\n','')
#
#		for var in menu_list:
#			if item.submenu == var[0]:
#				line_to_add = var[1] + 1
#				break
#		
#		filename = os.path.expanduser('~/.fluxbox/menu')
#		f = file(filename,'r')
#
#		text = f.read()
#		lines = text.split('\n')
#		lines.insert(line_to_add + 1, '   \t' + item.CreateMenuLine())
#		f.close()
#		
#		f = file(filename,'w')
#		text = ''
#		for l in lines:
#			text += l + '\n'
#		f.write(text)
#		f.close()
#		
#		# Getting ready for next iteration of daemon loop
#		file_list = new_file_list
#		start_count = count
#		
#		
#	elif start_count > count: 			# File has been removed
#		
#		new_file_list = GetLatestFiles('')
#		for filename in file_list:
#			if filename not in new_file_list:
#				if fnmatch.fnmatch(filename,'*.desktop'):
#					c = -1
#					for var in item_list:
#						c += 1
#						if var[0] == filename:
#							line_to_remove = var[1]
#							item_list.pop(c)			# Update item_list for next iteration
#							break					
#					break
#				
#		filename = os.path.expanduser('~/.fluxbox/menu')
#		f = file(filename,'r')
#
#		text = f.read()
#		lines = text.split('\n')
#		for i in range(0,len(lines)):
#			if line_to_remove in lines[i]:
#				lines.pop(i)
#				break
#		
#		
#		f = file(filename,'w')
#		text = ''
#		for l in lines:
#			text += l + '\n'
#		f.write(text)
#		f.close()
#
#		# Getting ready for next iteration of daemon loop
#		start_count = count
#		file_list = new_file_list
#
#
#
#					
#					
#	else:							# No change
#		continue
	continue