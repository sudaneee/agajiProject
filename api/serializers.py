from rest_framework import serializers
from src.models import User, Report, Notification
from django_filters.rest_framework import DjangoFilterBackend

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Report
        fields = ['user', 'category', 'content', 'image1', 
                    'image2', 'image3',  'audio', 'video', 'latitude', 'longitude',]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'ninNo',
            'name',
            'phoneNo',
            'address',
            'state',
            'lga',
            'nextOfKin',
            'nokAddress',
            'nokPhoneNo',
            'occupation',
        )



class UserProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'ninNo',
            'name',
            'phoneNo',
            'address',
            'state',
            'lga',
            'nextOfKin',
            'nokAddress',
            'nokPhoneNo',
            'occupation',
        )

    def update(self, instance, validated_data):
        #return self.update(request, *args, **kwargs)
        instance.username = validated_data['username']
        instance.ninNo = validated_data['ninNo']
        instance.name = validated_data['name']
        instance.phoneNo = validated_data['phoneNo']
        instance.address = validated_data['address']
        instance.state = validated_data['state']
        instance.lga = validated_data['lga']
        instance.nextOfKin = validated_data['nextOfKin']
        instance.nokAddress = validated_data['nokAddress']
        instance.nokPhoneNo = validated_data['nokPhoneNo']
        instance.occupation = validated_data['occupation']
        instance.save()
        return instance


class ReportHistorySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Report
        fields = [
            'url',
            'id',
            'user',
            'category',
            'content',
            'image1',
            'image2',
            'image3',
            'audio',
            'video',
            'latitude',
            'longitude',
            'created',
            'resolved',
        ]


class NotificationViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'department',
            'state',
            'lga',
            'title',
            'image',
            'body',
            'created',

        )


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'department',
            'state',
            'lga',
            'title',
            'image',
            'body',
            'created',
        ]