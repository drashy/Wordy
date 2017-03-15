#!/usr/bin/env python
try:
	import pygame
except:
	print("Could not import pygame, please make sure it is installed :)")
	exit()
	
import random
import os
import ashmenu
from pygame.locals import *

# Constants
DATADIR = "data"
VERSION = "v0.1"

class wordy(object):
	def __init__(self):
		""" Initialise the game """
		pygame.init()
		
		self.screen = pygame.display.set_mode((640,480),SRCALPHA|HWSURFACE)
		#print self.screen
		
		self.sprite = {}
		self.sprite["tile"] = pygame.image.load(os.path.join(DATADIR,"block.png")).convert_alpha()
		self.sprite["star"] = pygame.image.load(os.path.join(DATADIR,"star2.png")).convert_alpha()
		self.sprite["wordBackground"] = pygame.Surface((100,400))
		self.sprite["wordBackground"].fill((230,230,230))
		
		self.font = {}
		self.font["title"] = pygame.font.Font(os.path.join(DATADIR,"whitrabt.ttf"), 40)
		self.font["tile"] = pygame.font.Font(os.path.join(DATADIR,"whitrabt.ttf"), 30)
		self.font["score"] = pygame.font.Font(os.path.join(DATADIR,"modenine.ttf"), 20)
		self.font["30"] = pygame.font.SysFont("Verdana", 30)
		self.font["20"] = pygame.font.SysFont("Verdana", 20)
		self.font["small"] = pygame.font.Font(os.path.join(DATADIR,"modenine.ttf"), 12)
		
		#self.numChars = 6
		self.maxWordLength = 6

		self.clock = pygame.time.Clock()
		
		self.menuMain()
		print "Bai!"
		#self.main()
	


	def resetGame(self, full=False):
		self.wordList = self.getNewWordList(self.maxWordLength)
		self.currentWord = self.shuffle(self.wordList[0])
		
		self.userWordList = [False for x in xrange(len(self.wordList))]
		
		self.showStar = False
		self.correctWords = 0
		
		self.currentGuess = ""
		
		if full:
			self.time = 120
			self.timeLeft = 0
			self.points = 0
		


	def makeAlpha(self, surface, alpha):
		""" Make a translucent surface """
		t = surface.convert()
		#t.blit( surface, (0,0) )
		t.set_alpha(alpha)
		return t
	


	def getNewWordList(self, maxLen):
		""" Load the word list from file and pick one :) """
		# Start a new word list
		wordList = []
		
		randWord = ""
		for l in range(maxLen,2,-1): # maxLen (probably 6) to 3
			f = open(os.path.join(DATADIR,"words%s.txt" % l))
			tmp = f.read().split()
			f.close()
			#print "Read 'words%s.txt', %s words." % (l, len(tmp))
		
			if not randWord:
				randWord = tmp[random.randint(0,len(tmp)-1)] # Pick a word at random
				
			for word in tmp:
				charCount = 0
				tmpRandWord = randWord
				for char in list(word):
					if char in tmpRandWord:
						charCount += 1
						t = list(tmpRandWord)
						t.remove(char)
						tmpRandWord = "".join(t)
				if charCount == len(word):
					wordList.append(word)
		return wordList
	
	
	
	def shuffle(self, s):
		""" Shuffle a string """
		w = list(s)
		random.shuffle(w)
		return "".join(w)
	
	
	
	def checkWord(self):
		""" Check if the users word is a real one """
		print "currentGuess is '%s'" % self.currentGuess
		if self.currentGuess in self.wordList and not self.userWordList[self.wordList.index(self.currentGuess)]:
			points = len(self.currentGuess)
			if len(self.currentGuess) == self.maxWordLength:
				points = points * 2
				print "bonus points for longest word"
				self.showStar = True
			self.points += points
			self.timeLeft += 2 # Add 2 seconds to the clock
			print "user got a word, award %s points" % points
			self.userWordList[self.wordList.index(self.currentGuess)] = True
			self.correctWords += 1
			if self.correctWords >= 5:
				self.showStar = True
		self.currentGuess = ""

	
	
	def niceTime(self,t):
		""" Make a human readable time """
		m,s = divmod(t,60)
		if s < 60 and m < 1:
			time = "%s secs" % s
		elif s == 0:
			time = "%s mins" % m
		else:
			time = "%s mins, %s secs" % (m,s)
		return time
	
	
	
	def drawTiles(self, text, x, y, color, alphaMap=False):
		""" Draw tiles for every char in 'text' """
		x -= (len(text) * 42)/2
		for t in xrange(len(text)):
			tmpSurface = self.sprite["tile"].convert_alpha()
			txt = self.font["tile"].render(text[t], True, color)
			tmpSurface.blit( txt, ((tmpSurface.get_width()-txt.get_width())/2,(tmpSurface.get_height()-txt.get_height())/2) )
			if alphaMap and alphaMap[t]:
				tmpSurface = self.makeAlpha( tmpSurface, 50 )
			self.screen.blit( tmpSurface, (x+(t*42),y) )
	
	
	
	def menuMain(self):
		""" Main menu """

		m = ashmenu.ashMenu()
		m.setFont( pygame.font.Font(os.path.join(DATADIR,"whitrabt.ttf"), 30), (200,200,200))
		m.setSelectionColor( (255,0,0) )
		m.setSurface(self.screen)
		m.setItemSpacing(30)
		for i in ["Play Wordy!", "How to play", "Options", "Quit" ]:
			m.add(ashmenu.menuItem(i))
		#m.add(ashmenu.menuSlider("Slide1",0,10,1))
		#m.add(ashmenu.menuSlider("Slide2",0,100,1))
		#m.setSounds( pygame.mixer.Sound(os.path.join(DATADIR,"move.ogg")), pygame.mixer.Sound("select.ogg"), pygame.mixer.Sound("error.ogg") )
		
		quit = 0
		while not quit:
			self.screen.fill((255,255,255))
			self.screen.blit( self.font["title"].render("Wordy!", True, (0,255,0)), (10,10) )
			self.screen.blit( self.font["20"].render("%s" % VERSION, True, (0,255,0)), (10,60) )
			
			m.render((200,200))
			
			# Process events
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						quit = True
					elif event.key == K_UP: m.selectUp()
					elif event.key == K_DOWN: m.selectDown()
					elif event.key == K_LEFT: m.selectLeft()
					elif event.key == K_RIGHT: m.selectRight()
					elif event.key == K_RETURN:
						selected = m.getSelection()
						if selected == 0: # Play
							self.startGame()
						elif selected == 1: # How to play
							self.menuHelp()
						elif selected == 2: # Options
							pass
						elif selected == 3: # Quit
							quit = True
			
			pygame.display.update()
			self.clock.tick(30)



	def menuHelp(self):
		""" Help menu """
		menuItems = ["Back"]
		selected = 0
		
		quit = 0
		while not quit:
			self.screen.fill((255,255,255))
			self.screen.blit( self.font["title"].render("How to play Wordy!", True, (0,255,0)), (0,0) )
			self.screen.blit( self.font["20"].render("Instructions coming soon ;)", True, (0,255,0)), (0,50) )
			
			# Draw menu items
			for item in xrange(len(menuItems)):
				if item == selected: color = (255,0,0)
				else: color = (200,200,200)
				txt = self.font["tile"].render(menuItems[item], True, color)
				self.screen.blit( txt, (300,150+(item*40)))
			
			# Process events
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						quit = True
					elif event.key == K_RETURN:
						if selected == 0: # Quit
							quit = True
			
			# Update screen
			pygame.display.update()
			self.clock.tick(30)
	
	
	
	def startGame(self):
		self.resetGame(True)

		timeStart = pygame.time.get_ticks()
		self.timeLeft = self.time - ((pygame.time.get_ticks()-timeStart)/1000)

		#tmpSurface = pygame.Surface((40,40))

		##################
		# MAIN GAME LOOP
		##################
		middleX = self.screen.get_width()/2
			
		ticks = pygame.time.get_ticks()
		quit = False
		while self.timeLeft > 0 and not quit:
			self.screen.fill( (255,255,255) )
			self.screen.blit( self.font["score"].render("Points: %s" % self.points, True, (0,0,0)), (0,0) )
			self.screen.blit( self.font["score"].render("Time Left: %s" % self.niceTime(self.timeLeft), True, (0,0,0)), (200,0) )
			self.screen.blit( self.font["small"].render("Press 'Space' to shuffle", True, (0,0,255)), (middleX,140) )


			# Draw currentWord tiles
			alphaMap = [False for x in xrange(self.maxWordLength)]
			for x in xrange(len(self.currentGuess)):
				for y in xrange(len(self.currentWord)):
					if self.currentGuess[x] == self.currentWord[y] and not alphaMap[y]:
						alphaMap[y] = True
						break;
			self.drawTiles(self.currentWord, middleX, 100, (255,0,0), alphaMap)
			
			# Draw currentGuess tiles
			self.drawTiles(self.currentGuess, middleX+20, 200, (0,0,255))
				
			# Draw word list
			self.screen.blit( self.sprite["wordBackground"], (5,45))
			x = 0
			y = 0
			for a in xrange(len(self.wordList)):
				if self.userWordList[a]: t = self.wordList[a]
				else: t = '-'*len(self.wordList[a])
				txt = self.font["small"].render(t, True, (255,0,0))
				self.screen.blit( txt, (10+(x*50),50+(y*12)))
				y+=1
				if y > 30:
					y = 0
					x += 1
					
			# Draw star if needed
			if self.showStar:
				self.screen.blit( self.sprite["star"], (150,150) )
				self.screen.blit( self.font["score"].render("New word available! (press TAB)", True, (0,0,0)), (160,160) )
				
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						quit = True
					elif event.key == K_TAB and self.showStar:
						self.resetGame(False)
						
					elif event.key == K_RETURN and len(self.currentGuess)>0:
						self.checkWord()
						
					elif event.key == K_SPACE:
						self.currentWord = self.shuffle(self.wordList[0])
						
					elif event.key == K_BACKSPACE and len(self.currentGuess)>0:
						self.currentGuess = self.currentGuess[:-1]
						
					elif event.key >= K_a and event.key <= K_z:
						c = pygame.key.name(event.key)
						
						self.whatsLeft = list(self.currentWord)
						for letter in self.currentGuess:
							self.whatsLeft.remove(letter)
						
						if len(self.currentGuess)<self.maxWordLength and c in self.whatsLeft:
							self.currentGuess = self.currentGuess + c

			# Adjust time left
			tmpTicks = pygame.time.get_ticks()
			if tmpTicks-ticks > 1000:
				self.timeLeft -= 1
				ticks=tmpTicks
				
			# Update the screen
			pygame.display.update()
			self.clock.tick(30)
			

		##################
		# GAME OVER LOOP
		##################
		#print "Game over with %s points" % self.points
		
		quit = 0
		while not quit:
			self.screen.fill((255,255,255))
			self.screen.blit( self.font["30"].render("Game Over!", True, (0,255,0)), (200,100) )
			self.screen.blit( self.font["20"].render("You scored %s" % self.points, True, (0,255,0)), (200,140) )
			self.screen.blit( self.font["20"].render("Hit Return to continue", True, (0,255,0)), (200,180) )
			
			# Draw word list
			self.screen.blit(self.sprite["wordBackground"], (5,45))
			x = 0
			y = 0
			for a in xrange(len(self.wordList)):
				if not self.userWordList[a]: color = (0,0,255)
				else: color = (255,0,0)
				txt = self.font["small"].render(self.wordList[a], True, color)
				self.screen.blit( txt, (10+(x*50),50+(y*12)))
				y+=1
				if y > 30:
					y = 0
					x += 1

			for event in pygame.event.get():
				if event.type == KEYUP:
					if event.key == K_SPACE or event.key == K_RETURN:
						quit = True
				if event.type == KEYDOWN:
					 if event.key == K_ESCAPE:
						 quit = True
					
						
			pygame.display.update()
			self.timeLeft = self.time - ((pygame.time.get_ticks()-timeStart)/1000)
			self.clock.tick(30)

wordy()
