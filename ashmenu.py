import pygame, os

########################################################################
# E X C E P T I O N S 
########################################################################
class eNoFont(Exception):
	def __str__(self):
		return "Set font before adding items"

class eNoSurface(Exception):
	def __str__(self):
		return "Set surface before rendering"

class eMenuEmpty(Exception):
	def __str__(self):
		return "Nothing to render"

class eUnknownItemType(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return "Unknown menu item type (%s)" % repr(self.value)



########################################################################
# M E N U   I T E M S
########################################################################
class menuItem(object):
	def __init__(self, name):
		self.name = name

class menuSlider(menuItem):
	def __init__(self, name, min, max, current=0):
		self.name = name
		self.min = min
		self.max = max
		self.current = current
		self.step = 1
		self.width = 100
		self.height = 16
	
	def __setattr__(self, name, value):
		if name == "current":
			if value < self.min: value = self.min
			elif value > self.max: value = self.max
			
		self.__dict__[name] = value
			
			

########################################################################
# M E N U
########################################################################
class ashMenu(object):
	""" Creates a nice menu object """
	
	####################################################################
	# I N I T
	####################################################################
	def __init__(self):
		""" Initialise """
		self.menuItems = []
		self.font = None
		self.fontColor = (128,128,128)
		self.surface = None
		self.maxItemSize = [0,0]
		self.selection = 0
		self.selectionColor = (0,255,0)
		self.itemSpacing = 20
		self.soundList = {"move":None, "select":None, "error":None}
		self.menuSounds = True
	
	####################################################################
	# A D D
	####################################################################
	def add(self, item):
		""" Add an item to the menu """
		if not self.font: raise eNoFont
		
		# STRING
		if type(item) == menuItem:
			self.menuItems.append(item)
			self.resize( self.font.render(item.name, True, self.fontColor).get_size() )
		elif type(item) == menuSlider:
			self.menuItems.append(item)
		else:
			raise eUnknownItemType, type(item)
	

	####################################################################
	# R E S I Z E
	####################################################################
	def resize(self, newsize):
		""" Increase the size of the menu if required """
		if newsize[0] > self.maxItemSize[0]: self.maxItemSize[0] = newsize[0]
		if newsize[1] > self.maxItemSize[1]: self.maxItemSize[1] = newsize[1]
		

	####################################################################
	# S E T
	####################################################################
	def setFont(self, font, fontColor):
		""" Set the font to be used for the menu items """
		self.font = font
		self.fontColor = fontColor
	
	def setSurface(self, surface):
		""" Set the surface we want to render to """
		self.surface = surface
	
	def setItemSpacing(self, spacing):
		""" Set the spacing """
		self.itemSpacing = spacing
	
	def setSelectionColor(self, color):
		""" Set the spacing """
		self.selectionColor = color
	
	def setSounds(self, move=None, select=None, error=None):
		""" Set the spacing """
		self.soundList["move"] = move
		self.soundList["select"] = select
		self.soundList["error"] = error
		self.menuSounds = True
		
	
	####################################################################
	# G E T
	####################################################################
	def __len__(self):
		""" Work with len() """
		return len(self.menuItems)
		
	def getFont(self):
		return self.font
		
	def getSurface(self):
		return self.surface
		
	def getItemSpacing(self):
		return self.itemSpacing
		
	def getSelection(self):
		""" Return current selection """
		return self.selection
	
	def getSelectionColor(self):
		return self.selectionColor
	

	####################################################################
	# S E L E C T I O N
	####################################################################
	def selectUp(self):
		""" Move selection up """
		self.selection = (self.selection-1) % len(self.menuItems)
		#if self.menuSounds: self.soundList["move"].play()
	
	def selectDown(self):
		""" Move selection down """
		self.selection = (self.selection+1) % len(self.menuItems)
		#if self.menuSounds: self.soundList["move"].play()
	
	def selectLeft(self):
		""" Move selection left """
		try:
			self.menuItems[self.selection].current -= self.menuItems[self.selection].step
			#if self.menuSounds: self.soundList["move"].play()
		except:
			pass
		print "move left"
	
	def selectRight(self):
		""" Move selection right """
		try:
			self.menuItems[self.selection].current += self.menuItems[self.selection].step
			#if self.menuSounds: self.soundList["move"].play()
		except:
			pass
		print "move right"
	

	####################################################################
	# R E N D E R
	####################################################################
	def render(self, pos):
		""" Render the menu """
		# Error checking
		if not self.font: raise eNoFont
		if not self.surface: raise eNoSurface
		if not self.menuItems: raise eMenuEmpty
		
		#self.surface.fill( (40,40,40), (pos[0], pos[1], self.maxItemSize[0], self.maxItemSize[1]) )
		
		# Get rendering biatch..
		x, y = pos[0], pos[1]
		for i in self.menuItems:
			sel = self.menuItems.index(i)
			
			if type(i) == menuItem:
				if sel == self.selection:
					color = self.selectionColor
				else:
					color = self.fontColor
					
				self.surface.blit( self.font.render(i.name, True, color), (x,y) )
				y += self.itemSpacing
				
			elif type(i) == menuSlider:
				if sel == self.selection:
					color = self.selectionColor
				else:
					color = self.fontColor
				# Text	
				tmpTxt = self.font.render(i.name, True, color)
				self.surface.blit( tmpTxt, (x,y) )
				# Slider
				amount = (i.width/(i.max-i.min))*(i.current-i.min)
				tmpSurface = pygame.Surface((i.width,i.height))
				tmpSurface.fill( self.fontColor )
				tmpSurface.fill( self.selectionColor, (0,0,amount,i.height) )
				
				self.surface.blit( tmpSurface, (x+tmpTxt.get_width(), y) )
				y += self.itemSpacing
				
			else:
				raise eUnknownItemType, type(i)

















		#menuItems = ["Play Wordy!", "How to play", "Options", "Quit"]
		#selected = 0
		
		#selectPos = 0
		#selectDestPos = 0
		

			# Move selector
			#if selectPos > selectDestPos: selectPos -= abs( (selectPos-selectDestPos )/4.0)
			#elif selectPos < selectDestPos: selectPos += abs( (selectPos-selectDestPos )/4.0)
			#if abs(selectPos-selectDestPos) < 1: selectPos = selectDestPos
			#print selectPos, selectDestPos

			# Draw menu selector
			#tmpRect = (self.screen.get_width(), 30)
			#tmpSurface = pygame.Surface(tmpRect).convert_alpha()
			#tmpSurface.fill((200,200,255))
			#self.screen.blit( tmpSurface, (0, 145+selectPos) )
			
			# Draw menu items
			#for item in xrange(len(menuItems)):
			#	if item == selected:
			#		color = (0,0,255)
			#		selectDestPos = item*30
			#	else:
			#		color = (200,200,200)
			#	txt = self.font["tile"].render(menuItems[item], True, color)
			#	self.screen.blit( txt, (300,150+(item*30)))

