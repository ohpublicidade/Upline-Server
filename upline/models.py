from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Q

class State(models.Model):
    acronym = models.CharField(max_length=2, verbose_name=_('acronym'))
    name = models.CharField(max_length=255, verbose_name=_('name'))

    class Meta:
        verbose_name = _('state')
        verbose_name_plural = _('states')

    def __unicode__(self):
        return self.acronym
    
class City(models.Model):
    state = models.ForeignKey(State, verbose_name=_('state'))
    name = models.CharField(max_length=255, verbose_name=_('name'))

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('citys')

    def __unicode__(self):
        return self.state.acronym+' - '+self.name

    def to_json(self):
        return {'state':self.state.acronym,'name':self.name,'id':self.id}

class PostalCode(models.Model):
    city = models.ForeignKey(City,verbose_name=_('city'))
    street = models.CharField(max_length=255,verbose_name=_('street'))
    neighborhood = models.CharField(max_length=255,verbose_name=_('neighborhood'))
    postal_code = models.CharField(max_length=255,verbose_name=_('postal_code'))
    street_type = models.CharField(max_length=255,verbose_name=_('street_type'))
    approved = models.BooleanField(default=False,verbose_name=_('approved'))

    class Meta:
        verbose_name = _('postal code')
        verbose_name_plural = _('postal codes')

    def __unicode__(self):
        return self.postal_code

    def to_json(self):
        return { 'city':self.city.name,'state':self.city.state.acronym,'street':'%s %s'%(self.street_type,self.street),'zip_code':self.zip_code, 'neighborhood':self.neighborhood }


class Training(models.Model):
    name = models.CharField(max_length=255,verbose_name=_('name'))
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=_('create_time'))
    update_time = models.DateTimeField(auto_now=True,verbose_name=_('update_time'))

    class Meta:
        verbose_name = _("training")
        verbose_name_plural = _("trainings")

    def __unicode__(self):
        return self.name

class TrainingStep(models.Model):
    training = models.ForeignKey(Training,related_name='training_steps',verbose_name=_('training'))
    title = models.CharField(max_length=255,verbose_name=_('title'))
    media = models.FileField(upload_to="training_steps",blank=True, null=True,verbose_name=_('media'))
    step = models.IntegerField(verbose_name=_('step'))
    description = models.TextField(blank=True, null=True,verbose_name=_('description'))
    need_answer = models.BooleanField(default=False,verbose_name=_('need_answer'))
    answer_type = models.IntegerField(verbose_name=_('answer_type'))
    meetings_per_week = models.IntegerField(verbose_name=_('meetings_per_week'))
    weeks = models.IntegerField(verbose_name=_('weeks'))
    nr_contacts = models.IntegerField(verbose_name=_('nr_contacts'))
    day_1_notification_description = models.TextField(blank=True, null=True,verbose_name=_('day_1_notification_description'))
    day_2_notification_description = models.TextField(blank=True, null=True,verbose_name=_('day_2_notification_description'))
    day_3_notification_description = models.TextField(blank=True, null=True,verbose_name=_('day_3_notification_description'))
    day_4_notification_description = models.TextField(blank=True, null=True,verbose_name=_('day_4_notification_description'))
    day_5_notification_description = models.TextField(blank=True, null=True,verbose_name=_('day_5_notification_description'))
    day_6_notification_description = models.TextField(blank=True, null=True,verbose_name=_('day_6_notification_description'))
    day_7_notification_description = models.TextField(blank=True, null=True,verbose_name=_('day_7_notification_description'))
    day_14_notification_description = models.TextField(blank=True, null=True,verbose_name=_('day_14_notification_description'))
    day_28_notification_description = models.TextField(blank=True, null=True,verbose_name=_('day_28_notification_description'))
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=_('create_time'))
    update_time = models.DateTimeField(auto_now=True,verbose_name=_('update_time'))

    class Meta:
        verbose_name = _("training step")
        verbose_name_plural = _("training steps")

    def __unicode__(self):
        return self.title

class Level(models.Model):
    title = models.CharField(unique=True, max_length=255,verbose_name=_('title'))
    image = models.ImageField(null=True,upload_to="levels",verbose_name=_('image'))
    description = models.TextField(null=True,verbose_name=_('description'))
    gift = models.TextField(null=True,verbose_name=_('gift'))
    points_range_from = models.IntegerField(verbose_name=_('points_range_from'))
    points_range_to = models.IntegerField(verbose_name=_('points_range_to'))
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=_('create_time'))
    update_time = models.DateTimeField(auto_now=True,verbose_name=_('update_time'))

    class Meta:
        verbose_name = _("level")
        verbose_name_plural = _("levels")

    def __unicode__(self):
        return self.title

class Member(MPTTModel):
    user = models.OneToOneField(User,verbose_name=_('user'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='downlines', db_index=True,verbose_name=_('parent'))
    external_id = models.IntegerField(unique=True, blank=True, null=True,verbose_name=_('external_id'))
    name = models.CharField(max_length=255,verbose_name=_('name'))
    quickblox_id = models.CharField(max_length=255,null=True,verbose_name=_('quickblox_id'))
    quickblox_login = models.CharField(max_length=255,null=True,verbose_name=_('quickblox_login'))
    quickblox_password = models.CharField(max_length=255,null=True,verbose_name=_('quickblox_password'))
    points = models.IntegerField(default=0,verbose_name=_('points'))
    avatar = models.ImageField(upload_to='members', blank=True, null=True,verbose_name=_('avatar'))
    phone = models.CharField(max_length=45, blank=True, null=True,verbose_name=_('phone'))
    gender = models.IntegerField(choices=((0,"Masculino"),(1,'Feminino')),verbose_name=_('gender'))
    postal_code = models.CharField(max_length=255,verbose_name=_('postal_code'))
    city = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('city'))
    state = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('state'))
    address = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('address'))
    dream1 = models.ImageField(upload_to="dreams",blank=True, null=True,default=None,verbose_name=_('dream1'))
    dream2 = models.ImageField(upload_to="dreams",blank=True, null=True,default=None,verbose_name=_('dream2'))
    status = models.TextField(blank=True, null=True,verbose_name=_('status'))
    birthday = models.DateField(null=True,verbose_name=_('birthday'))
    level = models.ForeignKey(Level,null=True,verbose_name=_('level'))
    outpooring = models.IntegerField(default=0,verbose_name=_('outpooring'))
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=_('create_time'))
    update_time = models.DateTimeField(auto_now=True,verbose_name=_('update_time'))

    all_items = []

    def get_binary_outpouring_right(self,level,initial_parent):
        ret = {'obj':self,'left':None,'right':None}
        parent_child = Member.objects.filter(parent=initial_parent,mptt_level__lte=level,outpooring=1).exclude(id__in=initial_parent.all_items).order_by('id').first()
        if parent_child:
            children = Member.objects.filter(parent=self,mptt_level__lte=level,id__lte=parent_child.id).order_by('id')[:2]
        else:
            children = Member.objects.filter(parent=self,mptt_level__lte=level).order_by('id')[:2]

        for child in children:
            initial_parent.all_items.append(child.id)

        if len(children) < 2 and parent_child:
            initial_parent.all_items.append(parent_child.id)
        
        if ret['left'] == None and len(children) > 0:
            ret['left'] = children[0].get_binary(level,initial_parent)

        if len(children) == 2:
            ret['right'] = children[1].get_binary_outpouring_right(level,initial_parent)
        elif parent_child:
            ret['right'] = parent_child.get_binary_outpouring_right(level,initial_parent)

        return ret

    def get_binary_outpouring_left(self,level,initial_parent):
        ret = {'obj':self,'left':None,'right':None}
        parent_child = Member.objects.filter(parent=initial_parent,mptt_level__lte=level,outpooring=0).exclude(id__in=initial_parent.all_items).order_by('id').first()
        print str(self) +' - '+str(parent_child)+' - '+str(initial_parent.all_items)
        if parent_child:
            children = Member.objects.filter(parent=self,mptt_level__lte=level,id__lte=parent_child.id).order_by('id')[:2]
        else:
            children = Member.objects.filter(parent=self,mptt_level__lte=level).order_by('id')[:2]

        for child in children:
            initial_parent.all_items.append(child.id)

        if len(children) < 2 and parent_child:
            initial_parent.all_items.append(parent_child.id)
        
        if ret['left'] == None and len(children) > 0:
            ret['left'] = children[0].get_binary_outpouring_left(level,initial_parent)
        elif parent_child:
            ret['left'] = parent_child.get_binary_outpouring_left(level,initial_parent)

        if len(children) == 2:
            ret['right'] = children[1].get_binary(level,initial_parent)

        return ret

    def get_binary(self,level,initial_parent):
        if self == initial_parent:
            self.all_items = []
        
        ret = {'obj':self,'left':None,'right':None}

        children = Member.objects.filter(parent=self,mptt_level__lte=level).order_by('id')[:2]
        
        for child in children:
            initial_parent.all_items.append(child.id)
        
        if ret['left'] == None and len(children) > 0:
            if self == initial_parent:
                ret['left'] = children[0].get_binary_outpouring_left(level,initial_parent)
            else:
                ret['left'] = children[0].get_binary(level,initial_parent)

        if len(children) == 2:
            if self == initial_parent:
                ret['right'] = children[1].get_binary_outpouring_right(level,initial_parent)
            else:
                ret['right'] = children[1].get_binary(level,initial_parent)

        return ret

    class Meta:
        verbose_name = _("member")
        verbose_name_plural = _("members")

    class MPTTMeta:
        order_insertion_by = ['name']
        level_attr = 'mptt_level'

    def __unicode__(self):
        return self.name

class MemberTraingStep(models.Model):
    member = models.ForeignKey(Member,related_name='training_steps',verbose_name=_('member'))
    training_step = models.ForeignKey(TrainingStep,related_name='members',verbose_name=_('training_step'))
    answer = models.TextField(verbose_name=_('answer'))

    class Meta:
        verbose_name = _("member traing step")
        verbose_name_plural = _("member traing steps")

    def __unicode__(self):
        return self.member.name+' - '+self.training_step.title

class Team(models.Model):
    owner = models.ForeignKey(Member,related_name="team_owner",verbose_name=_('owner'))
    member = models.ForeignKey(Member,related_name="team_member",verbose_name=_('member'))
    position = models.IntegerField(verbose_name=_('position'))

    class Meta:
        verbose_name = _("member team")
        verbose_name_plural = _("member teams")

    def __unicode__(self):
        return self.owner.name +" - "+ self.member.name

class Contact(models.Model):
    owner = models.ForeignKey(Member,related_name="contact_owner",verbose_name=_('owner'))
    member = models.ForeignKey(Member,related_name="contact_member", blank=True, null=True,verbose_name=_('member'))
    avatar = models.ImageField(upload_to='contacts', blank=True, null=True,verbose_name=_('avatar'))
    contact_category = models.IntegerField(choices=((0,'Contato'),(1,'Cliente')),verbose_name=_('contact_category'))
    gender = models.IntegerField(choices=((0,"Masculino"),(1,'Feminino')),verbose_name=_('gender'))
    name = models.CharField(max_length=255,verbose_name=_('name'))
    email = models.EmailField(max_length=255,null=True,verbose_name=_('email'))
    phone = models.CharField(max_length=45, blank=True, null=True,verbose_name=_('phone'))
    cellphone = models.CharField(max_length=45, blank=True, null=True,verbose_name=_('cellphone'))
    birthday = models.DateField(null=True,verbose_name=_('birthday'))
    cpf = models.CharField(max_length=45, blank=True, null=True,verbose_name=_('cpf'))
    rg = models.CharField(max_length=45, blank=True, null=True,verbose_name=_('rg'))
    postal_code = models.CharField(max_length=255,verbose_name=_('postal_code'))
    region = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('region'))
    city = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('city'))
    state = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('state'))
    address = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('address'))
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=_('create_time'))
    update_time = models.DateTimeField(auto_now=True,verbose_name=_('update_time'))

    class Meta:
        verbose_name = _("contact")
        verbose_name_plural = _("contacts")

    def __unicode__(self):
        return self.name

class Goal(models.Model):
    member = models.ForeignKey(Member,verbose_name=_('member'))
    level = models.ForeignKey(Level,verbose_name=_('level'))
    date = models.DateTimeField(verbose_name=_('date'))
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=_('create_time'))
    update_time = models.DateTimeField(auto_now=True,verbose_name=_('update_time'))

    class Meta:
        verbose_name = _("goal")
        verbose_name_plural = _("goals")

    def __unicode__(self):
        return self.level.title+" - "+self.member.name

class LogMemberLogin(models.Model):
    member = models.ForeignKey(Member,verbose_name=_('member'))
    ipv4_address = models.CharField(max_length=15, blank=True, null=True,verbose_name=_('ipv4_address'))
    ipv6_address = models.CharField(max_length=40, blank=True, null=True,verbose_name=_('ipv6_address'))
    agent = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('agent'))
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=_('create_time'))
    update_time = models.DateTimeField(auto_now=True,verbose_name=_('update_time'))

    class Meta:
        verbose_name = _("log member login")
        verbose_name_plural = _("log member logins")

    def __unicode__(self):
        return self.member.name

    
class Product(models.Model):
    name = models.CharField(max_length=255,verbose_name=_('name'))
    active = models.BooleanField(default=True,verbose_name=_('active'))
    points = models.IntegerField(default=0,verbose_name=_('points'))
    table_value = models.DecimalField(max_digits=11, decimal_places=2,verbose_name=_('table_value'))
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=_('create_time'))
    update_time = models.DateTimeField(auto_now=True,verbose_name=_('update_time'))
    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __unicode__(self):
        return self.name

class Sale(models.Model):
    member = models.ForeignKey(Member,verbose_name=_('member'))
    client = models.ForeignKey(Contact,verbose_name=_('client'))
    active = models.BooleanField(default=True,verbose_name=_('active'))
    total = models.DecimalField(max_digits=11, decimal_places=2,default="0.00",verbose_name=_('total'))
    points = models.IntegerField(default=0,verbose_name=_('points'))
    paid = models.BooleanField(default=False,verbose_name=_('paid'))
    sent = models.BooleanField(default=False,verbose_name=_('sent'))
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=_('create_time'))
    update_time = models.DateTimeField(auto_now=True,verbose_name=_('update_time'))
    send_time = models.DateTimeField(null=True,verbose_name=_('send_time'))

    class Meta:
        verbose_name = _("sale")
        verbose_name_plural = _("sales")

    def __unicode__(self):
        return str(self.id)

class SaleItem(models.Model):
    product = models.ForeignKey(Product,verbose_name=_('product'))
    sale = models.ForeignKey(Sale,related_name='sale_items',verbose_name=_('sale'))
    quantity = models.IntegerField(default=0,verbose_name=_('quantity'))
    total = models.DecimalField(max_digits=11, decimal_places=2,default="0.00",verbose_name=_('total'))
    notificate_at = models.DateField(verbose_name=_('notificate_at'))
    notified = models.BooleanField(default=False,verbose_name=_('notified'))
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=_('create_time'))
    update_time = models.DateTimeField(auto_now=True,verbose_name=_('update_time'))
    class Meta:
        verbose_name = _("sale item")
        verbose_name_plural = _("sale items")

    def __unicode__(self):
        return str(self.id)
    
class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts',verbose_name=_('user'))
    title = models.CharField(max_length=255,verbose_name=_('title'))
    level = models.ForeignKey(Level,verbose_name=_('level'))
    content = models.TextField(null=True,blank=True,default=None,verbose_name=_('content'))
    media = models.FileField(upload_to="posts",null=True,blank=True,default=None,verbose_name=_('media'))
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=_('create_time'))
    update_time = models.DateTimeField(auto_now=True,verbose_name=_('update_time'))

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __unicode__(self):
        return self.title
    
class Calendar(models.Model):
    public = models.BooleanField(default=False,verbose_name=_('public'))
    user = models.ForeignKey(User,null=True,verbose_name=_('user'))
    name = models.CharField(max_length=255,verbose_name=_('name'))

    class Meta:
        verbose_name = _("calendar")
        verbose_name_plural = _("calendars")

    def __unicode__(self):
        return self.name
    
class Event(models.Model):
    owner = models.ForeignKey(User,verbose_name=_('owner'))
    title = models.CharField(max_length=255,verbose_name=_('title'))
    all_day = models.BooleanField(default=False,verbose_name=_('all_day'))
    begin_time = models.DateTimeField(null=True,verbose_name=_('begin_time'))
    end_time = models.DateTimeField(null=True,verbose_name=_('end_time'))
    invited = models.ManyToManyField(Contact,blank=True,verbose_name=_('invited'))
    members = models.ManyToManyField(Member,blank=True,verbose_name=_('members'))
    calendar = models.ForeignKey(Calendar,related_name='events',verbose_name=_('calendar'))
    note = models.TextField(null=True,blank=True,verbose_name=_('note'))

    postal_code = models.ForeignKey(PostalCode,null=True,blank=True,default=None,verbose_name=_('postal_code'))
    number = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('number'))
    complement = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('complement'))
    lat = models.FloatField(null=True,blank=True,default=None,verbose_name=_('lat'))
    lng = models.FloatField(null=True,blank=True,default=None,verbose_name=_('lng'))

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __unicode__(self):
        return self.title

class MediaCategory(models.Model):
    media_type = models.IntegerField(choices=((0,'Imagem'),(1,'Audio'),(2,'Video')),verbose_name=_('media_type'))
    name = models.CharField(max_length=255,verbose_name=_('name'))
    class Meta:
        verbose_name = _("media category")
        verbose_name_plural = _("media categorys")

    def __unicode__(self):
        return self.name

class Media(models.Model):
    media_category = models.ForeignKey(MediaCategory,related_name='medias',verbose_name=_('media_category'))
    name = models.CharField(max_length=255,verbose_name=_('name'))
    media_file = models.FileField(upload_to="multimidida",verbose_name=_('media_file'))
    
    class Meta:
        verbose_name = _("media")
        verbose_name_plural = _("medias")

    def __unicode__(self):
        return self.name
    

