# -*- coding: latin-1 -*-

class Color:
	'''	Color is a representation of colors. 
	
	Attribute:
		CONST_LAMBDA	Lambda used for float comparison ( 1/2550 )
	
	'''
	CONST_LAMBDA = 0.0004
	
	colorOpColor = {
		'+'  : lambda col1,col2: Color( c=col1.getCyan()+col2.getCyan(), m=col1.getMagenta()+col2.getMagenta(), y=col1.getYellow()+col2.getYellow() ),
		'-'  : lambda col1,col2: Color( c=col1.getCyan()-col2.getCyan(), m=col1.getMagenta()-col2.getMagenta(), y=col1.getYellow()-col2.getYellow() ),
		'*'  : lambda col1,col2: Color( c=col1.getCyan()*col2.getCyan(), m=col1.getMagenta()*col2.getMagenta(), y=col1.getYellow()*col2.getYellow() ),
		'/'  : lambda col1,col2: Color( c=col1.getCyan()/col2.getCyan(), m=col1.getMagenta()/col2.getMagenta(), y=col1.getYellow()/col2.getYellow() ),
		'==' : lambda col1,col2: abs( col1.getCyan()-col2.getCyan() ) < Color.CONST_LAMBDA and abs( col1.getMagenta()-col2.getMagenta() ) < Color.CONST_LAMBDA and abs( col1.getYellow()-col2.getYellow() ) < Color.CONST_LAMBDA ,
		'<'	 : lambda col1,col2: col1.getCyan() < col2.getCyan() and col1.getMagenta() < col2.getMagenta() and col1.getYellow() < col2.getYellow(),
		'>'	 : lambda col1,col2: col1.getCyan() > col2.getCyan() and col1.getMagenta() > col2.getMagenta() and col1.getYellow() > col2.getYellow(),

	}
	
	colorOpFloat = {
		'+' : lambda col,flo: Color( c=col.getCyan()+flo, m=col.getMagenta()+flo, y=col.getYellow()+flo ),
		'-' : lambda col,flo: Color( c=col.getCyan()-flo, m=col.getMagenta()-flo, y=col.getYellow()-flo ),
		'*' : lambda col,flo: Color( c=col.getCyan()*flo, m=col.getMagenta()*flo, y=col.getYellow()*flo ),
		'/' : lambda col,flo: Color( c=col.getCyan()/flo, m=col.getMagenta()/flo, y=col.getYellow()/flo ),
	}
	
	def __init__(self,**kwargs):
		''' RGB values are in range [0,255], integer format
			CMY values ar in range [0.0,1.0], float format '''
		if( 'c' in kwargs or 'm' in kwargs or 'y' in kwargs ):
			self._c = Color.putInCmyRange( kwargs['c'] )
			self._m = Color.putInCmyRange( kwargs['m'] )
			self._y = Color.putInCmyRange( kwargs['y'] )
		elif( 'r' in kwargs or 'g' in kwargs or 'b' in kwargs ):
			self._c, self._m, self._y = Color.rgbToCmy( Color.putInRgbRange( kwargs['r'] ), Color.putInRgbRange( kwargs['g'] ), Color.putInRgbRange( kwargs['b'] ) )
		else:
			raise NameError('Color bad initialisation')
	
	# Accessors
	def getCyan(self):
		return self._c
		
	def getMagenta(self):
		return self._m
		
	def getYellow(self):
		return self._y
		
	def setCyan(self, c):
		self._c = Color.putInCmyRange(c)
			
	def setMagenta(self, m):
		self._m = Color.putInCmyRange(m)
		
	def setYellow(self, y):
		self._y = Color.putInCmyRange(y)
	
	# Conversion
	@classmethod
	def rgbToCmy(cls, r, g, b):
		return 1 - ( r / 255 ), 1 - ( g / 255 ), 1 - ( b / 255 )
	@classmethod
	def cmyToRgb(cls, c, m, y):
		return int( ( 1 - c ) * 255 ), int( ( 1 - m ) * 255 ), int( ( 1 - y ) * 255 )
	
	def toCmy(self):
		return self._c, self._m, self._y
	
	def toRgb(self):
		return self.cmyToRgb(self._c, self._m, self._y)
		
	# Operators
	def __mul__(self, other):
		if isinstance(other,Color):
			return Color.colorOpColor['*'](self,other)
		elif isinstance(other, float):
			return Color.colorOpFloat['*'](self,other)
		else:
			raise NameError('Wrong multiplyer type. \n Should be Color or float')
	def __rmul__(self, other):
		return self.__mul__(self, other)
		
	def __truediv__(self, other):
		if isinstance(other,Color):
			if ( other.hasZeroValue() ):
				raise NameError('Zero division, you broke math !')
			return Color.colorOpColor['/'](self,other)
		elif isinstance(other, float):
			if ( other == 0.0 ):
				raise NameError('Zero division, you broke math !')
			return Color.colorOpFloat['/'](self,other)
		else:
			raise NameError('Wrong divider type. \n Should be Color or float')

	def __rtruediv__(self, other):
		return self.__truediv__(self, other)

	def __add__(self, other):
		if isinstance(other,Color):
			return Color.colorOpColor['+'](self,other)
		elif isinstance(other, float):
			return Color.colorOpFloat['+'](self,other)
		else:
			raise NameError('Wrong type added to Color. \n Should be Color or float')

	def __radd__(self, other):
		return self.__add__(self, other)

	def __sub__(self, other):
		if isinstance(other,Color):
			return Color.colorOpColor['-'](self,other)
		elif isinstance(other, float):
			return Color.colorOpFloat['-'](self,other)
		else:
			raise NameError('Wrong type substracted to Color. \n Should be Color or float')

	def __rsub__(self, other):
		return self.__sub__(self, other)
			
	def __eq__(self, other):
		if isinstance(other,Color):
			return Color.colorOpColor['=='](self,other)
		else:
			raise NameError('Wrong type compare to Color. \n Should be Color only')
			
	def __ne__(self, other):
		if isinstance(other,Color):
			return not Color.colorOpColor['=='](self,other)
		else:
			raise NameError('Wrong type compare to Color. \n Should be Color only')
			
	def __lt__(self, other):
		if isinstance(other,Color):
			return Color.colorOpColor['<'](self,other)
		else:
			raise NameError('Wrong type compare to Color. \n Should be Color only')
			
	def __gt__(self, other):
		if isinstance(other,Color):
			return Color.colorOpColor['>'](self,other)
		else:
			raise NameError('Wrong type compare to Color. \n Should be Color only')
			
	def __le__(self, other):
		if isinstance(other,Color):
			return Color.colorOpColor['<'](self,other) or Color.colorOpColor['=='](self,other)
		else:
			raise NameError('Wrong type compare to Color. \n Should be Color only')
			
	def __ge__(self, other):
		if isinstance(other,Color):
			return Color.colorOpColor['>'](self,other) or Color.colorOpColor['=='](self,other)
		else:
			raise NameError('Wrong type compare to Color. \n Should be Color only')
		
	# Tools
	def hasZeroValue(self):
		if( self._c == 0.0 or self._m == 0.0 or self._y == 0 ):
			return True
		return False
		
	def __repr__(self):
		return '%s( Cyan = %r , Magenta = %r , Yellow = %r )' % ( self.__class__, self._c, self._m, self._y ) 
		
	@classmethod
	def putInRgbRange(cls, val):
		if val < 0:
			return 0
		elif val > 255:
			return 255
		else:
			return val
	
	@classmethod
	def putInCmyRange(cls, val):
		if val < 0.0:
			return 0.0
		elif val > 1.0:
			return 1.0
		else:
			return val
		
		
if __name__ == "__main__":
	
	print ( "\n============================================")
	print (   "=       Color module tests and how to      =")
	print (   "============================================")
	
	ALICEBLUE = Color(r=240, g=248, b=255),
	CHOCOLATE = Color(r=210, g=105, b=30),
	MOCCASIN = Color(r=255, g=228, b=181),

	myColor = Color(c=0.15, m=0.3, y=0.6)
	print ( '\n>>> myColor = Color(c=0.15, m=0.3, y=0.6)' )
	print ( myColor )

	print ( "\n>>> myColor * 2.0" )
	print ( myColor * 2.0 )
	
	print ( "\n>>> myColor / 2.0" )
	print ( myColor / 2.0 )
	
	print ( "\n>>> myColor + 0.01" )
	print ( myColor + 0.01 )
	
	print ( "\n>>> myColor - 0.01" )
	print ( myColor - 0.01 )
	
	newColor = Color(r=255, g=0, b=42)
	print ( '\n>>> newColor = Color(r=255, g=0, b=42)' )
	print ( newColor )
	
	print ( "\n>>> myColor * newColor" )
	print ( myColor * newColor )
	
	print ( "\n>>> newColor.setCyan(0.24)" )
	newColor.setCyan(0.24)
	
	print ( "\n>>> myColor / newColor" )
	print ( myColor / newColor )
	
	print ( "\n>>> myColor + newColor" )
	print ( myColor + newColor )
	
	print ( "\n>>> myColor - newColor" )
	print ( myColor - newColor )
	
	alice = ALICEBLUE
	print ( "\n>>> alice = ALICEBLUE")
	print ( alice )
	
	choco = CHOCOLATE
	print ( "\n>>> choco = CHOCOLATE")
	print ( choco )
	
	indian = MOCCASIN
	print ( "\n>>> indian = MOCCASIN")
	print ( indian )
	
	print ( "\n>>> indian == choco")
	print ( indian == choco )
	
	print ( "\n>>> choco == choco")
	print ( choco == choco )
	
	print ( "\n>>> indian != choco")
	print ( indian != choco )
	
	print ( "\n>>> indian != indian")
	print ( indian != indian )
	
	print ( "\n>>> indian < choco")
	print ( indian < choco )
	
	print ( "\n>>> indian > choco")
	print ( indian > choco )
	
	print ( "\n>>> indian >= choco")
	print ( indian >= choco )
	
	print ( "\n>>> choco >= indian")
	print ( choco >= indian )
	
	print ( "\n>>> indian >= indian")
	print ( indian >= indian )
	
	print ( "\n>>> indian <= choco")
	print ( indian <= choco )
	
	print ( "\n>>> choco <= indian")
	print (  choco <= indian )
	
	print ( "\n>>> indian <= indian")
	print ( indian <= indian )
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	