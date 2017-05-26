#encoding=utf8

import sys,os,re,hashlib,time
#需要安装tqdm插件
from conf import conf

class compare():
	def __init__(self,file,project,floder,install):
		self.path = file
		self.other = re.sub('new','old',self.path)
		self.project = project
		self.floder = floder
		self.install = install
		self.run()
	def run(self):
		config_path = eval("conf.%s['path']"%(str(project)))
		filePath = self.path.split('/')[-2]
		otherPath = re.sub('new','old',filePath)
		#print path+self.other.split(path)[1]
		#filename = str(files).split('/')[-1]
		if os.path.exists(self.other):
			#print self.other.split(config_path)
			fileRoute = config_path+self.other.split(self.project)[1]
			pathMd5 = self.getFileMD5(self.path)
			otherMd5 = self.getFileMD5(self.other)
			if pathMd5 == otherMd5:
				pass
			else:
				self.install.write('rm -rf %s \n'%fileRoute)
				self.install.flush()
				print self.package(self.path)
		else:
			paths = config_path+filePath
			if not os.path.exists(paths):
				#print "mkdir %s \n"%paths
				self.install.write("mkdir %s \n"%paths)
				self.install.flush()
			print self.package(self.path)
	def getFileMD5(self,filepath):
	    f = open(filepath,'rb')
	    md5obj = hashlib.md5()
	    md5obj.update(f.read())
	    hash = md5obj.hexdigest()
	    f.close()
	    return str(hash).upper()
	def package(self,filepath):
		relatively = self.path.split('%s'%(self.project))
		path = relatively[1].split('/')[:-1]
		realPath = '/'.join(path)
		filename = str(self.path).split('/')[-1]
		#print "cp %s /home/script/vlib/package/%s"%(str(self.path),str(self.floder))
		#print "cp %s ../..%s/ \n"%(str(filename),str(realPath))
		os.system(r"cp %s /home/script/vlib/package/%s"%(str(self.path),str(self.floder)))
		self.install.write(r"cp %s ../..%s/ \n"%(str(filename),str(realPath)))
		#note.write('echo 文件 %s 已经复制到 %s'%(str(filename),str(relatively[1])))
		self.install.flush()
		return '发现变动文件 %s 已复制'%(str(self.path))


def filePath(path,p):
	ignore = {'file':[],'floder':[]}
	listDir = []
	delDir = []
	config_ignoreFile = eval("conf.%s['file']"%(str(p)))
	config_ignoreFloder = eval("conf.%s['floder']"%(str(p)))
	for doc in config_ignoreFile:
		ignore['file'].append("%s/%s"%(str(path),str(doc)))
	for floder in config_ignoreFloder:
		ignore['floder'].append("%s/%s"%(str(path),str(floder)))
	for parent,dirnames,filenames in os.walk(path):
		for name in filenames:
			listDir.append('%s/%s'%(str(parent),str(name)))
	listDir = list(set(listDir))
	for route in listDir:
		if route in ignore['file']:
			delDir.append(route)
		for ignorePath in ignore['floder']:
			if route.startswith('%s'%(str(ignorePath))):
				delDir.append(route)
	delDir = list(set(delDir))
	for k in delDir:
		if k in listDir:
			listDir.remove(k)
	return listDir

def create(project):
	path = '/version/new/%s'%(str(project))
	addr = filePath(path,project)
	now = time.time()
	curtime = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(now))
	floder = "%s-%s"%(str(project),str(curtime))
	os.system("mkdir ./package/%s"%(str(floder)))
	os.system("touch ./package/%s/setup.sh"%(str(floder)))
	note = open('/home/script/vlib/package/%s/setup.sh'%(str(floder)),'a+')
	note.write('#!/bin/bash \n')
	for way in addr:
		compare(way,project,floder,note)
	note.close()
	print "正在生成安装包 ..."
	os.system('tar zcvf /home/script/vlib/install/%s.tar.gz ./package/%s'%(str(floder),str(floder)))
	print "安装包已生成，位置： /home/script/vlib/install/%s.tar.gz"%(str(floder))
	os.system("cd /version/old/%s/ && git pull"%project)

if __name__ == '__main__':
    #create('/version/new/hiture_HGCP','hiture_HGCP')
    project = sys.argv[1]
    create(str(project))
