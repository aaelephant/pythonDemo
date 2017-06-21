#!/usr/local/bin/python
#- * - coding:utf-8 - * -


from collections import namedtuple

class Entity(object):
	"""docstring for Entity"""

	def __init__(self, class_name, columns, **kwargs):
		super(Entity, self).__init__()
		_columns = [i.strip() for i in columns.split(" ") if i.strip()]
		_columns.extend(kwargs.keys())
		print _columns
		columns = list(set(_columns))
		print columns
		entity = namedtuple(class_name, columns)
		print entity
		self._entity = entity(**kwargs)

	def __getattribute__(self, key):
		entity = super(Entity, self).__getattribute__("_entity")
		try:
			return super(Entity, self).__getattribute__(key)
		except:
			print '(get except)'
			return getattr(entity, key)


	def __setattr__(self, key, value):
		if key == "_entity":
			super(Entity, self).__setattr__("_entity", value)
			return
		entity = super(Entity, self).__getattribute__("_entity")
		try:
			# setattr(entity, key, value)
			entity.__setattr__(key, value)
		except:
			print '(set except)'
			super(Entity, self).__setattr__(key, value)


if __name__ == '__main__':
	user = {"name": "zhipeng", "age": 20}
	entity = Entity("user", "", **user)
	print entity
	# print dir(entity)
	print entity.name, entity.age
	# print entity.score
	# entity(name='yin')
	# TPoint = namedtuple('TPoint', ['x', 'y'])
	# p = TPoint(x=10, y=20)
	# print p.x + p.y
	entity.hh = 100
	# entity.score = 200
	# print entity.score
	print entity.hh
	entity.name = 'zhang'
	print entity.name

	entity.sex = "boy"
	print "sex:", entity.sex

		