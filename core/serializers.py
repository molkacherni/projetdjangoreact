from .models import User,ProfileUser
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProfileUser
        fields = ['first_name','last_name','registration_number', 'phone_number', 'address', 'post', 'birthday', 'gender', 'image']
        # fields = '__all__'
        
class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProfileUser
        # fields = ['first_name','last_name','registration_number', 'phone_number', 'address', 'post', 'birthday', 'gender', 'image']
        fields = '__all__'
  
class UserRegistrationSerializer(serializers.ModelSerializer):
    profileuser = UserProfileSerializer()
    class Meta:
        model = User
        fields = ['email','password','profileuser']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        profileuser = validated_data.pop('profileuser')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        ProfileUser.objects.create(user=user,**profileuser)
        return user
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class UpdateUserSerializer(serializers.ModelSerializer):
    profileuser = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('email','profileuser')

    # def validate_email(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(email=value).exists():
    #         raise serializers.ValidationError({"email": "This email is already in use."})
    #     return value

    # def validate_registration_number(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(registration_number=value).exists():
    #         raise serializers.ValidationError({"register number": "This username is already in use."})
    #     return value

    def update(self, instance, validated_data):
        profileuser = validated_data.pop('profileuser')
        #instance.first_name = validated_data['first_name']
        #print(instance)
        
        #instance.email = validated_data['email']
        #instance.registration_number = validated_data['registration_number']
        #instance.birthday = validated_data['birthday']
        #instance.phone_number = validated_data['phone_number']
        #instance.address = validated_data['address']
        #instance.post = validated_data['post']
        #instance.image = validated_data['image']

        instance.save()
        profileuser.post = validated_data['post']
        profileuser.save()

        return instance
class UserListSerializer(serializers.ModelSerializer):
    profileuser = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id','email','role','profileuser')
        # read_only_fields = ('userprofile',)
class UpdatePasswordUserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('old_password', 'password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
            pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['role'] = user.role
        return token


