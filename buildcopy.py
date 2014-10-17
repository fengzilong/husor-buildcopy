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
			#print '[' + filename + '] δ�ҵ�ƥ���ļ�...'
			#print '-' * 32
		elif excludefiles.has_key(filename):
			duplicates.append('[' + filename + ']\n' + ', '.join(excludefiles[filename]) + '')
			#print '-' * 32
			#print '[' + filename + '] �����ظ��ļ�...'
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

	print '������ɣ����ι�����' + str(counter) + '���ļ�'
	
	print str(len(unmatches)) + '���ļ�δƥ��: '
	print '\n'.join(unmatches)
	
	print str(len(duplicates)) + '���ļ������ظ�: '
	print '\n'.join(duplicates)
	
	if len(unmatches) > 0 or len(duplicates) > 0:
		print '����δƥ����ظ��ļ������ֶ�����...'

def sameFind(path):
	files = {}
	excludefiles = {}
	
	for root, dirs, filenames in os.walk(path):
		for filename in filenames:
			if files.has_key(filename):
				#������Ѵ��ڣ�counter + 1����¼path
				files[filename]['counter'] = files[filename]['counter'] + 1
				files[filename]['path'].append(os.path.join(root, filename))
			else:
				#����������ڣ��򴴽�������ʼ��counter & path
				files[filename] = {}
				files[filename]['counter'] = 1
				files[filename]['path'] = []
				files[filename]['path'].append(os.path.join(root, filename))

	for (k, v) in files.items():
		if v['counter'] > 1:
			#print '\n' + '-' * 32
			#print '�ҵ��ظ��ļ�: '
			#print '�ļ���: ' + k
			#print '����: ' + str(v['counter']) + '��'
			#print '����·��: ' + ', '.join(v['path'])
			#print '-' * 32
			excludefiles[k] = v['path']

	return excludefiles

if __name__ == "__main__":
	print '���ڶ�ȡ�����Ե�...'

	excludefiles = dict(sameFind('.\\assets\\'), **sameFind('.\\build\\'))

	files = {'js' : {}, 'css' : {}}

	#����js�ļ�
	buildJsPath=".\\assets\\js\\"
	files['js'] = walkDirs(buildJsPath)

	#����css�ļ�
	buildCssPath = ".\\assets\\css\\"
	files['css'] = walkDirs(buildCssPath)

	print '���ҵ�' + str(len(files['js'])) + '��js�ļ���' + str(len(files['css'])) + '��css�ļ�\n'

	copytype = raw_input('����js����css(����js��css)?')
	if(files.has_key(copytype)):
		copyFrom(files[copytype], '.\\build\\', excludefiles)
		pass
	else:
		print '�������'
	
	
	
	
	
