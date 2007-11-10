# /usr/bin/env python
## Filename : main.py

import os, fnmatch

''' The main file of MarchFluxMenu. All the functions and variables are defined over here. '''

def is_sorted(list):
	''' Checks if the list passed on as argument is sorted or not '''
	
	old = list[:]
	new = list[:]
	new.sort()
	if old == new:
		return True		## If list is sorted
	else:
		return False		## If list is NOT sorted
	
def sortdic(adict):
	''' Takes a dictionary and returns a SORTED list of items (not keys) '''
	
	items = adict.items()
	items.sort()
	return [value for key, value in items]
	
def IconFind(icon_name):
	''' Implements the icon finding algorithm. Tries to match label name with names of 
	icon files in the directory /usr/share/pixmaps'''
	
	for root, dirs, files in os.walk('/usr/share/pixmaps'):
		for name in files:
			if icon_name == name:
				return os.path.join(root, name)
			elif icon_name.partition('.')[0] in name:
				return os.path.join(root, name)
#			else:
#				for root, dirs, files in os.walk('/usr/share/icons'):
#					for name in files:
#						if icon_name == name:
#							return os.path.join(root, name)
#						elif icon_name.partition('.')[0] in name:
#							return os.path.join(root, name)
				
	## Default icon for apps with no icons!	
	return '~/.marchfluxmenu/icons/application-default-icon.png'	

class ExecMenuItem:
	def __init__(self, label, command, icon, submenu):
		self.label = label
		self.command = command
		self.icon = icon
		self.submenu = submenu
		
	def __cmp__(self, other):
		return cmp(self.label.upper(), other.label.upper())
		
	def GenerateMenuLine(self):
		label = '(' + self.label + ')'
		command = '{' + self.command + '}'
		if '/' not in self.icon:
			self.icon = IconFind(self.icon)
		icon = '<' + self.icon + '>'
		
		
		return '\t[exec]' + '  ' + label + '  ' +  command + '  ' + icon +'\n'

class SubMenuItem:
	def __init__(self, label, icon, members):
		self.label = label
		self.icon = icon
		self.members = members
		
		
		self.population = len(self.members)
		self.body = ''
		
		#self.GenerateSubMenu()
		
	def AppendToSubMenu(self,item):
		self.members.append(item)
		self.population += 1
		
	def GenerateSubMenu(self, Sort):
		
		if Sort:
			self.members.sort()
		text = '   [submenu]' + '  ' + '('+ self.label + ')' + '  ' +'<'+ self.icon + '>' +'\n'
		
		for item in self.members:
			text += item.GenerateMenuLine()
			
		text += '   [end]'
		self.body = text[:]
		del text
		
		return self.body
	
	def WriteMenuFile(self):
		path = ''
		f = file(path + self.label + '.menu','w')
		f.write(self.body)
		f.close()
		
	def RemoveFromSubMenu(self,item):
		self.members.remove(item)
		#self.members.pop(ind)
		#self.members.remove(item)
		self.population = self.population - 1
		
		#return self.members
		

#############################
## Variables Defined :
#############################

m8 = SubMenuItem('Sound & Video','~/.marchfluxmenu/icons/applications-multimedia.png',[])
m7 = SubMenuItem('Programming','~/.marchfluxmenu/icons/applications-development.png',[])
m1 = SubMenuItem('Education','~/.marchfluxmenu/icons/applications-education.png',[])
m2 = SubMenuItem('Games','~/.marchfluxmenu/icons/applications-games.png',[])
m3 = SubMenuItem('Graphics','~/.marchfluxmenu/icons/applications-graphics.png',[])
m4 = SubMenuItem('Internet','~/.marchfluxmenu/icons/applications-internet.png',[])
m5 = SubMenuItem('Office','~/.marchfluxmenu/icons/applications-office.png',[])
m9 = SubMenuItem('System Tools','~/.marchfluxmenu/icons/applications-system.png',[])
m0 = SubMenuItem('Accessories','~/.marchfluxmenu/icons/applications-accessories.png',[])
m6 = SubMenuItem('Others','~/.marchfluxmenu/icons/applications-other.png',[])

#submenu_list = [m0,m1,m2,m3,m4,m5,m7,m8,m9,m6]

	
submenu_dict = { 
'Sound & Video': m8,
'Programming':m7, 
'Education':m1, 
'Games':m2,
'Graphics':m3,
'Internet':m4,
'Office':m5,
'System Tools':m9,
'Accessories':m0,
'Others':m6
}


#############################
## Functions Defined :
#############################

def ParseDesktopFile(filename):
	''' Parses a .desktop file and returns an ExecMenuItem instance'''
	
	label = ''
	command = ''
	icon = ''
	submenu = ''
	
	f = file(filename)
	
	for line in f.readlines():
		if line[0] != '#':
			text = line.split('=')
			
			if text[0] == 'Name' :
				label = text[1].replace ( "\n", "" )
			elif text[0] == 'Exec':
				command  = text[1].replace ( "\n", "" )
			elif text[0] == 'Icon':
				icon = text[1].replace ( "\n", "" )
			elif text[0] == 'Categories':
				if ';' in text[1]:
					categories = text[1].split(';')
				else:
					categories = text[1]
				if 'AudioVideo'  in categories:
					submenu = 'Sound & Video'
				elif 'Development' in categories:
					submenu = 'Programming'
				elif 'Education' in categories:
					submenu = 'Education'
				elif 'Game' in categories:
					submenu = 'Games'
				elif 'Graphics' in categories:
					submenu = 'Graphics'
				elif 'Network' in categories:
					submenu = 'Internet'
				elif 'Office' in categories:
					submenu = 'Office'
				elif 'System' in categories:
					submenu = 'System Tools'
				elif 'Utility' in categories:
					submenu = 'Accessories'
				else:
					submenu = 'Others'
	
	if label != ''and submenu != '':
		return ExecMenuItem(label, command, icon, submenu)
	else:
		pass
	
	
	f.close()
	

def ParseFluxboxMenu(menufile):
	''' Parses the ~/.fluxbox/menu file, and returns a 3-tuple whose elements are respectively :
		(1) The initial text, i.e the part of fluxbox menu preceeding the submenu block
		(2) The concluding text, i.e. the part of fluxbox menu following the submenu block
		(3) A dictionary  of included SubMenuItem instances, with the submenu labels (as defined
																		in submenu_dict) as the keys '''
	
	menufile = os.path.expanduser('~/.fluxbox/menu')
	submenus_in_menu = []
	lines =[]
	f = file(menufile) 
	text = f.read()
	
	init_text = text.partition('[separator] (tag start)')[0] + '[separator] (tag start)\n'
	#print init_text
	end_text = '[separator] (tag end)' + text.rpartition('[separator] (tag end)')[2] 
	#print end_text
	ll= text.split('\n')
	for l in ll:
		lines.append(l.replace('\r',''))
	
	try:
		start = lines.index('[separator] (tag start)')
		end = lines.index('[separator] (tag end)')
	except:
		start, end = 0, len(lines)

	#print start, end
	for ln in range(start,end):
					
		if '[submenu]' in lines[ln]:
			menu_label = lines[ln].partition('(')[2].partition(')')[0]
			menu_icon = lines[ln].partition('<')[2].partition('>')[0]
			submenu = SubMenuItem(menu_label, menu_icon, [])
			ln += 1
			while True:
				if '[end]' in lines[ln] :
					submenus_in_menu.append(submenu)
					ln += 1
					break
				else:
					item_label = lines[ln].partition('(')[2].partition(')')[0]
					item_command = lines[ln].partition('{')[2].partition('}')[0]
					item_icon = lines[ln].partition('<')[2].partition('>')[0]
					item_submenu = menu_label		
					submenu.AppendToSubMenu(ExecMenuItem(item_label, item_command, item_icon, item_submenu))
					ln += 1
					
		else:
			pass
		
	dict = submenu_dict
	
	for m in submenus_in_menu:
		dict[m.label] = m
		
	return init_text, end_text, dict

def GetLatestFiles(dirname):
	''' returns a list of files (with filepath) sorted according to newest first'''
	
	dirname = '/usr/share/applications/'
	
	list = []
	for files in os.listdir(dirname):
		a = ((os.path.getctime(os.path.join(dirname,files))),os.path.join(dirname,files))
		list.append(a)
		
	list.sort()
	list.reverse()
	
	filelist = []
	for var in list:
		filelist.append(var[1])
		
	return filelist

def ListExecItemsFromDesktop(filelist):
	''' Returns a list of all the ExecMenuItem-s parsed from the currently existing .desktop files '''	
	
	l = []
	filelist = GetLatestFiles('')
	for filename in filelist:
		if fnmatch.fnmatch(filename,'*.desktop'):			
			item = ParseDesktopFile(filename)
			try:
				a = item.label
				l.append(item)
				
			except:
				#print filename
				pass
		
		#list.sort(lambda x,y:cmp(x[1].upper(),y[1].upper()))
	return l
##

