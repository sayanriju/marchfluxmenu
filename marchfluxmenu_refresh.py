#!/usr/bin/env python
##Fluxbox Menu Generator

import os, fnmatch
from main import *

last_file = GetLatestFile('')
if fnmatch.fnmatch(last_file,'*.desktop'):
	item = ParseDesktopFile(last_file)
else:
	exit()

list = ParseMenuFile()

line_to_add = -1
item.CreateMenuLine().replace('\n','')

for var in list:
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
	



