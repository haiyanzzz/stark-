#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.conf.urls import url
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from django.forms import fields
from app01 import models
class StarkConfig(object):
    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
    list_display = []
    # =================url相关，reverse反向解析=============
    def get_change_url(self,nid):
        name = "stark:%s_%s_change"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        edit_url = reverse(name,args=(nid,))  #反向解析只要找到他的name属性，就会找到他对应的路径
        return edit_url

    def get_add_url(self):
        name = "stark:%s_%s_add" % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        edit_url = reverse(name)
        return edit_url

    def get_delete_url(self, nid):
        name = "stark:%s_%s_delete" % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        edit_url = reverse(name,args=(nid,))
        return edit_url

    def get_list_url(self):
        name = "stark:%s_%s_changelist" % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        edit_url = reverse(name)
        return edit_url

    # ===============吧删除，编辑，复选框设置默认按钮==================

    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return "选择"
        return mark_safe("<input type='checkbox' name='zzzz' value='%s'/>"%obj.id)

    def edit(self,obj=None,is_header=False):
        if is_header:
            return "操作"
        return mark_safe("<a href='%s'>编辑</a>"%(self.get_change_url(obj.id),))

    def delete(self,obj=None,is_header=False):
        if is_header:
            return "删除"
        #动态跳转路径，反向解析，因为每次都要用到，我们可以吧它封装到一个函数
        return mark_safe("<a href='%s'>删除</a>"%self.get_delete_url(obj.id))

    #做默认的删除和编辑。对这个方法重写的时候可以吧权限管理加进去，
    # 当它都什么权限的时候显示什么按钮。
    def get_list_display(self):
        data = []
        if self.list_display:
            data.extend(self.list_display) #在新的列表里面吧list_display扩展进来
            data.append(StarkConfig.edit)  #因为是默认的，直接在类里面去调用edit
            data.append(StarkConfig.delete)
            data.insert(0,StarkConfig.checkbox)
        return data

    show_add_btn = True

    # ======这个方法可自定制（如果把show_add_btn设置为False就不会显示添加按钮）=====
    def get_show_add_btn(self):
        return self.show_add_btn

    # =================请求处理的视图================
    def change_list_views(self,request,*args,**kwargs):
        data_list = self.model_class.objects.all()
        def inner():
            '''展示th的信息'''
            for field_name in self.get_list_display():
                if isinstance(field_name,str):
                    verbose_name = self.model_class._meta.get_field(field_name).verbose_name
                else:
                    verbose_name = field_name(self,is_header=True)
                # head_list.append(verbose_name)
                yield {"head_list":verbose_name}

        '''展示td的信息'''
        def inner2():
            # [["id","name"],["id","name"],["id","name"],]
            # new_data_list = []
            for row in data_list:
                temp = []
                for field_name in self.get_list_display():
                    if isinstance(field_name,str):  #判断field_name对象是不是字符串
                        #如果是字符串类型的就是用getattr的方式，因为对象不能.字符串
                        val = getattr(row,field_name)   #row."id"
                    else:
                        val = field_name(self,row)
                    temp.append(val)
                yield temp
                # new_data_list.append(temp)

        '''如果list_display为空的时候显示对象'''
        if not self.list_display:
            new_data_list=[]
            for item in data_list:
                temp = []
                temp.append(item)
                new_data_list.append(temp)
        return render(request, "stark/change_list_views.html", {"head_list":inner(),"data_list":inner2(),"add_url":self.get_add_url(),"show_add_btn":self.get_show_add_btn()})

    model_form_class=None
    def get_model_form_class(self):
        if self.model_form_class:   #如果自己定制了就用自己的，在这就什么也不返回了，如果没有自己定义就返回默认的这个Form
            return self.model_form_class
        # 方式一定义ModelForm
        # class TestModelForm(ModelForm):
        #     class Meta:
        #         model = self.model_class
        #         fields = "__all__"
        # return TestModelForm
        # 方式二定义
        Meta = type("Meta", (object,), {"model": self.model_class, "fields": "__all__"})
        TestModelForm = type("TestModelForm", (ModelForm,), {"Meta": Meta})
        return TestModelForm
    def add_views(self,request,*args,**kwargs):
        model_form_class = self.get_model_form_class()
        if request.method=="GET":
            form = model_form_class()
            return render(request,"stark/add_view.html",{"form":form})
        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            else:
                return render(request, "stark/add_view.html", {"form": form})

    def delete_view(self, request,nid, *args, **kwargs):
        self.model_class.objects.filter(pk=nid).delete()
        return redirect(self.get_list_url())

    def change_views(self, request,nid, *args, **kwargs):
        model_form_class = self.get_model_form_class()
        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.get_list_url())
        if request.method == "GET":
            form = model_form_class(instance=obj)
            return render(request, "stark/edit_view.html", {"form": form})
        else:
            form = model_form_class(data=request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            else:
                return render(request, "stark/edit_view.html", {"form": form})

    # =============路由系统，对应相应的视图函数=====================
    def get_urls(self):
        app_model_name = (self.model_class._meta.app_label,self.model_class._meta.model_name)
        all_url = [
            url(r'^$', self.change_list_views,name="%s_%s_changelist"%app_model_name),
            url(r'^add/$', self.add_views,name="%s_%s_add"%app_model_name),
            url(r'^(\d+)/delete/$', self.delete_view,name="%s_%s_delete"%app_model_name),
            url(r'^(\d+)/change/$', self.change_views,name="%s_%s_change"%app_model_name),
        ]
        all_url.extend(self.extra_urls())
        return all_url

    # ===========额外扩展url(用户可以进行随意扩展)==========
    def extra_urls(self):
        return []

    @property
    def urls(self):
        return self.get_urls()
class StarkSite(object):
    def __init__(self):
        self._registry ={}  #放置处理请求对应关系
        '''
        _registry = {
					models.Role: StarkConfig(models.Role,v1.site),
					models.UserInfo: StarkConfig(models.UserInfo,v1.site)
					models.UserType: StarkConfig(models.UserType,v1.site)
					models.Article: StarkConfig(models.Article,v1.site)
				}
		'''
    def register(self,model_class,stark_config_class=None):
        if not stark_config_class:
            '''stark_config_class是类对象，如果没有这个类就重新赋值，去执行StarkConfig'''
            stark_config_class = StarkConfig
        self._registry[model_class] = stark_config_class(model_class,self)
        #如果用户自己传进去类了，就用自己的，自己的需要继承StarkConfig。如果自己没有就找基类的，自己有就用自己的

    def get_urls(self):
        url_list = []
        for model_calss,stark_config_obj in self._registry.items():
            app_name = model_calss._meta.app_label#应用名称
            model_name = model_calss._meta.model_name#表的名称
            cur_url = url(r'^{0}/{1}/'.format(app_name,model_name),(stark_config_obj.urls,None,None))
            #这是的stark_config_obj是上面StarkConfig的实例对象。stark_config_obj.urls就会去找上面类的urls
            url_list.append(cur_url)
        return url_list
    @property #吧方法当属性来用
    def urls(self):
        return (self.get_urls(),None,'stark')  #第三个参数是namesapce
site = StarkSite()   #实例化
