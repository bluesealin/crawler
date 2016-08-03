# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from blog.models import Blog
from django.utils import timezone 
from t66y.spiders.fid7 import Fid7Spider
import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class T66YPipeline(object):
    def process_item(self, item, spider):
        #清除含空项的item
        for i in item.values():
            if i==[]:
                raise DropItem('Drop null item!')
        for key in item.keys():
            item[key]=item[key][0]
        #清除非近期发布的item
        now=datetime.datetime.now()
        pub_date=datetime.datetime.strptime(item['date_str'],'%Y-%m-%d %H:%M')
        if (now-pub_date).days>20:
            raise DropItem('Drop past item!')
        return item

    
class ModelSave(object):
    def process_item(self, item, spider):
        blog=Blog()
        blog.blog_title=item['title']
        #blog.blog_text="[%s](%s)"%(item['title'],item['href'])
        #处理href,只取最后几位数字
        num=item['href'].split('.')[-2][-7:]
        blog.blog_text='blog/html/'+num+'.html'
        blog.blog_img=''
        blog.blog_text_brief=''
        blog.pub_date=datetime.datetime.strptime(item['date_str'],'%Y-%m-%d %H:%M')
        blog.blog_praise=int(item['commentnum'])
        blog.save()
        
     
        #html=open(blog.blog_text,'w')
        #content=item['content']
        #html.write(content.encode("gbk"))
        #html.close()
        html_dir='/home/dk/mysite/blog/templates/'+blog.blog_text

        file=open(html_dir,'w')

        u=item['content']
        
        file.write(u.encode('utf-8'))#utf8转str
        
        file.close()
        
        
        
        return item
