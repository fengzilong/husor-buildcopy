#!/usr/bin/python
# -*- coding:gbk -*-
# filename : buildcopy.py

import sys, os

def walkDirs(path):
	files = {}
	
	for root, dirs, filenames in os.walk(path):
		for filename in filenames:
			files[filename] = os.path.join(root, filename)

	return files

def copyFrom(copyfiles, findpath, excludefiles):
	findfiles = walkDirs(findpath)
	unmatches = []
	duplicates = []
	counter = 0

	for filename in copyfiles:
		if not findfiles.has_key(filename):
			unmatches.append('[' + filename + ']')
			#print '-' * 32
			#print '[' + filename + '] 未找到匹配文件...'
			#print '-' * 32
		elif excludefiles.has_key(filename):
			duplicates.append('[' + filename + ']\n' + ', '.join(excludefiles[filename]) + '')
			#print '-' * 32
			#print '[' + filename + '] 存在重复文件...'
			#print '\n'.join(excludefiles[filename])
			#print '-' * 32
		else:
			cfp = open(copyfiles[filename], 'w')
			ffp = open(findfiles[filename], 'r')
			try:
				content = ffp.read();
				cfp.write(content)
				counter = counter + 1
			except Exception, e:
				raise
			finally:
				cfp.close()
				ffp.close()

	print '拷贝完成，本次共拷贝' + str(counter) + '个文件'
	
	print str(len(unmatches)) + '个文件未匹配: '
	print '\n'.join(unmatches)
	
	print str(len(duplicates)) + '个文件存在重复: '
	print '\n'.join(duplicates)
	
	if len(unmatches) > 0 or len(duplicates) > 0:
		print '存在未匹配或重复文件，请手动操作...'

def sameFind(path):
	files = {}
	excludefiles = {}
	
	for root, dirs, filenames in os.walk(path):
		for filename in filenames:
			if files.has_key(filename):
				#如果键已存在，counter + 1并记录path
				files[filename]['counter'] = files[filename]['counter'] + 1
				files[filename]['path'].append(os.path.join(root, filename))
			else:
				#如果键不存在，则创建，并初始化counter & path
				files[filename] = {}
				files[filename]['counter'] = 1
				files[filename]['path'] = []
				files[filename]['path'].append(os.path.join(root, filename))

	for (k, v) in files.items():
		if v['counter'] > 1:
			#print '\n' + '-' * 32
			#print '找到重复文件: '
			#print '文件名: ' + k
			#print '数量: ' + str(v['counter']) + '个'
			#print '所在路径: ' + ', '.join(v['path'])
			#print '-' * 32
			excludefiles[k] = v['path']

	return excludefiles

if __name__ == "__main__":
	print '正在读取，请稍等...'

	excludefiles = dict(sameFind('.\\assets\\'), **sameFind('.\\build\\'))

	files = {'js' : {}, 'css' : {}}

	#所有js文件
	buildJsPath=".\\assets\\js\\"
	files['js'] = walkDirs(buildJsPath)

	#所有css文件
	buildCssPath = ".\\assets\\css\\"
	files['css'] = walkDirs(buildCssPath)

	print '共找到' + str(len(files['js'])) + '个js文件，' + str(len(files['css'])) + '个css文件\n'

	copytype = raw_input('拷贝js还是css(输入js或css)?')
	if(files.has_key(copytype)):
		copyFrom(files[copytype], '.\\build\\', excludefiles)
		pass
	else:
		print '输入错误'
	
	
	
	
	
