from django import forms

from .models import UserModel


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'placeholder': 'Enter username here...'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        "placeholder": "Enter email here..."}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={
        'placeholder': 'Enter first name here...'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={
        'placeholder': "Enter last name here..."}))
    birthday = forms.DateField(label='Birthday', widget=forms.DateInput(attrs={
        'placeholder': 'Enter birthday here...', 'id': 'birthday'},
        format='%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    gender = forms.ChoiceField(label='Gender', choices=UserModel.GENDER_CHOICES, widget=forms.Select(attrs={
        'placeholder': 'Select your gender...'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "placeholder": "Enter password here..."}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm password..."}))

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name', 'birthday', 'gender')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        user.is_staff = False
        user.is_active = True
        if commit:
            user.save()
        return user
