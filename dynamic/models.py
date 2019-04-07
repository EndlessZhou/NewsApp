from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(name='create_time', auto_now_add=True)
    modify_time = models.DateTimeField(name='modify_time', auto_now=True)
    status = models.IntegerField(name='status', default=1)

    class Meta:
        abstract = True


class Dynamic(BaseModel):
    phone_number = models.TextField(name='phone_number')
    text = models.TextField(name='text')
    photo = models.TextField(name='photo')

    class Meta:
        db_table = "dynamic"


class DynamicDetail(BaseModel):
    dynamic_id = models.IntegerField(name='dynamic_id')
    phone_number = models.TextField(name='phone_number')
    text = models.TextField(name='text')

    class Meta:
        db_table = 'dynamic_detail'


class Follow(BaseModel):
    owner = models.TextField(name='owner')
    friend = models.TextField(name='friend')

    class Meta:
        db_table = "follow"


class Like(BaseModel):
    dynamic_id = models.IntegerField(name='dynamic_id')
    operator = models.TextField(name='operator')

    class Meta:
        db_table = 'like'


class Comment(BaseModel):
    dynamic_id = models.IntegerField(name='dynamic_id')
    operator = models.TextField(name='operator')
    text = models.TextField(name='text')

    class Meta:
        db_table = 'comment'
