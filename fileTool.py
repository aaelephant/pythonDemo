#!/usr/bin/python

import io

file = io.open('hello.py', 'r')
result = file.readall()

print result