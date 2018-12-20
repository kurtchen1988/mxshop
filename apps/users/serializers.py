import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

from .models import VerifyCode

from MxShop.settings import REGEX_MOBILE

User = get_user_model()

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param data:
        :return:
        '''

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码非法')

        # 验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError('距离上一次发送未超过60s')

        return mobile

class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True,max_length=4, min_length=4, error_messages={
        'blank':'请输入验证码',
        'required':'请输入验证码',
        'max_length':'验证码格式错误',
        'min_length':'验证码格式错误'
    }, help_text='验证码')

    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=BlogPost.objects.all())])

    def validate_code(self, code):
        '''
        try:
            VerifyCode.objects.get(mobile=self.initial_data['username']).order_by('-add_time')
        except VerifyCode.DoesNotExist as e:
            pass
        except VerifyCode.MultipleObjectsReturned as e:
            pass
        '''

        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_records = verify_records[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
            if five_minutes_ago < last_records.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_records.code != code:
                raise serializers.ValidationError('验证码错误')

        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile')
