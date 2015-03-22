#coding=utf8
import re , os , yaml, logging
import interface
import res
from utls.rg_io import rg_logger

#加载配置文件
#默认conf.yaml的加载器
class conf_loader:
    def  __init__(self,conf):
        self.conf    = conf
        self.curpath = os.path.dirname(self.conf)
        rg_logger.debug("yaml current path:%s" %self.curpath)
    def  replace(self,matchobj):
        filepath = matchobj.groups()[0]
        filepath = re.sub("^\.",self.curpath,filepath)
        filepath = env_exp.value(filepath)
        rg_logger.debug("import yaml:%s",filepath)
        doc      = open(filepath).read()
        return  doc
    def load(self):
        if not os.path.exists(self.conf) :
            raise interface.rigger_exception("unfound file: %s" %self.conf )
        doc = open(self.conf,"r").read()
        #自定义yaml语法解析
        #将import的文件使用正则替换掉
        doc = re.sub(r"""#!import *["'](.*)["']""",self.replace,doc)
        return doc

    def load_data(self,ori=None,new=None):
        doc = self.load()
        if ori is not None:
            doc = doc.replace(ori,"!!python/object:" + new)
        data = yaml.load(doc)
        return data
