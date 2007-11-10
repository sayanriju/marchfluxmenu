# /usr/bin/env python
## Filename: mfm_generate.py

import os, fnmatch
import cPickle as pickle
from main import *

''' Generates the Fluxbox Menu '''

for file in os.listdir('/usr/share/applications/'):
	if fnmatch.fnmatch(file,'*.desktop'):
		try:
			item = ParseDesktopFile('/usr/share/applications/'+file)
			submenu_dict[item.submenu].AppendToSubMenu(item)
		except:
			#print file
			pass

del file

list = sortdic(submenu_dict)

string = '[begin] (March Flux) \n'
string += ExecMenuItem('Web Browser', 'firefox', IconFind('firefox.png'), '').GenerateMenuLine()
string += ExecMenuItem('Terminal', 'xterm', IconFind('term.png'), '').GenerateMenuLine()
string +='''    [separator] (--------)
 [submenu] (Settings) {settings} <~/.marchfluxmenu/icons/preferences-system.png>
		[config] (Fluxbox Menu)
		[reconfig] (Reload Config)
		[restart] (Restart Fluxbox)
		[workspaces] (Workspaces)
 [end]
[separator] (tag start)	'''
string += '\n'
	
for m in list:
	if m.population != 0:
		m.GenerateSubMenu(Sort = True)
		string += m.body
		string += '\n'

string += '[separator] (tag end)\n' + '[exit] (Exit) <~/.marchfluxmenu/icons/exit.png>\n'+ '[end]\n'

#print string
filename = os.path.expanduser('~/.fluxbox/menu')
f = file(filename,'w')
f.write(string)
f.close()

''' Initiation! Records the currently exisitng ExecMenuItems present from the .desktop files '''

itemdata = 'itemlist.data'

item_list = ListExecItemsFromDesktop('')


f = file(itemdata, 'w')
pickle.dump(item_list, f)                # dump the object to a file
f.close()

del item_list


