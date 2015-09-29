 # -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from upline.models import *
from rest_framework import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
import mimetypes, json, base64, uuid

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ("id", 'name')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(read_only=True,many=True)
    class Meta:
        model = User
        fields = ("id",'groups', 'username', 'email')

class UsernameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username')

class LevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Level
        fields = ("id",'title','image','points_range_from','points_range_to')

class TrainingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Training
        fields = ("id",'name',)

class TrainingSetpSerializer(serializers.HyperlinkedModelSerializer):
    training = TrainingSerializer()
    class Meta:
        model = TrainingStep
        fields = ("id",'training','title','media','step','description',)

class UplineSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    level = LevelSerializer(many=False, read_only=True)
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Member
        fields = ("id","member_type","user",'quickblox_id','create_time','external_id','name','points','avatar','phone','gender','postal_code','city','state','address','address_number','dream1','dream2','status','level','answers','birthday')


class DownlineSerializer(serializers.HyperlinkedModelSerializer):
    level = LevelSerializer(many=False, read_only=True)
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Member
        fields = ("id","member_type",'quickblox_id','create_time','external_id','name','points','avatar','phone','gender','postal_code','city','state','address','address_number','dream1','dream2','status','level','answers')


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    level = LevelSerializer(many=False, read_only=True)
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parent = UplineSerializer(many=False, read_only=True)
    downlines = DownlineSerializer(many=True, read_only=True)
    avatar_base64 = serializers.CharField(required=False,allow_blank=True)
    dream1_base64 = serializers.CharField(required=False,allow_blank=True)
    dream2_base64 = serializers.CharField(required=False,allow_blank=True)
    
    class Meta:
        model = Member
        fields = ("id","member_type","user","avatar_base64","dream1_base64","avatar_base64",'quickblox_id','parent','downlines','create_time','external_id','name','points','avatar','phone','gender','postal_code','city','state','address','address_number','dream1','dream2','status','level','answers','birthday')

class MemberRegisterSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.SlugField()
    email = serializers.EmailField()
    grant_type = serializers.CharField(initial="password")
    password = serializers.CharField(style={'input_type': 'password'})
    parent_user = serializers.SlugField()
    avatar_base64 = serializers.CharField(required=False,allow_blank=True)
    dream1_base64 = serializers.CharField(required=False,allow_blank=True)
    dream2_base64 = serializers.CharField(required=False,allow_blank=True)

    def validate_parent_user(self,value):
        members = Member.objects.filter(user__username=value,member_type=0)
        if len(members) != 1:
            raise serializers.ValidationError("Invalid Parent ID")
        return value

    def validate_email(self, value):
        users = User.objects.filter(email=value)
        if len(users) > 0:
            raise serializers.ValidationError("Email already registered")
        return value

    def validate_username(self, value):
        users = User.objects.filter(username=value)
        if len(users) > 0:
            raise serializers.ValidationError("Username already registered")
        return value


    def save(self):
        user = User()
        user.username = self.validated_data['username']
        user.email = self.validated_data['email']
        user.set_password(self.validated_data['password'])
        user.save()
        user.groups.add(Group.objects.get(id=3))
        user.save()

        member = Member()
        if 'avatar_base64' in self.validated_data:
            avatar = self.validated_data.pop('avatar_base64')
            if len(avatar) > 0:
                avatar_base64 = avatar.split(',')[1]
                avatar_mime = avatar.split(';')[0].split(':')[1]
                avatar_extension = avatar_mime.split('/')[1]
                member.avatar = SimpleUploadedFile(name=str(uuid.uuid4())+'.'+avatar_extension, content=base64.b64decode(avatar_base64), content_type=avatar_mime)
        if 'dream1_base64' in self.validated_data:
            dream1 = self.validated_data.pop('dream1_base64')
            if len(dream1) > 0:
                dream1_base64 = dream1.split(',')[1]
                dream1_mime = dream1.split(';')[0].split(':')[1]
                dream1_extension = dream1_mime.split('/')[1]
                self.dream1 = SimpleUploadedFile(name=str(uuid.uuid4())+'.'+dream1_extension, content=base64.b64decode(dream1_base64), content_type=dream1_mime)
        if 'dream2_base64' in self.validated_data:
            dream2 = self.validated_data.pop('dream2_base64')
            if len(dream2) > 0:
                dream2_base64 = dream2.split(',')[1]
                dream2_mime = dream2.split(';')[0].split(':')[1]
                dream2_extension = dream2_mime.split('/')[1]
                self.dream2 = SimpleUploadedFile(name=str(uuid.uuid4())+'.'+dream2_extension, content=base64.b64decode(dream2_base64), content_type=dream2_mime)

        member.parent = Member.objects.get(user__username=self.validated_data['parent_user'])
        member.member_type = 1

        if 'name' in self.validated_data:
            member.name = self.validated_data['name']
        if 'phone' in self.validated_data:
            member.phone = self.validated_data['phone']
        if 'gender' in self.validated_data:
            member.gender = self.validated_data['gender']
        if 'postal_code' in self.validated_data:
            member.postal_code = self.validated_data['postal_code']
        if 'birthday' in self.validated_data:
            member.birthday = self.validated_data['birthday']
        if 'state' in self.validated_data:
            member.state = self.validated_data['state']
        if 'city' in self.validated_data:
            member.city = self.validated_data['city']
        if 'address' in self.validated_data:
            member.address = self.validated_data['address']
        if 'address_number' in self.validated_data:
            member.address_number = self.validated_data['address_number']
        member.user = user
        member.save()

    class Meta:
        model = Member
        fields = ("id","member_type",'avatar_base64',"dream1_base64","dream2_base64",'name','email','grant_type','parent_user','username','password','phone','birthday','gender','postal_code','state','city','address','address_number')

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    level = LevelSerializer(many=False, read_only=True)
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parent = UplineSerializer(many=False, read_only=True)
    downlines = DownlineSerializer(many=True, read_only=True)
    avatar_base64 = serializers.CharField(write_only=True,required=False,allow_blank=True)

    def save(self):
        if 'avatar_base64' in self.validated_data:
            avatar = self.validated_data.pop('avatar_base64')
            if len(avatar) > 0:
                avatar_base64 = avatar.split(',')[1]
                avatar_mime = avatar.split(';')[0].split(':')[1]
                avatar_extension = avatar_mime.split('/')[1]
                self.avatar = SimpleUploadedFile(name=str(uuid.uuid4())+'.'+avatar_extension, content=base64.b64decode(avatar_base64), content_type=avatar_mime)
        super(MemberSerializer, self).save()

    class Meta:
        model = Member
        fields = ("id","member_type","user","avatar_base64",'quickblox_id','parent','downlines','create_time','external_id','name','points','avatar','phone','gender','postal_code','city','state','address','address_number','dream1','dream2','status','level','answers','birthday')

class MemberLoginSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    level = LevelSerializer(many=False, read_only=True)
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parent = UplineSerializer(many=False, read_only=True)
    downlines = DownlineSerializer(many=True, read_only=True)
    class Meta:
        model = Member
        fields = ("id","member_type",'user','member_uid','quickblox_id','quickblox_password','parent','downlines','create_time','external_id','name','points','avatar','phone','gender','postal_code','city','state','address','address_number','dream1','dream2','status','level','birthday','answers')

class ContactSerializer(serializers.HyperlinkedModelSerializer):
    member = MemberSerializer(read_only=True)
    avatar_base64 = serializers.CharField(write_only=True,required=False,allow_blank=True)

    def create(self,validated_data):
        contact = Contact()
        member = Member.objects.get(user=self.context['request'].user)
        contact.owner = member

        if 'avatar_base64' in self.validated_data:
            avatar = validated_data.pop('avatar_base64')
            if len(avatar) > 0:
                avatar_base64 = avatar.split(',')[1]
                avatar_mime = avatar.split(';')[0].split(':')[1]
                avatar_extension = avatar_mime.split('/')[1]
                contact.avatar = SimpleUploadedFile(name=str(uuid.uuid4())+'.'+avatar_extension, content=base64.b64decode(avatar_base64), content_type=avatar_mime)

        
        if 'email' in self.validated_data:
            contact.email = validated_data.pop('email')
        if 'cellphone' in self.validated_data:
            contact.cellphone = validated_data.pop('cellphone')
        if 'birthday' in self.validated_data:
            contact.birthday = validated_data.pop('birthday')
        if 'cpf' in self.validated_data:
            contact.cpf = validated_data.pop('cpf')
        if 'rg' in self.validated_data:
            contact.rg = validated_data.pop('rg')
        if 'region' in self.validated_data:
            contact.region = validated_data.pop('region')
        if 'contact_category' in self.validated_data:
            contact.contact_category = validated_data.pop('contact_category')
        if 'name' in self.validated_data:
            contact.name = validated_data.pop('name')
        if 'phone' in self.validated_data:
            contact.phone = validated_data.pop('phone')
        if 'gender' in self.validated_data:
            contact.gender = validated_data.pop('gender')
        if 'postal_code' in self.validated_data:
            contact.postal_code = validated_data.pop('postal_code')
        if 'city' in self.validated_data:
            contact.city = validated_data.pop('city')
        if 'state' in self.validated_data:
            contact.state = validated_data.pop('state')
        if 'address' in self.validated_data:
            contact.address = validated_data.pop('address')
        contact.save()
        return contact

    class Meta:
        model = Contact
        fields = ("id","avatar_base64","avatar","email","cellphone","birthday","cpf","rg","region",'member','contact_category','name','phone','gender','postal_code','city','state','address')

class ContactDownlineSerializer(serializers.HyperlinkedModelSerializer):
    member = DownlineSerializer(read_only=True)
    class Meta:
        model = Contact
        fields = ("id","avatar","email","cellphone","birthday","cpf","rg","region",'member','contact_category','name','phone','gender','postal_code','city','state','address')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ("id","name","active","points","table_value","create_time")

class SaleItemSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = SaleItem
        fields = ("id","product","quantity","total","notificate_at")

class SaleItemRegisterSerializer(serializers.HyperlinkedModelSerializer):
    sale = serializers.PrimaryKeyRelatedField(many=False, queryset=Sale.objects.all(),write_only=True)
    product = serializers.PrimaryKeyRelatedField(many=False, queryset=Product.objects.all())
    class Meta:
        model = SaleItem
        fields = ("id","product","quantity","notificate_at","sale")

class SaleSerializer(serializers.HyperlinkedModelSerializer):
    client = ContactDownlineSerializer(read_only=True)
    sale_items = SaleItemSerializer(many=True,read_only=True)
    class Meta:
        model = Sale
        fields = ("id","client","sale_items","active","total","points","create_time","paid","sent","send_time")

class SaleRegisterSerializer(serializers.HyperlinkedModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Contact.objects.all(),source="client")
    sale_items = SaleItemRegisterSerializer(many=True)
    class Meta:
        model = Sale
        fields = ("id","client_id","sale_items")

class TrainingStepSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    def get_status(self,training_step):
        members = training_step.members.filter(member__user=self.context['request'].user)
        if len(members) > 0:
            return True
        return False

    def get_answer(self,training_step):
        members = training_step.members.filter(member__user=self.context['request'].user)
        if len(members) > 0:
            return MemberTrainingStepSerializer(members[0]).data
        return None

    class Meta:
        model = TrainingStep
        fields = ('id','status','answer','title','media',"thumbnail","media_type",'step','description','need_answer',"answer_type","meetings_per_week","weeks","nr_contacts")


class MemberTrainingStepSerializer(serializers.HyperlinkedModelSerializer):
    training_step = serializers.PrimaryKeyRelatedField(many=False,queryset=TrainingStep.objects.all())
    media_base64 = serializers.CharField(write_only=True,required=False,allow_blank=True)

    def create(self,validated_data):
        validated_data['member'] = Member.objects.get(user=self.context['request'].user)
        return super(MemberTrainingStepSerializer, self).create(validated_data)

    def save(self):
        print self.validated_data
        if 'media_base64' in self.validated_data:
            media = self.validated_data.pop('media_base64')
            print 'batata'
            if len(media) > 0:
                media_base64 = media.split(',')[1]
                media_mime = media.split(';')[0].split(':')[1]
                media_extension = media_mime.split('/')[1]
                self.media = SimpleUploadedFile(name=str(uuid.uuid4())+'.'+media_extension, content=base64.b64decode(media_base64), content_type=media_mime)
        super(MemberTrainingStepSerializer, self).save()

    class Meta:
        model = MemberTrainingStep
        fields = ('id','answer','training_step','media','media_base64')

class TrainingSerializer(serializers.HyperlinkedModelSerializer):
    training_steps = TrainingStepSerializer(many=True,read_only=True)
    class Meta:
        model = Training
        fields = ('id','name','training_steps')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id',"user","title","content","media","thumbnail","media_type","create_time","update_time")

class CalendarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Calendar
        fields = ("id","name","color")

class EventSerializer(serializers.HyperlinkedModelSerializer):
    invited = ContactSerializer(many=True,read_only=True)
    members = DownlineSerializer(many=True,read_only=True)
    calendar = CalendarSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ("id","alert_at_hour","alert_5_mins","alert_15_mins","alert_30_mins","alert_1_hour","alert_2_hours","alert_1_day","title","all_day","begin_time","end_time","invited","members","calendar","note","postal_code","complement","lat","lng",'state','city','address','address_number')

class EventRegisterSerializer(serializers.HyperlinkedModelSerializer):
    invited = serializers.PrimaryKeyRelatedField(many=True, queryset=Contact.objects.all())
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=Member.objects.all())
    calendar = serializers.PrimaryKeyRelatedField(many=False, queryset=Calendar.objects.all())

    def create(self,validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(EventRegisterSerializer, self).create(validated_data)

    class Meta:
        model = Event
        fields = ("id","alert_at_hour","alert_5_mins","alert_15_mins","alert_30_mins","alert_1_hour","alert_2_hours","alert_1_day","title","all_day","begin_time","end_time","invited","members","calendar","note","postal_code","complement","lat","lng",'state','city','address','address_number')


class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ("id","acronym","name")

class CitySerializer(serializers.HyperlinkedModelSerializer):
    state = StateSerializer(many=False)
    class Meta:
        model = State
        fields = ("id","state","name")

class PostalCodeSerializer(serializers.HyperlinkedModelSerializer):
    city = CitySerializer(many=False)
    class Meta:
        model = PostalCode
        fields = ("city","street","neighborhood","postal_code","street_type")

class GoalSerializer(serializers.HyperlinkedModelSerializer):
    level = serializers.PrimaryKeyRelatedField(many=False, queryset=Level.objects.all())

    def create(self,validated_data):
        goal = Goal()
        goal.level = validated_data.pop('level')
        member = Member.objects.get(user=self.context['request'].user)
        goal.member = member
        goal.date = validated_data.pop('date')
        goal.save()
        return goal

    class Meta:
        model = Goal
        fields = ("id","level","date")

class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ("id","name","media","thumbnail","media_type")

class MediaCategorySerializer(serializers.HyperlinkedModelSerializer):
    medias = MediaSerializer(many=True,read_only=True)
    class Meta:
        model = MediaCategory
        fields = ("id","name","medias")