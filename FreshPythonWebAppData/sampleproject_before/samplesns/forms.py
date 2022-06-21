# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:30:39 2019

@author: asuto
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:10:56 2019

@author: asuto
"""


from django import forms
from .models import User



class LoginForm(forms.Form):
    name = forms.CharField(label="",required=True, max_length=100,
                           widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"ユーザ名"}))
    password = forms.CharField(label="",required=True,max_length=100,
                               widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"パスワード"}))

class UploadFileForm(forms.Form):
    text = forms.CharField(label="",max_length=200,widget=forms.TextInput(attrs={"placeholder":"投稿メッセージを入力", "class":"form-control"}))
    image = forms.ImageField(label="", required=True)
    
class UploadSamneForm(forms.Form):
    #text = forms.CharField(label="",max_length=200,widget=forms.Textarea)
    image = forms.ImageField(label="", required=True)

class SearchForm(forms.Form):
    
    tag_search = forms.CharField(label="", max_length=100,required=True,widget=forms.TextInput(attrs={"placeholder":"タグ検索", "class":"form-control", "id":"search-box"}))
    friend_search = forms.CharField(label="", max_length=100,required=True,widget=forms.TextInput(attrs={"placeholder":"ユーザ検索", "class":"form-control", "id":"search-box"}))

class IntroduceForm(forms.Form):
    introduce = forms.CharField(label="",max_length=35,widget=forms.Textarea(attrs={"cols" : "20", "class":"form-control", "placeholder" : "自己紹介文を入力してください"}))

#パスワードの変更用フォーム
#class UpdatePasswordForm(forms.Form):

#新規ユーザー登録用フォーム
#class CreateUserForm(forms.Form):
