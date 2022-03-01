from django.db import models
from asgiref.sync import sync_to_async


class User(models.Model):
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    username = models.SlugField(max_length=255, default='')
    language_code = models.CharField(max_length=10, default=None)
    is_bot = models.BooleanField(default=None)
    is_admin = models.BooleanField(default=False)
    user_id = models.IntegerField()

    def get_full_name(self):
        if self.first_name or self.last_name:
            if not self.first_name and self.last_name:
                return f'{self.last_name}'
            elif self.first_name and not self.last_name:
                return f'{self.first_name}'
            else:
                return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.username}'

    @classmethod
    async def get_or_create(cls, user_id, **kwargs):
        try:
            user = await sync_to_async(cls.objects.get)(user_id=user_id)
            await sync_to_async(cls.objects.update)(user_id=user_id, **kwargs)
        except cls.objects.model.DoesNotExist:
            user = cls(user_id=user_id, **kwargs)
            await sync_to_async(user.save)()
        return user

    @classmethod
    async def get_admins(cls):
        admins = await sync_to_async(list)(cls.objects.filter(is_admin=True))
        return admins

    def __str__(self):
        return self.get_full_name()


class Mail(models.Model):
    user_id = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    email_type = models.CharField(default='mail', max_length=255)

    def __str__(self):
        return f'{self.email}'

    @classmethod
    async def get_mails(cls, user_id, **kwargs):
        mails = await sync_to_async(list)(cls.objects.filter(user_id=user_id, **kwargs))
        return mails

    @classmethod
    async def create(cls, user_id, **kwargs):
        mail = await sync_to_async(cls.objects.create)(user_id=user_id, **kwargs)
        return mail

    @classmethod
    async def get(cls, **kwargs):
        mail = await sync_to_async(cls.objects.get)(**kwargs)
        return mail

    async def remove(self):
        self.is_active = False
        await sync_to_async(self.save)()