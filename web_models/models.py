from django.db import models

# Create your models here.
class Items(models.Model):
    name=models.CharField(max_length=50,unique=True)
    key=models.CharField(max_length=100,help_text="key的名称要与资源表中（如：CPUInfo）的字段对应")
    #key的名称要与资源表中（如：CPUInfo）的字段对应
    data_type_option=(('float','Float'),('str','Str'),('int','Int'))
    data_type=models.CharField(u"指标数据类型",max_length=50,choices=data_type_option,default='int')
    memo=models.CharField(u"备注",max_length=128,blank=True,null=True)
    service=models.ForeignKey("ServiceType",verbose_name=u"属于")
    def __str__(self):
        return "%s.%s" %(self.service.name,self.key)
    class Meta:
        verbose_name=u"监控指标"
        verbose_name_plural=u"监控指标"


class Services(models.Model):
    monitor_type_list=(('agent','Agent'),('snmp','SNMP'))
    monitor_type=models.CharField(max_length=50,choices=monitor_type_list)
    name=models.CharField(u"服务名称",max_length=50,unique=True)
    service_type=models.ForeignKey("ServiceType",verbose_name=u"服务类型")
    #plugin=models.CharField(u"插件名",max_length=100)
    interval=models.IntegerField(u"监控间隔",default=30)
    #items=models.ForeignKey('Items',verbose_name=u"指标列表",blank=True)
    #trigger=models.ManyToManyField('Trigger',verbose_name=u"关联触发器",blank=True)
    memo=models.CharField(u"备注",max_length=128,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=u"服务"
        verbose_name_plural=u"服务"


class ServiceType(models.Model):
    name=models.CharField(u"类型名称",max_length=50,unique=True)
    plugin = models.CharField(u"插件名", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=u"服务类型"
        verbose_name_plural=u"服务类型"


class Templates(models.Model):
    name=models.CharField(u"模版名称",max_length=50)
    services=models.ManyToManyField('Services',verbose_name=u"服务列表")
    trigger = models.ManyToManyField('Trigger', verbose_name=u"关联触发器", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=u"配置模版"
        verbose_name_plural = u"配置模版"


class Trigger(models.Model):
    name=models.CharField(u"触发器名称",max_length=64)
    service=models.ForeignKey("ServiceType",verbose_name=u"关联服务类型")
    serverity_choices=(
        ('1','unknow'),
        ('2','warning'),
        ('3','error'),
        ('4','critical'),
    )
    item=models.ForeignKey('Items',verbose_name=u"关联监控指标")
    serverity=models.CharField(u"告警级别",choices=serverity_choices,max_length=64)
    count=models.IntegerField(u"失败次数",default=4,help_text="失败多少次告警")
    operator_type_choices=(('eq','='),('lt','<'),('gt','>'))
    operator_type=models.CharField(u"运算符",choices=operator_type_choices,max_length=64)
    data_calc_type_choices=(
        ('avg','Average'),
        ('max','Max'),
        ('hit','Hit'),
        ('last','Last'),
    )
    data_calc_func=models.CharField(u"数据处理方式",choices=data_calc_type_choices,max_length=64)
    threshold=models.IntegerField(u"阀值")

    def __str__(self):
        return "%s.%s.%s.%s" % (self.item,self.data_calc_func,self.operator_type,self.threshold)

    class Meta:
        verbose_name=u"触发器"
        verbose_name_plural = u"触发器"


class HostGroup(models.Model):
    name=models.CharField(u"主机组名",max_length=64,unique=True)
    memo=models.TextField(u"备注",blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=u"主机组"
        verbose_name_plural = u"主机组"


class Host(models.Model):
    name=models.CharField(u"主机名",max_length=64,unique=True)
    ip_addr=models.GenericIPAddressField(u"IP地址",unique=True)
    host_groups=models.ManyToManyField("HostGroup",verbose_name=u"所属主机组",blank=True)
    monitor_groups = models.ForeignKey("MonitorGroup", verbose_name=u"所属监控组", blank=True)
    status_choices=(
        ('online','online'),
        ('down','down'),
        ('Unreachable','Unreachable'),
        ('Problem','Problem'),
    )
    host_alive_check_interval=models.IntegerField(u'主机存活状态检测间隔',default=30)
    status=models.CharField(u'状态',max_length=20,choices=status_choices,default='online')
    memo=models.TextField(u'备注',blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=u"主机"
        verbose_name_plural=u"主机"


class MonitorGroup(models.Model):
    name=models.CharField(u"监控组名",max_length=64,unique=True)
    templates=models.ForeignKey("Templates",blank=True,verbose_name=u"关联模版")
    user = models.OneToOneField("UserInfo", verbose_name=u"监控人")
    memo=models.TextField(u"备注",blank=True,null=True)
    appkey=models.CharField(u"应用ID",max_length=64,unique=True)#这是外部告警用到的appkey

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=u"监控组"
        verbose_name_plural = u"监控组"


class CPUInfo(models.Model):
    host = models.ForeignKey("Host")
    user = models.FloatField()
    system = models.FloatField()
    nice = models.FloatField()
    idle = models.FloatField()
    iowait = models.FloatField()
    steal = models.FloatField()
    create_date=models.FloatField()


class MemoryInfo(models.Model):
    host=models.ForeignKey("Host")
    MemTotal=models.IntegerField()
    MemFree=models.IntegerField()
    MemUsage=models.IntegerField()
    MemUsage_p=models.IntegerField()
    Buffers=models.IntegerField()
    Cached=models.IntegerField()
    create_date = models.FloatField()


class UserInfo(models.Model):
    name=models.CharField(u"用户名",max_length=50)
    mobile=models.CharField(u"手机",max_length=12,unique=True)
    email=models.EmailField(u"邮箱",max_length=50,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=u"用户信息"
        verbose_name_plural=u"用户信息"


class Admin(models.Model):
    user=models.OneToOneField(UserInfo,verbose_name=u"关联用户")
    username=models.CharField(u"登录名",unique=True,max_length=50)
    password=models.CharField(u"密码",max_length=16)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name=u"登录帐号"
        verbose_name_plural=u"登录帐号"

#记录告警信息
class Alert(models.Model):
    hostname=models.CharField(max_length=64)
    trigger=models.ForeignKey("Trigger")
    fail_count=models.IntegerField()
    message=models.CharField(max_length=64,default='',blank=True,null=True)
    alert_time=models.DateTimeField(auto_now_add=True)
    latest_time=models.DateTimeField(auto_now=True)

#记录历史数据
class History(models.Model):
    host=models.ForeignKey('Host')
    service=models.ForeignKey('ServiceType')
    key=models.CharField(max_length=30)
    value=models.CharField(max_length=30)
    create_date=models.FloatField()


#图形配置
class Graph(models.Model):
    host=models.ForeignKey('Host',verbose_name=u'主机')
    service = models.ForeignKey('ServiceType',verbose_name=u'服务类型')
    item=models.ManyToManyField('Items',verbose_name=u'监控指标')

    def __str__(self):
        return "%s的%s" % (self.host.name,self.service.name)

    class Meta:
        verbose_name = u"图形配置"
        verbose_name_plural = u"图形配置"



