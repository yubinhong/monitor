from django.db import models

# Create your models here.
class Items(models.Model):
    name=models.CharField(max_length=50,unique=True)
    key=models.CharField(max_length=100)
    data_type_option=(('float','Float'),('str','Str'),('int','Int'))
    data_type=models.CharField(u"指标数据类型",max_length=50,choices=data_type_option,default='int')
    memo=models.CharField(u"备注",max_length=128,blank=True,null=True)
    def __str__(self):
        return "%s.%s" %(self.name,self.key)
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
        (1,'online'),
        (2,'down'),
        (3,'Unreachable'),
        (4,'Problem'),
    )
    host_alive_check_interval=models.IntegerField(u'主机存活状态检测间隔',default=30)
    status=models.IntegerField(u'状态',choices=status_choices,default=1)
    memo=models.TextField(u'备注',blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=u"主机"
        verbose_name_plural=u"主机"


class MonitorGroup(models.Model):
    name=models.CharField(u"监控组名",max_length=64,unique=True)
    templates=models.ForeignKey("Templates",blank=True)
    memo=models.TextField(u"备注",blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=u"监控组"
        verbose_name_plural = u"监控组"


class CPUInfo(models.Model):
    host=models.ForeignKey("Host")
    user=models.FloatField()
    system=models.FloatField()
    nice=models.FloatField()
    idle=models.FloatField()
    wait=models.FloatField()
    steal=models.FloatField()


class MemoryInfo(models.Model):
    host=models.ForeignKey("Host")
    memoryTotal=models.IntegerField()
    memoryFree=models.IntegerField()
    memoryUse=models.IntegerField()
    memoryShare=models.IntegerField()
    memoryBuffer=models.IntegerField()
    memoryCache=models.IntegerField()
