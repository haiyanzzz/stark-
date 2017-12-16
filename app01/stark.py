#!usr/bin/env python
# -*- coding:utf-8 -*-
print("sssss6666666")
from app01 import models
from django.conf.urls import url
from stark.service import v1
from django.shortcuts import render,HttpResponse,redirect
from django.forms import ModelForm
class UserInfoConfig(v1.StarkConfig):
    # 1、
    list_display = ["id","name","email"]
    # list_display = []
   # 2、
    def extra_urls(self):
        url_list =[
            url(r'^xxxx/$',self.func),
        ]
        return url_list

    def func(self,request):
        return HttpResponse("我是额外添加的路径哦....")
    # 3、
    # show_add_btn=False   #默认是True的，如果不让显示添加按钮可以自定制

    # 4、
    def get_model_form_class(self):
        class MyModelForm(ModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"
                error_messages={
                    "name":{"required":"用户名不能为空"},
                    "email":{"invalid":"邮箱格式不正确"}
                }
        return MyModelForm
    # 5、
    def delete_view(self, request,nid, *args, **kwargs):
        if request.method=="GET":
            return render(request,"stark/delete_view.html",{"quxiao_url":self.get_list_url()})
        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_list_url())
v1.site.register(models.UserInfo,UserInfoConfig)

class RoleConfig(v1.StarkConfig):

    list_display = ["id","name"]
    # list_display = []
    def extra_urls(self):
        url_list =[
            url(r'^aaaa/$',self.func),
        ]
        return url_list

    def func(self,request):
        return HttpResponse("我是额外添加的路径哦....")

    # show_add_btn=False   #默认是True的，如果不让显示添加按钮可以自定制


    def get_model_form_class(self):
        class MyModelForm(ModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"
                error_messages={
                    "name":{"required":"用户名不能为空"},
                }
        return MyModelForm
v1.site.register(models.Role,RoleConfig)
v1.site.register(models.UserType)

class HostConfig(v1.StarkConfig):
    def ip_port(self, obj= None,is_header=False):
        if is_header:  #如果是True就返回的是th的,默认就是True
            return "自定义列"
        return "%s_%s"%(obj.id,obj.port,)  #当是False的时候就返回的是td的
    list_display = ["id","name","ip","port",ip_port]

    # =====扩展一个url路径======
    def extra_urls(self):
        url_list = [
            url(r'^report/$', self.report_view),
        ]
        return url_list
    def report_view(self,request):
        return HttpResponse("<h3>这是我给报表另外添加的一个路径</h3>")
v1.site.register(models.Host,HostConfig)
