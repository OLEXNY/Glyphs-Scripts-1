#MenuTitle: Permutation Text Generator
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Outputs glyph permutation text for kerning.
"""

import vanilla
import GlyphsApp
import re

class PermutationTextGenerator( object ):
	def __init__( self ):
		# Window 'self.w':
		editY = 22
		textY  = 17
		spaceX = 10
		spaceY = 10
		buttonX = 120
		buttonY = 20
		windowWidth = 400
		windowHeight = spaceY*7+editY*2+textY*2+buttonY+20
		windowWidthResize  = 600 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Permutation Text Generator", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.Tosche.PermutationTextGenerator.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.text_1 = vanilla.TextBox( (spaceX, spaceY, 40, textY), "List 1", sizeStyle='regular' )
		self.w.edit_1 = vanilla.EditText( (spaceX*2+40, spaceY, -15, editY), "", sizeStyle = 'small')
		self.w.text_2 = vanilla.TextBox( (spaceX, spaceY*2+editY, 40, textY), "List 2", sizeStyle='regular' )
		self.w.edit_2 = vanilla.EditText( (spaceX*2+40, spaceY*2+editY, -15, editY), "", sizeStyle = 'small')
		self.w.text_3 = vanilla.TextBox( (spaceX*2+40, spaceY*3+editY*2, 85, textY), "Insert List 2", sizeStyle='regular' )
		self.w.radio  = vanilla.RadioGroup((spaceX*3+120, spaceY*3+editY*2, 200, textY), ["Both", "Before", "After"], isVertical = False, sizeStyle='regular')
		self.w.text_4 = vanilla.TextBox( (spaceX*2+40, spaceY*4+editY*2+textY, 320, textY), "Line break after every", sizeStyle='regular' )
		self.w.edit_3 = vanilla.EditText( (spaceX*2+184, spaceY*4+editY*2+textY-2, 40, editY), "0", sizeStyle = 'regular')
		self.w.text_5 = vanilla.TextBox( (spaceX*2+228, spaceY*4+editY*2+textY, 40, textY), "pairs", sizeStyle='regular' )
		# Run Button:
		self.w.outputButton = vanilla.Button((spaceX*2+40, spaceY*6+editY*2+textY*2, buttonX, buttonY), "Macro Panel", sizeStyle='regular', callback=self.PermutationTextGeneratorMain )
		self.w.viewButton = vanilla.Button((spaceX*3+40+buttonX, spaceY*6+editY*2+textY*2, buttonX, buttonY), "Edit View", sizeStyle='regular', callback=self.PermutationTextGeneratorMain )
		self.w.setDefaultButton( self.w.viewButton )
		
		# Load Settings:
		if not self.LoadPreferences():
			print "Note: 'Permutation Text Generator' could not load preferences. Will resort to defaults"
			
		
		# Open window and focus on it:
		self.w.open()
		self.w.radio.set(0)
		self.w.makeKey()

		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_1"] = self.w.edit_1.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_2"] = self.w.edit_2.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.radio"] = self.w.radio.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_3"] = self.w.edit_3.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			self.w.edit_1.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_1"] )
			self.w.edit_2.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_2"] )
			self.w.radio.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.radio"] )
			self.w.edit_3.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_3"] )
		except:
			return False
			
		return True

	def makeList(self, string):
		try:
			newList=[]
			while string !="":
				if string[0] == "/":
					name = ""
					while string != "" or (string[0] != "/" and string[0] !=" "):
						name = name + string[0]
						if string != "":
							try:
								string = string[1:]
							except:
								pass
						if string =="" or string[0] == "/" or string[0] == " ":
							break
					newList.append(name)
				elif string[0] == " ":
					string = string[1:]
				else:
					newList.append(string[0])
					string = string[1:]
			return newList

		except Exception, e:
			Glyphs.showMacroWindow()
			print "Permutation Text Generator Error: %s" % e

	def PermutationTextGeneratorMain( self, sender ):
		try:
			string1 = self.w.edit_1.get()
			string2 = self.w.edit_2.get()
			if string1 == "" or string2 == "":
				Glyphs.showMacroWindow()
				print "There needs to be something in both fields."
			else:
				newList1 = self.makeList(string1)
				newList2 = self.makeList(string2)
				finalRow = []
				for item2 in newList2:
					if item2[0] == "/":
						item2 = item2 + " "
					row = ""
					
					if self.w.radio.get() ==1: # if Before
						if int(self.w.edit_3.get()) != 0:
							i = 0
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								
								if i == int(self.w.edit_3.get()): # line break at every 'i'th pair
									row = row + "\n" + item2 + item1
									i = 0
								else:
									row = row + " " + item2 + item1
								i = i+1
						else:
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								row = row + " "+ item2 + item1
						row = row[1:]
						finalRow.append(row)

					elif self.w.radio.get() ==2: # if After
						if int(self.w.edit_3.get()) != 0:
							i = 1
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								
								if i == int(self.w.edit_3.get()): # line break at every 'i'th pair
									row = row + item1 + item2+ "\n"
									i = 0
								else:
									row = row + item1 + item2 + " "
								i = i+1
						else:
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								row = row + item1 + item2 + " "
						finalRow.append(row)

					else: # if Both
						if int(self.w.edit_3.get()) != 0:
							i = 1
							row = row + item2
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								
								if i == int(self.w.edit_3.get()): # line break at every 'i'th pair
									row = row + item1 + item2+ "\n" + item2
									i = 0
								else:
									row = row + item1 + item2
								i = i+1
						else:
							row = row + item2
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								row = row + item1 + item2
						finalRow.append(row)

				if sender == self.w.outputButton: # Show in Macro Window
					Glyphs.showMacroWindow()
					for thisRow in finalRow:
						print thisRow

				else:
					if int(self.w.edit_3.get()) != 0:
						finalText="\n".join(finalRow)
						finalText=re.sub(" \n", "\n", finalText)
					else:
						finalText=row
					
					try:
						Glyphs.currentDocument.windowController().activeEditViewController().graphicView().setDisplayString_(finalText)
					except:
						Glyphs.currentDocument.windowController().addTabWithString_(finalText)
			
			if not self.SavePreferences( self ):
				print "Note: 'Permutation Text Generator' could not write preferences."
			
			
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Permutation Text Generator Error: %s" % e

PermutationTextGenerator()