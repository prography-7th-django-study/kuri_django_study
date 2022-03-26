from django.conf import settings
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# class User(AbstractUser):
#      pass

 
# class User(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=20)

# user가 '선택한' book이기 때문에 users에서 Fk로 1:N 관계만 만들어 주면 된다!! (다른 모델은 필요 없음)
class Book(models.Model):
    # ISBN : 국제표준도서번호 - 이미 있는 고유명사는 그대로 써주는 것이 좋다 (이럴 때는 대문자 허용!)
    name = models.CharField(max_length=1000)
    ISBN = models.CharField(max_length=50, unique=True)
    author = models.CharField(max_length=500)
    # 카테고리는 따로 빼서 만드는 것이 좋음 (서로 종속관계)
    # large_category = models.CharField(max_length=100)
    # medium_category = models.CharField(max_length=100)
    # small_category = models.CharField(max_length=100)
    category = models.ForeignKey('SmallCategory', on_delete=models.CASCADE, related_name='preferred_category')

    image = models.URLField(max_length=2000, blank=True, default="")
    score = models.FloatField()
    publisher = models.CharField(max_length=500)
    # m2n 관계이기 때문에 related_name 설정
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='preferred_books', blank=True)

    def __str__(self):
        return self.name

## self : 내 모델을 FK

# 카테고리 : 이렇게 계속 종속된 형태?
# class LargeCategory(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.name
#
#
# class MediumCategory(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     category = models.ForeignKey('LargeCategory', on_delete=models.CASCADE, blank=True)
#
#     def __str__(self):
#         return self.name

### MPTTModel 사용
# https://django-mptt.readthedocs.io/en/latest/tutorial.html
# hierarchical data를 다루는데 유리하다고 함
class SmallCategory(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    # category = models.ForeignKey('MediumCategory', on_delete=models.CASCADE, blank=True)


    ###### TreeForeignKey를 쓰면 계층 구조 쿼리에도 엄청 좋다는데...
    ########## null=True 안쓰면 에러 (카테고리 가진게 없다고)
    ### https://django-mptt.readthedocs.io/en/latest/models.html?highlight=TreeForeignKey#the-treemanager-custom-manager
    category = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="sub_categories") # depth
    #
    class MPTTMeta:
        parent_attr = 'category'

    def __str__(self):
        return self.name

## 생각해볼 거리
# category 따로 빼기
# author를 따로 빼기 - 2명 이상일 수도 있으므로
# 선호도 가중치는 어떻게 할 것인가 - user마다 다르므로 캐싱?
