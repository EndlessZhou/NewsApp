from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(name='create_time', auto_now_add=True)
    modify_time = models.DateTimeField(name='modify_time', auto_now=True)

    class Meta:
        abstract = True


class UserInfo(BaseModel):
    user_name = models.TextField(name='user_name')
    password = models.TextField(name='password')
    phone_number = models.TextField(name='phone_number', unique=True)
    avatar = models.TextField(name='avatar')

    class Meta:
        db_table = "user_info"

    def verify(self):
        try:
            UserInfo.objects.get(password=self.password, phone_number=self.phone_number)
        except self.DoesNotExist:
            return False
        else:
            return True
