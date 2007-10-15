#!/usr/bin/env python
##Fluxbox Menu Generator

import os, fnmatch
from main import *


m8 = SubMenuItem('Sound & Video','/home/sayan/marchfluxmenu/icons/applications-multimedia.png')
m7 = SubMenuItem('Programming','/home/sayan/marchfluxmenu/icons/applications-development.png')
m1 = SubMenuItem('Education','')
m2 = SubMenuItem('Games','/home/sayan/marchfluxmenu/icons/applications-games.png')
m3 = SubMenuItem('Graphics','/home/sayan/marchfluxmenu/icons/applications-graphics.png')
m4 = SubMenuItem('Internet','/home/sayan/marchfluxmenu/icons/applications-internet.png')
m5 = SubMenuItem('Office','/home/sayan/marchfluxmenu/icons/applications-office.png')
m9 = SubMenuItem('System Tools','/home/sayan/marchfluxmenu/icons/applications-system.png')
m0 = SubMenuItem('Accessories','/home/sayan/marchfluxmenu/icons/applications-accessories.png')
m6 = SubMenuItem('Others','/home/sayan/marchfluxmenu/icons/applications-other.png')

menu_list = [m0,m1,m2,m3,m4,m5,m7,m8,m9,m6]

#for root, dirs, files in os.walk('/usr/share/'):
#	for name in files:
#		if fnmatch.fnmatch(name,'*.desktop'):
for filename in os.listdir('/usr/share/applications/'):
	if fnmatch.fnmatch(filename,'*.desktop'):
	#filename = os.path.join(root, name)
		try:
			item = ParseDesktopFile('/usr/share/applications/'+filename)
			
			for menu in menu_list:
				if menu.label == item.submenu:
					menu.AppendToMenu(item)
					break
		except:
			print filename
			pass


##########################################

string = '[begin] (March Flux) \n'
for menu in menu_list:
	if menu.population != 0:
		string += menu.GenerateSubMenu() +'\n'
	
string += '[end]'
f = file('/home/sayan/.fluxbox/menu','w')
f.write(string)

	

