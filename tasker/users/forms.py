from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from branch.models import Branch
from engineers.models import Engineer
from technicians.models import Technician

User = get_user_model()


ROLE_CHOICES = (
    ('engineer', 'Техник'),
    ('technician', 'Инженер'),
)


class CreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    branch = forms.ChoiceField(
        choices=[(branch.pk, branch.name) for branch in Branch.objects.all()])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name',
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
        if commit:
            user.save()
            if role == 'technician':
                tech = Technician.objects.create(
                    user=user, branch_id=branch_id)
            elif role == 'engineer':
                eng = Engineer.objects.create(user=user, branch_id=branch_id)
        return user
