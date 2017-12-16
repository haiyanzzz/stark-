from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=32,verbose_name="用户名")
    email = models.EmailField(max_length=32,verbose_name="邮箱")
    ut = models.ForeignKey(to="UserType",verbose_name="所属用户")

    class Meta:
        verbose_name_plural= "用户信息表"
    def __str__(self):
        return self.name

class UserType(models.Model):
    name = models.CharField(max_length=32,verbose_name="用户类型")

    class Meta:
        verbose_name_plural = "用户类型表"

    def __str__(self):
        return self.name
class Role(models.Model):
    name = models.CharField(max_length=32,verbose_name="角色名称")

    class Meta:
        verbose_name_plural = "角色表"

    def __str__(self):
        return self.name

class Host(models.Model):
    name = models.CharField(max_length=32,verbose_name="主机名称")
    ip = models.GenericIPAddressField(verbose_name="IP",protocol='ipv4')
    port = models.IntegerField(verbose_name="端口")
