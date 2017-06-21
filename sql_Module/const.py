#!/usr/local/bin/python
#-*- coding:utf-8 -*-

# Put in const.py...:
# class _const(object):
#     class ConstError(TypeError): pass
#     def __setattr__(self,name,value):
#         if self.__dict__.has_key(name):
#             raise self.ConstError, "Can't rebind const(%s)"%name
#         self.__dict__[name]=value
class const(object):
	class ConstError(TypeError): 
		pass
	class ConstCaseError(ConstError):
		pass

	def __setattr__(self, name, value):
		if self.__dict__.has_key(name):
			raise self.ConstError, "can't change const.%s" % name
		if not name.isupper():
			raise self.ConstCaseError, "const name '%s' is not all uppercase" % name

		self.__dict__[name] = value
import sys
sys.modules[__name__] = const()