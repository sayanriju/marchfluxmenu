#!/usr/bin/env python
##Fluxbox Menu Generator

import os, fnmatch


def IconFind(icon_name):
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
				
			
	return ''		
	

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
		
#	def GenerateSubmenu(self):
#		self.body += '[end]'
#		return self.body
		
	def AppendToMenu(self, ExecMenuItem):
#		if '[end]' not in self.body:
#			self.body += CreateMenuLine(ExecMenuItem)
#		else:
	
		menuline = ExecMenuItem.CreateMenuLine()
		#self.body.replace('\t','')
		list = self.body.split('\n')
		### No Sorting of menu items!! Can be added easily if reqrd.

		
		end = list.pop()						## removing the '[end]'
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
	label = ''
	command = ''
	icon = ''
	submenu = ''
	
	#fff = os.path.join()
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
				#print label	
			list.append((label,ln-1))
	
	f.close()
	return list

def GetLatestFile(dirname):
	dirname = '/usr/share/applications/'
	
	list = []
	for files in os.listdir(dirname):
		a = ((os.path.getctime(os.path.join(dirname,files))),os.path.join(dirname,files))
		list.append(a)
		
	list.sort()
	return list[-1][1]