#!/usr/bin/env python
##Fluxbox Menu Generator

'''' Generates the fluxbox menu '''

import os
from main import *

## Setting up seubmenus with Tango icons
m8 = SubMenuItem('Sound & Video','~/.marchfluxmenu/icons/applications-multimedia.png')
m7 = SubMenuItem('Programming','~/.marchfluxmenu/icons/applications-development.png')
m1 = SubMenuItem('Education','~/.marchfluxmenu/icons/applications-education.png')
m2 = SubMenuItem('Games','~/.marchfluxmenu/icons/applications-games.png')
m3 = SubMenuItem('Graphics','~/.marchfluxmenu/icons/applications-graphics.png')
m4 = SubMenuItem('Internet','~/.marchfluxmenu/icons/applications-internet.png')
m5 = SubMenuItem('Office','~/.marchfluxmenu/icons/applications-office.png')
m9 = SubMenuItem('System Tools','~/.marchfluxmenu/icons/applications-system.png')
m0 = SubMenuItem('Accessories','~/.marchfluxmenu/icons/applications-accessories.png')
m6 = SubMenuItem('Others','~/.marchfluxmenu/icons/applications-other.png')

menu_list = [m0,m1,m2,m3,m4,m5,m7,m8,m9,m6]


## Grouping ExecMenuItem instances obtained from each .desktop file according to the submenus to which they belong
desktop_file_list = SortDesktopFiles()
for filename in desktop_file_list:
	
	try:
		item = ParseDesktopFile(filename)
		
		for menu in menu_list:
			if menu.label == item.submenu:
				menu.AppendToMenu(item)
				break
	except:
		#print filename
		pass


## Initial part of menu (add ur fav programs here)
string = '[begin] (March Flux) \n'
string += ExecMenuItem('Web Browser', 'firefox', IconFind('firefox.png'), '').CreateMenuLine()
string += ExecMenuItem('Terminal', 'xterm', IconFind('term.png'), '').CreateMenuLine()
string +='''    [separator] (--------)
	[submenu] (Settings) {settings} <~/.marchfluxmenu/icons/preferences-$
		[exec] (Menu Editor) {~/.marchfluxmenu/fluxmenu/fluxMenu.py}
		[config] (Fluxbox Menu)
		[reconfig] (Reload config)
	[end]
	[separator] (--------)'''



## Submenu part with respective members being created
string += '[separator]\n'
for menu in menu_list:
	if menu.population != 0:
		string += menu.GenerateSubMenu() +'\n'
	

## Concluding part of menu
#string +='[separator]\n[submenu] (fluxbox menu)\
#		[config] (Configure)\n\
#		[submenu] (User Styles) {Choose a style...}\n\
#			[stylesdir] (~/.fluxbox/styles)\n\
#		[end]\n\
#		[workspaces] (Workspace List)\n\
#		[submenu] (Tools)\n\
#			[exec] (fluxconf) {fluxconf}\n\
#			[exec] (fluxkeys) {fluxkeys}\n\
#			[exec] (fluxmenu) {fluxmenu}\n\
#			[exec] (Window name) {xprop WM_CLASS|cut -d \" -f 2|xmessage -file - -center}\n\
#			[exec] (Screenshot - JPG) {import screenshot.jpg && display -resize 50% screenshot.jpg}\n\
#			[exec] (Screenshot - PNG) {import screenshot.png && display -resize 50% screenshot.png}\n\
#			[exec] (Regen Menu) {fluxbox-generate_menu}\n\
#		[end]\n\
#		[commanddialog] (Fluxbox Command)\n\
#		[reconfig] (Reload config)\n\
#		[restart] (Restart)\n\
#		[exec] (About) {(fluxbox -v; fluxbox -info | sed 1d) 2> /dev/null | xmessage -file - -center}\n\
#		[separator]\n'
string += '[end]\n'

	
## Write to menu file
filename = os.path.expanduser('~/.fluxbox/menu')
f = file(filename,'w')
f.write(string)

	

