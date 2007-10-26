#!/usr/bin/env python
##Fluxbox Menu Generator

''' This is the main file where various classes and functions are defined'''

import os, fnmatch


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
				
			
	return '~/.marchfluxmenu/icons/application-default-icon.png'		
	

class ExecMenuItem:
	def __init__(self, label, command, icon, submenu):
		self.label = label
		self.command = command
		self.icon = icon
		self.submenu = submenu
		
	def CreateMenuLine(self):
		label = '(' + self.label + ')'
		command = '{' + self.command + '}'
		if '/' not in self.icon:
			self.icon = IconFind(self.icon)
		icon = '<' + self.icon + '>'
		
		
		return '[exec]' + '  ' + label + '  ' +  command + '  ' + icon +'\n'
	
	
class SubMenuItem:
	def __init__(self, label, icon, body='', members=[], population=0):
		self.label = label
		self.icon = icon
		self.population = population
		self.members = members
		self.body = '  [submenu]' + '  ' + '('+label+')' + '  ' +'<'+ icon + '>' +'\n' + '  [end]'
		
		
	def AppendToMenu(self, ExecMenuItem):
#		if '[end]' not in self.body:
#			self.body += CreateMenuLine(ExecMenuItem)
#		else:
	
		menuline = ExecMenuItem.CreateMenuLine()
		list = self.body.split('\n')
		### No Sorting of menu items!! Can be added easily if reqrd.
		#list.sort()
		
		end = list.pop()	## removing the '[end]'
		list.append('\t\t' + menuline)			## Adding the new Exec item
		
		self.body = list[0] 					## rebuilding body
		for item in list[1:]:
			if item != '':
				self.body +=  '\n' + item 
		self.body +=  end
		
		self.population += 1
		self.members.append(ExecMenuItem)
		
		return self
		
	def GenerateSubMenu(self):
		return self.body




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
				categories = text[1].split(';')
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
	

def ParseMenuFile():	
	'''' Parses the fluxbox menu file and returns a list of tuples, 	each 2-tuple
	containing the submenu name & line number where the submenu name appears in the menu file '''
	
	filename = os.path.expanduser('~/.fluxbox/menu')
	f = file(filename,'r')
	
	ln =0
	list = []
	for line in f.readlines():
		ln += 1
		if '[submenu]' in line:
			label = ''
			for i in range(line.find('(')+1,line.find(')')):
				label += line[i]
			list.append((label,ln-1))
	
	f.close()
	return list

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
	''' Returns a list if 2-tuples, each containing the *.desktop filepath &
	the label of the ExecMenuItem instance that the file describes
	To be used for removing extinct items from menu'''
	
	
	list = []
	#filelist = GetLatestFiles('')
	for filename in filelist:
		if fnmatch.fnmatch(filename,'*.desktop'):
			item = ParseDesktopFile(filename)
			try:
				a = ((filename, item.label))
				list.append(a)
			except:
				pass
	return list

def ListExecItemsFromMenu(menufile):
	''' returns a list of labels of the ExecMenuItem elements defined in the menufile 
	(not required right now)'''
	
	menufile = os.path.expanduser('~/.fluxbox/menu')
	
	f = file(menufile,'r')
	
	list = []
	text = f.read()
	lines = text.split('\n')
	
	for l in lines:
		if '[exec]' in l:
			a = l.partition('(')[2].partition(')')[0]
			list.append(a)
	
	return list	