from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from .serializers import UserSerializers, MailSerializers, User, Mail


class UserAdminsListView(ListAPIView):
    queryset = User.objects.filter(is_admin=True)
    serializer_class = UserSerializers


class UserGetOrCreate(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_object(self):
        json = self.request.data
        user_id = json['user_id']
        data = json['data']
        try:
            user = User.objects.get(user_id=user_id)
        except User.objects.model.DoesNotExist:
            user = User(user_id=user_id, **data)
            user.save()
        return user

class MailGet(RetrieveUpdateDestroyAPIView):
    queryset = Mail.objects.all()
    serializer_class = MailSerializers

    def get_object(self):
        json = self.request.data
        data = json['data']
        return Mail.objects.get(**data)


class MailsGet(ListAPIView):
    serializer_class = MailSerializers
    queryset = Mail.objects.all()

    def get_queryset(self):
        json = self.request.data
        data = json['data']
        user_id = json['user_id']
        return Mail.objects.filter(user_id=user_id, **data)

class CreateMail(RetrieveUpdateDestroyAPIView):
    serializer_class = MailSerializers
    queryset = Mail.objects.all()

    def get_object(self):
        json = self.request.data
        data = json['data']
        user_id = json['user_id']
        return Mail.objects.create(user_id=user_id, **data)
