from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','password']
        extra_kwargs = {
            # only write purpose, won't show password
            'password' : {'write_only' : True}
        }

### If we want to be able to return complete object instances
    # based on the validated data we need to implement one or both of the .create() and .update() methods. For example:
    # 검증된 데이터를 기반으로 완전한 객체 인스턴스를 반환 : create() or update()
    def create(self, validated_data):
        password = validated_data.pop('password', None)

        ## User 모델
        instance = self.Meta.model(**validated_data)
        if password is not None:
            # 패스워드 해쉬
            instance.set_password(password)

        # 비밀번호 넣은 것 저장
        instance.save()
        return instance