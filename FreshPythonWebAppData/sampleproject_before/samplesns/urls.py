# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:28:06 2019

@author: asuto
"""


from django.urls import path

from . import views


urlpatterns=[
        path("",views.index, name = "index"),
        #ログアウト処理
        path("logout/",views.logout, name = "logout"),
        
        #ホーム画面へ遷移
        path("home/", views.home, name="home"),
        
        #投稿処理
        path("home/upload/",views.upload, name = "upload"),
        
        #わっしょい処理
        path("home/good/<str:user_name>/<int:image_id>/<int:my_id>/",views.good, name = "good"),

        #タグ検索処理
        path("home/tagsearch/",views.tagSearch, name = "tag"),
        
        #他ユーザのマイページへジャンプ
        path("home/fripage/<int:friend_id>",views.mypage, name = "friend"),
        
        #マイページへジャンプ
        path("home/mypage/", views.mypage, name="mypage"),
        
        #フォロワーの追加
        path("home/add/",views.addFriend, name = "add"),
        
        #ユーザの検索
        path("home/search/",views.search, name = "search"),
        
        #プロフィール画像の登録
        path("home/samne/", views.samne, name="samne"),
        
        #自己紹介文の登録
        path("home/introduce/",views.introduce, name = "introduce"),
        
        #パスワードの変更
        
        #新規ユーザー登録

        #ユーザの削除
        
        #トレンドワード検索
        
]