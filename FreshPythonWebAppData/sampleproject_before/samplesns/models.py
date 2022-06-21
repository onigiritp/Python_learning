from django.db import models

# Create your models here.
class User(models.Model):
    #クラス変数

    account_name = models.CharField(max_length=100, unique=True) #アカウント名
    password = models.CharField(max_length=100,default="password") #パスワード
    samne = models.CharField(max_length = 100,default="None")
    introduce = models.CharField(max_length = 200,default="None")
    
    def __str__(self):
         return self.account_name
            
class Photo(models.Model):
    image = models.ImageField(upload_to="samplesns/")
        
        
class Friend(models.Model):
    my_num=models.CharField(max_length=10)
    f_num=models.CharField(max_length=10)
    
        
    
     