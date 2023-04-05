from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from branches.models import Branch
from engineers.models import Engineer
from technicians.models import Technician

User = get_user_model()


ROLE_CHOICES = (
    ('engineer', 'Инженер'),
    ('technician', 'Техник'),
)


class CreationForm(UserCreationForm):
    last_name = forms.CharField(required=True,
                                max_length=30,
                                label='Фамилия',
                                help_text='Введите фамилию',)
    first_name = forms.CharField(required=True,
                                 max_length=30,
                                 label='Имя',
                                 help_text='Введите имя')
    middle_name = forms.CharField(required=True,
                                  max_length=30,
                                  label='Отчество',
                                  help_text='Введите отчество',)
    phone_number = forms.CharField(required=False,
                                   max_length=20,
                                   label='Телефон',
                                   help_text='Введите телефон',)
    role = forms.ChoiceField(choices=ROLE_CHOICES,
                             label='Должность')
    branch = forms.ChoiceField(
        choices=[(branch.pk, branch.city) for branch in Branch.objects.all()],
        label='Филиал')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('last_name', 'first_name', 'middle_name', 'phone_number',
                  'username', 'email', 'role', 'branch')

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in dict(ROLE_CHOICES).keys():
            raise forms.ValidationError('Недопустимая роль')
        return role

    def save(self, commit=True):
        user = super().save(commit=False)
        branch_id = self.cleaned_data['branch']
        role = self.cleaned_data['role']
        last_name = self.cleaned_data['last_name']
        first_name = self.cleaned_data['first_name']
        middle_name = self.cleaned_data['middle_name']
        phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
            if role == 'technician':
                tech = Technician.objects.create(
                    user=user,
                    branch_id=branch_id,
                    last_name=last_name,
                    first_name=first_name,
                    middle_name=middle_name,
                    phone=phone_number,
                )
            elif role == 'engineer':
                eng = Engineer.objects.create(
                    user=user,
                    branch_id=branch_id,
                    last_name=last_name,
                    first_name=first_name,
                    middle_name=middle_name,
                    phone=phone_number,
                )
        return user
