from rest_framework import serializers
from .models import *
from accounts.models import User
from django.db.models import Q
from .paginations import OfferPagination

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profileId = serializers.IntegerField(source= 'profile.id',read_only=True)
    password = serializers.CharField(style={'input_type':'password'},write_only=True,required=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True,required=True)
    image = serializers.ImageField(source='profile.image',read_only=True)
    class Meta :
        model = User
        fields = ('id','profileId','username','email','password','password2','image')
    def validate(self,data):
        pw1 = data.get('password')
        pw2 = data.pop('password2')
        if pw1 != pw2 :
            raise serializers.ValidationError('Passwords should match')
        return data
    def create(self,validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user_obj = User(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj


class SimpleUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta :
        model = User
        fields = ('id','username')



class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class SimpleProfileSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(source='user.username',read_only=True)
    email = serializers.EmailField(source='user.email',read_only=True)
    class Meta :
        model = Profile
        fields = ('id','url','name','image','about','phone','city','email')



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    offers = serializers.SerializerMethodField('paginated_offers',read_only=True)
    #page_size = serializers.SerializerMethodField('get_page_size', read_only=True)
    #count = serializers.SerializerMethodField('get_count',read_only=True)

    name = serializers.CharField(source='user.username',read_only=True)
    email = serializers.EmailField(source='user.email',read_only=True)

    class Meta :
        model = Profile
        fields = ('id','url','name','image','offers','about','phone','city','email')

    def paginated_offers(self,obj):
        profile = obj
        offers = Offer.objects.filter(profile=profile)
        query = self.context['request'].GET.get('q')
        if query is not None :
            offers = offers.filter(Q(description__icontains=query)|
                                   Q(title__icontains=query)|
                                   Q(profile__user__username__icontains=query)).distinct()

        paginator = OfferPagination()
        page = paginator.paginate_queryset(offers, self.context['request'])
        serializer = OfferSerializer(page, many=True, context={'request': self.context['request']})
        return serializer.data


class OfferSerializer(serializers.HyperlinkedModelSerializer):

    comments = serializers.SerializerMethodField('get_related_comment',read_only=True)
    likes = serializers.SerializerMethodField('get_all_likes',read_only=True)
    profile = serializers.SerializerMethodField('get_profile_info',read_only=True)

    # profileUrl = serializers.HyperlinkedRelatedField(
    #     read_only=True,
    #     source = 'profile',
    #     lookup_field='pk',
    #     view_name='profile-detail'
    # )

    class Meta :
        model = Offer
        fields = ('id','profile','title','image','description','categorie','hide','comments','likes')
    def get_related_comment(self,obj):
        comments = Comment.objects.all().filter(product=obj).order_by('-id')
        serializer = CommentSerializer(comments,many=True,context={'request': self.context['request']})
        return serializer.data
    def get_all_likes(self,obj):
        likes = obj.likes.all()
        serializer = UserSerializer(likes,many=True,context={'request': self.context['request']})
        return serializer.data
    def get_profile_info(self,obj):
        profile_obj = obj.profile
        serializer = SimpleProfileSerializer(profile_obj,many=False,context={'request': self.context['request']})
        return serializer.data


class UpdatePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=255)

    class Meta :
        model = User
        fields = ('password','new_password')
        extra_kwargs = {'password': {'write_only': True, 'required': True},
                        'new_password':{'write_only': True, 'required': True}}




class CommentResponseSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='owner.username',read_only=True)
    image = serializers.ImageField(source='owner.profile.image',read_only=True)
    likes = serializers.SerializerMethodField('get_all_like',read_only=True)
    user_id = serializers.IntegerField(source='owner.id',read_only=True)
    profile_id = serializers.IntegerField(source='owner.profile.id',read_only=True)
    class Meta :
        model = CommentResponse
        fields = ('id','profile_id','comment','owner','user_id','content','username','image','likes')
    def get_all_like(self,obj):
        commentResponse_obj = obj
        likes = commentResponse_obj.likes.all()
        serializers = UserSerializer(likes,many=True,context={'request':self.context['request']})
        return serializers.data

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    username  = serializers.CharField(source='owner.username',read_only=True)
    image     = serializers.ImageField(source='owner.profile.image',read_only=True)
    responses = serializers.SerializerMethodField('get_all_responses',read_only=True)
    likes     = serializers.SerializerMethodField('get_all_likes',read_only=True)
    user_id = serializers.IntegerField(source='owner.id',read_only=True)
    profile_id = serializers.IntegerField(source='owner.profile.id',read_only=True)


    class Meta :
        model = Comment
        fields = ('id','owner','user_id','profile_id','username','image','content','responses','likes')
    def get_all_responses(self,obj):
        comment_obj = obj
        responses = comment_obj.commentresponse_set.all()
        serializer = CommentResponseSerializer(responses,many=True,context={'request':self.context['request']})
        return serializer.data
    def get_all_likes(self,obj):
        comment_obj = obj
        likes = comment_obj.likes.all()
        serializer = UserSerializer(likes,many=True,context={'request':self.context['request']})
        return serializer.data
