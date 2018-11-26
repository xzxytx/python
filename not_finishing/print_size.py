import sys
import os
print(sys.argv)
print(os.getcwd())


def get_FileSize(filePath):
	# filePath = unicode(filePath,'utf8')
	l = []
	try:
		l = os.listdir(filePath)
	except:
		pass
	try:
		fsize = os.path.getsize(filePath)
	except:
		fsize = 0
	z = 0
	for i in l:
		z += get_FileSize(filePath + '\\' + i)
	return fsize + z
	# print(fsize)
	# fsize = fsize/float(1024*1024)
	# return round(fsize,2)
# l = os.listdir('此电脑/MI 8/内部存储设备')
path = os.getcwd()
l = os.listdir(path)
print(l)
print('='*50)
for file in l:
	size_mb = get_FileSize(path + '\\' +file)/1024/1024
	print(file.ljust(40), round(size_mb, 1), 'MB')
input('任意键 结束')