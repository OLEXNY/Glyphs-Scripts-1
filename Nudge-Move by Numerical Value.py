#MenuTitle: Nudge-move by Numerical Value
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Nudge-moves selected nodes by the values specified in the window. Vanilla required.
"""

import vanilla
import GlyphsApp

class NudgeMoveWindow( object ):
	def __init__( self ):
		spaceX = 14
		spaceY = 14
		textSizeX = 16
		buttonSizeX = 60
		fieldSizeX = 60
		elementSizeY = 20
		# Window 'self.w':
		windowWidth  = spaceX+textSizeX+spaceX+buttonSizeX+spaceX+fieldSizeX+spaceX+buttonSizeX+spaceX
		windowHeight = spaceY+elementSizeY+spaceY+elementSizeY+spaceY
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Nudge-Move", # window title
			autosaveName = "com.tosche.Nudge-movebyNumericalValue(GUI).mainwindow" # stores last window position and size
		)
		
		# Text:
		self.w.textX = vanilla.TextBox( ( spaceX, spaceY+2, textSizeX, elementSizeY), "X:", sizeStyle='small' )
		self.w.textY = vanilla.TextBox( ( spaceX, spaceY+elementSizeY+spaceY+2, textSizeX, elementSizeY), "Y:", sizeStyle='small' )
		# Field
		self.w.fieldX = vanilla.EditText( (spaceX+textSizeX+spaceX+buttonSizeX+spaceX, spaceY, fieldSizeX, elementSizeY), "0", sizeStyle = 'small')
		self.w.fieldY = vanilla.EditText( (spaceX+textSizeX+spaceX+buttonSizeX+spaceX, spaceY+elementSizeY+spaceY, fieldSizeX, elementSizeY), "0", sizeStyle = 'small')
		# Run Button:
		self.w.leftButton = vanilla.SquareButton((spaceX+textSizeX+spaceX, spaceY, buttonSizeX, elementSizeY), "Left", sizeStyle='small', callback=self.nudgeMove )
		self.w.rightButton = vanilla.SquareButton((spaceX+textSizeX+spaceX+buttonSizeX+spaceX+fieldSizeX+spaceX, spaceY, buttonSizeX, elementSizeY), "Right", sizeStyle='small', callback=self.nudgeMove )
		self.w.downButton = vanilla.SquareButton((spaceX+textSizeX+spaceX, spaceY+elementSizeY+spaceY, buttonSizeX, elementSizeY), "Down", sizeStyle='small', callback=self.nudgeMove )
		self.w.upButton = vanilla.SquareButton((spaceX+textSizeX+spaceX+buttonSizeX+spaceX+fieldSizeX+spaceX, spaceY+elementSizeY+spaceY, buttonSizeX, elementSizeY), "Up", sizeStyle='small', callback=self.nudgeMove )
		
		# Load Settings:
		if not self.LoadPreferences():
			print "Note: 'Nudge-move by Numerical Value (GUI)' could not load preferences. Will resort to defaults"
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.tosche.Nudge-movebyNumericalValue(GUI).fieldX"] = self.w.fieldX.get()
			Glyphs.defaults["com.tosche.Nudge-movebyNumericalValue(GUI).fieldY"] = self.w.fieldY.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			self.w.fieldX.set( Glyphs.defaults["com.tosche.Nudge-movebyNumericalValue(GUI).fieldX"] )
			self.w.fieldY.set( Glyphs.defaults["com.tosche.Nudge-movebyNumericalValue(GUI).fieldY"] )
		except:
			return False
			
		return True

	def nudgeMove( self, sender ):
		try:
			float(self.w.fieldX.get())
			float(self.w.fieldY.get())

			if sender is self.w.leftButton:
				offsetX = -float(self.w.fieldX.get())
				offsetY = 0.0
			elif sender is self.w.rightButton:
				offsetX = float(self.w.fieldX.get())
				offsetY = 0.0
			elif sender is self.w.upButton:
				offsetX = 0.0
				offsetY = float(self.w.fieldY.get())
			elif sender is self.w.downButton:
				offsetX = 0.0
				offsetY = -float(self.w.fieldY.get())
	
			try:
				Font = Glyphs.font # frontmost font
				listOfSelectedLayers = Font.selectedLayers
				
				def nudge(oncurveMv, offcurve1, offcurve2, oncurveSt):
					distanceX = oncurveMv.x - oncurveSt.x
					distanceX1 = oncurveMv.x - offcurve1.x
					distanceX2 = offcurve2.x - oncurveSt.x
					if distanceX1 != 0:
						offcurve1.x += (1-distanceX1/distanceX)*offsetX
					else:
						offcurve1.x += offsetX
				
					if distanceX2 != 0:
						offcurve2.x += (distanceX2/distanceX)*offsetX
				
					distanceY = oncurveMv.y - oncurveSt.y
					distanceY1 = oncurveMv.y - offcurve1.y
					distanceY2 = offcurve2.y - oncurveSt.y
					if distanceY1 != 0:
						offcurve1.y += (1-distanceY1/distanceY)*offsetY
					else:
						offcurve1.y += offsetY
				
					if distanceY2 != 0:
						offcurve2.y += (distanceY2/distanceY)*offsetY
					
	
				for thisLayer in Font.selectedLayers:
					glyph = thisLayer.parent
					glyph.beginUndo()
					for thisPath in thisLayer.paths:
						numOfNodes = len(thisPath.nodes)
						for i in range(numOfNodes):
							node = thisPath.nodes[i]
							if node in thisLayer.selection():
								nodeBefore = thisPath.nodes[i-1]
								if not nodeBefore in thisLayer.selection():
									if nodeBefore.type == 65:
										if thisPath.nodes[i-2].type == 65:
											oncurveMv = node
											offcurve1 = nodeBefore
											offcurve2 = thisPath.nodes[i-2]
											oncurveSt = thisPath.nodes[i-3]
											nudge(oncurveMv, offcurve1, offcurve2, oncurveSt)
				
										# if off-curve is the edge of selection
										elif thisPath.nodes[i-2].type != 65:
											oncurveMv = thisPath.nodes[i+1]
											offcurve1 = node
											offcurve2 = nodeBefore
											oncurveSt = thisPath.nodes[i-2]
											nudge(oncurveMv, offcurve1, offcurve2, oncurveSt)
											node.x -= offsetX
											node.y -= offsetY
											
								nodeAfter = thisPath.nodes[i+1]
								if not nodeAfter in thisLayer.selection():
									if nodeAfter.type == 65:
										if thisPath.nodes[i+2].type ==65:
											oncurveMv = node
											offcurve1 = nodeAfter
											offcurve2 = thisPath.nodes[i+2]
											oncurveSt = thisPath.nodes[i+3]
											nudge(oncurveMv, offcurve1, offcurve2, oncurveSt)
										# if off-curve is the edge of selection
										elif thisPath.nodes[i+2].type != 65:
											thisPath.nodes[i-1].x -= offsetX
											thisPath.nodes[i-1].y -= offsetY
											oncurveMv = thisPath.nodes[i-1]
											offcurve1 = node
											offcurve2 = nodeAfter
											oncurveSt = thisPath.nodes[i+2]
											nudge(oncurveMv, offcurve1, offcurve2, oncurveSt)
											thisPath.nodes[i-1].x += offsetX
											thisPath.nodes[i-1].y += offsetY
											node.x -= offsetX
											node.y -= offsetY
											
								node.x += offsetX
								node.y += offsetY
					glyph.endUndo()
				
				if not self.SavePreferences( self ):
					print "Note: 'Nudge-move by Numerical Value (GUI)' could not write preferences."
				
			except Exception, e:
				# brings macro window to front and reports error:
				Glyphs.showMacroWindow()
				print "Nudge-move by Numerical Value (GUI) Error: %s" % e

		except:
			Glyphs.displayDialog_withTitle_("You seem to have entered a value that is not a number. Period is fine.", "Numbers only!")


NudgeMoveWindow()