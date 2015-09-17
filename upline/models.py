from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Q
from rq import Queue
from worker import conn
from utils import convert_audio, convert_video
from upline.quickblox import create_user
from Crypto.Cipher import AES
import base64, uuid
from s3direct.fields import S3DirectField
from push_notifications.models import APNSDevice, GCMDevice

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

# class Audio(models.Model):
#     audio = models.FileField(upload_to='audios')
#     converted = models.BooleanField(default=False)

#     class Meta:
#         verbose_name = "Audio"
#         verbose_name_plural = "Audios"

#     def __unicode__(self):
#         return self.audio.url

#     def save(self, *args, **kwargs):
#         super(Audio, self).save(*args, **kwargs)
#         if self.audio.url.rsplit( ".", 1 )[1] != "mp3":
#             q = Queue(connection=conn)
#             result = q.enqueue(convert_audio, self)
#         # print 'ffmpeg -i '+self.audio.path+' '+self.audio.path.rsplit( ".", 1 )[ 0 ]+'.mp3'
        

# class Video(models.Model):
#     video = models.FileField(upload_to='videos')
#     thumbnail = models.ImageField(upload_to='videos',null=True,blank=True,default=None)
#     converted = models.BooleanField(default=False)

#     class Meta:
#         verbose_name = "Video"
#         verbose_name_plural = "Videos"

#     def __unicode__(self):
#         return self.video.url

#     def save(self, *args, **kwargs):
#         super(Video, self).save(*args, **kwargs)
#         q = Queue(connection=conn)
#         result = q.enqueue(convert_video, self)

class TrainingStep(models.Model):
    training = models.ForeignKey(Training,related_name='training_steps',verbose_name=_('training'))
    title = models.CharField(max_length=255,verbose_name=_('title'))
    media = S3DirectField(dest='training_steps', null=True)
    thumbnail = models.ImageField(upload_to="thumbnails",blank=True, null=True,verbose_name=_('thumbnail'))
    step = models.IntegerField(verbose_name=_('step'))
    description = models.TextField(blank=True, null=True,verbose_name=_('description'))
    need_answer = models.BooleanField(default=False,verbose_name=_('need_answer'))
    answer_type = models.IntegerField(verbose_name=_('answer_type'),choices=((0,_('text')),(1,_('audio')),(2,_('video')),(3,_('list')),(4,_('meeting'))))
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
    group = models.ForeignKey(Group,verbose_name=_('group'),null=True)
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
    member_uid = models.UUIDField(unique=True, null=True, editable=False)
    user = models.OneToOneField(User,verbose_name=_('user'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='downlines', db_index=True,verbose_name=_('parent'))
    external_id = models.IntegerField(unique=True, blank=True, null=True,verbose_name=_('external_id'))
    name = models.CharField(max_length=255,verbose_name=_('name'))
    quickblox_id = models.CharField(max_length=255,null=True,verbose_name=_('quickblox_id'),editable=False)
    quickblox_password = models.CharField(max_length=255,null=True,verbose_name=_('quickblox_password'),editable=False)
    points = models.IntegerField(default=0,verbose_name=_('points'))
    avatar = models.ImageField(upload_to='members', blank=True, null=True,verbose_name=_('avatar'))
    phone = models.CharField(max_length=45, blank=True, null=True,verbose_name=_('phone'))
    gender = models.IntegerField(choices=((0,"Masculino"),(1,'Feminino')),verbose_name=_('gender'))
    postal_code = models.CharField(max_length=255,verbose_name=_('postal_code'))
    city = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('city'))
    state = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('state'))
    address = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('address'))
    address_number = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('address_number'))
    dream1 = models.ImageField(upload_to="dreams",blank=True, null=True,default=None,verbose_name=_('dream1'))
    dream2 = models.ImageField(upload_to="dreams",blank=True, null=True,default=None,verbose_name=_('dream2'))
    status = models.CharField(blank=True, null=True,verbose_name=_('status'),max_length=255)
    birthday = models.DateField(null=True,verbose_name=_('birthday'))
    level = models.ForeignKey(Level,null=True,verbose_name=_('level'),editable=False)
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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.member_uid = str(uuid.uuid4())
            self.quickblox_password = User.objects.make_random_password()
            self = create_user(self)
            self.encrypt_quickblox_password()
        super(Member, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("member")
        verbose_name_plural = _("members")

    class MPTTMeta:
        order_insertion_by = ['name']
        level_attr = 'mptt_level'

    def __unicode__(self):
        return self.name

    def encrypt_quickblox_password(self):
        key = "%s%s%s"%(self.user.username,str(self.quickblox_id),self.member_uid)
        enc_secret = AES.new(key[:32])
        tag_string = (str(self.quickblox_password) +
                      (AES.block_size -
                       len(str(self.quickblox_password)) % AES.block_size) * "\0")
        cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))
        self.quickblox_password = cipher_text

    def decrypted_quickblox_password(self):
        key = "%s%s%s"%(self.user.username,str(self.quickblox_id),self.member_uid)
        dec_secret = AES.new(key[:32])
        raw_decrypted = dec_secret.decrypt(base64.b64decode(self.quickblox_password))
        clear_val = raw_decrypted.rstrip("\0")
        return clear_val

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
    owner = models.ForeignKey(Member,related_name="contact_owner",verbose_name=_('upline'))
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
    address_number = models.CharField(max_length=255, blank=True, null=True,verbose_name=_('address_number'))
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
    group = models.ForeignKey(Group,verbose_name=_('group'),null=True)
    content = models.TextField(null=True,blank=True,default=None,verbose_name=_('content'))
    media = S3DirectField(dest='posts', null=True)
    thumbnail = models.ImageField(upload_to="thumbnails",blank=True, null=True,verbose_name=_('thumbnail'))
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
    postal_code = models.CharField(max_length=255,verbose_name=_('postal_code'),null=True,blank=True)
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
    media = S3DirectField(dest='media', null=True)
    thumbnail = models.ImageField(upload_to="thumbnails",blank=True, null=True,verbose_name=_('thumbnail'))
    converted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("media")
        verbose_name_plural = _("medias")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Media, self).save(*args, **kwargs)
        if not converted:
            if self.media_category.media_type == 1:
                q = Queue(connection=conn)
                result = q.enqueue(convert_audio, self)
            elif self.media_category.media_type == 2:
                q = Queue(connection=conn)
                result = q.enqueue(convert_video, self)

class Notification(models.Model):
    level = models.ForeignKey(Group,verbose_name=_('level'))
    message = models.CharField(max_length=255,verbose_name=_('message'))
    sent = models.BooleanField(default=False,editable=False,verbose_name=_('sent'))

    def save(self, *args, **kwargs):
        super(Notification, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __unicode__(self):
        return self.message
    