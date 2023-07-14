from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label='First name:',
        help_text='. Letters only.',
        required=False,
        widget=forms.HiddenInput()
    )
    last_name = forms.CharField(
        label='Last name:',
        help_text='. Letters only.',
        required=False,
        widget=forms.HiddenInput()
    )
    username = forms.CharField(
        label='Tên tài khoản:',
        help_text='. Chỉ chấp nhận kí tự, chữ số và các dấu @/./+/-/_.'
    )
    email = forms.EmailField(
        label='Email:',
        help_text=''
    )
    # account_type = forms.CharField(
    #     label='References:',
    #     help_text='If you\'re not sure what to fill in this field, enter your username instead'
    # )
    member1_name = forms.CharField(
        label='Họ tên thành viên 1:',
    )
    member1_id = forms.CharField(
        label='Mã sinh viên của thành viên 1:',
    )
    member1_class = forms.CharField(
        label='Lớp của thành viên 1:',
    )
    member2_name = forms.CharField(
        label='Họ tên thành viên 2:',
    )
    member2_id = forms.CharField(
        label='Mã sinh viên của thành viên 2:',
    )
    member2_class = forms.CharField(
        label='Lớp của thành viên 2:',
    )
    member3_name = forms.CharField(
        label='Họ tên thành viên 3:',
    )
    member3_id = forms.CharField(
        label='Mã sinh viên của thành viên 3:',
    )
    member3_class = forms.CharField(
        label='Lớp của thành viên 3:',
    )
    password1 = forms.CharField(
        label='Mật khẩu:',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Mật khẩu phải bao gồm ít nhất 6 kí tự.'
    )
    password2 = forms.CharField(
    label='Xác nhận mật khẩu:',
    strip=False,
    widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    help_text='Nhập lại mật khẩu để xác nhận. Mật khẩu phải chứa ít nhất 6 kí tự.'
)


    class Meta:
        model = User
        fields = ['username', 'email', 
                  'member1_name', 'member1_id', 'member1_class', 
                  'member2_name', 'member2_id', 'member2_class', 
                  'member3_name', 'member3_id', 'member3_class', 
                  'password1', 'password2']
