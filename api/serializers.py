from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

	@classmethod
	def get_token(cls, user):
		token = super(MyTokenObtainPairSerializer, cls).get_token(user)

		# Add custom claims
		token['username'] = user.username
		return token


class RegisterSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
			required=True,
			validators=[UniqueValidator(queryset=User.objects.all())]
			)

	password = serializers.CharField(write_only=True, required=True)
	password2 = serializers.CharField(write_only=True, required=True)

	sex = serializers.BooleanField(write_only=True, required=True)
	address = serializers.CharField(write_only=True, required=True)
	bthd = serializers.DateField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ('username', 'password', 'password2', 'email', 'sex', 'address', 'bthd')
		extra_kwargs = {
			'sex': {'required': True},
			'address': {'required': True},
			'bthd': {'required': True},
		}

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({"password": "Password fields didn't match."})

		return attrs

	def create(self, validated_data):
	
		user = User.objects.create(
			username = validated_data['username'],
			email = validated_data['email'],
			password = validated_data['password']
		)
		user.set_password(validated_data['password'])
		user.save()

		prof = User.objects.get(username__exact = validated_data['username'])

		sex = validated_data['sex']
		address = validated_data['address']
		bthd = validated_data['bthd']

		prof.profile.sex = sex
		prof.profile.address = address
		prof.profile.bthd = bthd
		prof.save()

		return user