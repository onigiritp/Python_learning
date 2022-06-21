from django.shortcuts import render,redirect
from  django.template import loader
from .models import User,Friend,Photo
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from glob import glob
import json
from datetime import datetime,timedelta
import os
#データ分析用のライブラリ
import pandas as pd
from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt
import japanize_matplotlib
import scipy.cluster as cluster

# Create your views here.

#初回のＵＲＬ遷移
def index(request):
    form = LoginForm()  #ログインフォーム生成
    #ユーザー登録フォーム生成
    
    
    context={"form":form,}
    #ログインページにジャンプ
    return render(request,"samplesns/login.html",context=context)

def logout(request):
    request.session.clear()
    
    return index(request)

#ホーム画面
def home(request):
    #セッションにログイン情報がない時
    if not "user" in request.session:
            
        f = LoginForm(request.POST)
            
        #入力チェック
        if f.is_valid():
            
            name = f.cleaned_data.get("name")
            password = f.cleaned_data.get("password")


            #DB検索
            parameter={"account_name":name,"password":password}
            u = User.objects.filter(**parameter)
           
            if len(u) == 0:#DBにいない
                return index(request)
            #辞書型リストに変換して、0番目の辞書をuに再代入
            u = u.values()[0]
           
            #セッションに格納
            request.session["user"]=u
        
            #新規ユーザはJSONファイルを保存するディレクトリが無いので作成する
            path=r"samplesns/static/files/u*"
            directries=glob(path)
            tmp=list(map(lambda x: int(x[24:]),directries))
        
            if not u["id"] in tmp:#ディレクトリの作成
                os.mkdir("samplesns/static/files/u{}".format(u["id"]))
        else:
            return index(request)

    #セッションにログイン情報があるとき
    else:
        u = request.session["user"]
            
    uform = UploadFileForm() #画像投稿用フォーム
    sform = SearchForm() #タグ検索用フォーム
        
    con={"upload":uform,"search":sform,"user":u}
        
    #自分のJSONパスを追加
    path=r"samplesns/static/files/u{}".format(u["id"])+"/"
    jsonlist=glob(path+"*.json")
        
    #フォロワーのパスを追加
        
    #フォロワーの情報を検索
    f = Friend.objects.filter(my_num=str(u["id"]))
        
    #フォロワーのJSONパスの追加
    for user in f:
        fid=user.f_num
        path=r"samplesns/static/files/u{}".format(fid)+"/"
        jsonlist=jsonlist+glob(path+"*.json")
            
    #JSONのパスを元にJSONを辞書型リストとして取得
    testlist=[]
    for j in jsonlist:
        with open(file=j,mode="r",encoding="utf-8") as f:
            data =json.load(f)
        testlist.append(data)
        
    testlist.sort(key=sortlist)
    testlist.reverse()
        
    if len(testlist)>0:    
        con["textlist"]=testlist
        con["len"]=len(testlist)
    return render(request,"samplesns/home.html",con)


#画像を時間順に並び替える
def sortlist(x):
    timestr=x["time"]
    result=datetime.strptime(timestr,"%Y-%m-%d %H:%M:%S")  
    return result

#ファイル名を考える    
def getFileName():
        #日付と時刻を文字列化
        now=str(datetime.now())
        
        #不要な情報を削除
        now2=now.split(".")[0]
        now2=now2.replace(":","")
        now2=now2.replace("-","")
        now2=now2.replace(" ","")
        filename=now2+".json"
        
        return filename
        
#画像と投稿文をアップロード
def upload(request):
    if "POST" == request.method:
        
        #セッション内のユーザ情報取得
        user = request.session["user"]
        uid = str(user["id"])
        account_name = str(user["account_name"])
        
        form = UploadFileForm(request.POST,request.FILES)
        
        #ファイルの不正チェック
        if not form.is_valid():
            HttpResponse("エラー")
        
        #/static/media下に保存
        photo = Photo()
        photo.image=form.cleaned_data["image"]
        photo.save()
        
        #保存したパスを取得
        url = photo.image.url.split("/")[-1]
        url="media/samplesns/"+url
        name = getFileName()
        
        
        #ハッシュタタグを分離(テキストの末尾に# でハッシュタグとする)
        tmp=request.POST["text"].split("#")
        text = tmp[0]
        if len(tmp) >1:
            tag = tmp[1:]
            #タグの先頭と末尾に\nと半角スペースとがあったら取り除く
            tag =[i.strip(" ") for i in tag]
            tag =[i.strip("　") for i in tag]
            
            tag =[i.strip("\n") for i in tag]
            tag =[i.strip("\r") for i in tag]
            tag =[i.strip("\t") for i in tag]
            
        else:
            tag=[]
            
        #JSONファイルの作成
        data={  "fileName":name.split(".")[0],
                "uid":uid,
                "user":account_name,
                "text":text,
                "image":url,
                "tag":tag,
                "time":str(datetime.now())[:-7],
                "good":[],
                }
        filepath="samplesns/static/files/u{}/{}".format(uid,name)
        with open (filepath,mode="w",encoding="utf-8") as f:
           json.dump(data,f,ensure_ascii=False)
        
        return redirect(request.META['HTTP_REFERER'])
    
    else:
        return home(request)

#ワッショイボタンの処理
def good(request,user_name,image_id,my_id):
    #写真の持ち主
    user = User.objects.filter(account_name=user_name)[0]
    
    #template = loader.get_template("samplesns/index.html")
    path="samplesns/static/files/u{}/{}.json".format(user.id,image_id)
    
    with open(file=path,mode="r",encoding="utf-8") as f:
        data =json.load(f)
        #ワッショイを自分が押したかどうか判断するロジックの
        #都合上、goodは整数ではなく、アカウントIDのリスト
        data["good"] += [my_id]
        
    with open(file=path,mode="w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False)
        
        return redirect(request.META['HTTP_REFERER'])
    
#自分の投稿を探す
def getMyJson(uid):
    path="samplesns/static/files/u{}/*.json".format(uid)
    files =glob(path)
    
    jlist=[]
    for file in files:
        with open(file=file,mode="r",encoding="utf-8") as f:
            data =json.load(f)
            jlist.append(data)
    return jlist

#ユーザの検索
def search(request):
    if "POST" == request.method:
        friend_name=request.POST["friend_search"]
        user=request.session["user"]
        parameter={"account_name__contains":friend_name}
    
        #DB検索
        friend = User.objects.filter(**parameter).exclude(account_name=user["account_name"])
    
        uform = UploadSamneForm()
        search=SearchForm()

        myid = request.session["user"]["id"]
   
        jlist = getMyJson(myid)
        jlist.sort(key=sortlist)
        jlist.reverse()
        con={"flag":"my","user":user,"upload":uform,"search":search,"friends":friend,"jlist":jlist}
    
        #おすすめユーザの検索メソッド呼び出し
        con["rec_friends"] = recommend_friend()

        return render(request,"samplesns/mypage.html",con)
    else:
        home(request)
#マイページ
def mypage(request,friend_id=None):
    tmp=0
    #自分が自分のマイページを見ようとする
    if friend_id == None:
        user = request.session["user"]
        parameter={"account_name":user["account_name"]}
        flag="my"
        user = User.objects.filter(**parameter)#見たい人
    
    #他人のマイページを見ようとする
    else:
        user = request.session["user"]
        
        flag="friend"
        
        #利用者がフォロー済みかどうか判断
        parameter={"id":friend_id}#検索対象ユーザのID
        parameter2={"my_num":str(request.session["user"]["id"]),"f_num":str(friend_id)}
        follow = Friend.objects.filter(**parameter2)
        if len(follow) ==0:
            tmp=1#未フォロー
        else:
            tmp=2#フォロー済み
        
        user = User.objects.filter(id=friend_id)#検索対象ユーザ
        
    uform = UploadSamneForm()
    search=SearchForm()
    
    #自分のJSONファイルを作成するための
    jlist = getMyJson(user[0].id)
    jlist.sort(key=sortlist)
    jlist.reverse()
    con = {"flag": flag, "user": user[0], "upload": uform, "search": search, "jlist": jlist, "follow": tmp}
    
    #自分のページを見る際には自己紹介欄を修正できるようにする
    if flag== "my":
        iform = IntroduceForm()
        con["introduce"]=iform
        #パスワード更新用フォーム

    return render(request,"samplesns/mypage.html",con)

#1日の時間ごとの投稿データの作成
def day_post(post_list):
    df = pd.DataFrame(columns=['ealrydawn','morning','noon','afternoon','night','midnight'])

    for data in post_list:
        if not data['user'] in df.index:
            temp = pd.DataFrame({'ealrydawn':0,'morning':0,'noon':0,'afternoon':0,'night':0,'midnight':0},index=[data['user']])
            df = df.append(temp)
        #print(df)
         
        if int(data['time'])>=2 and int(data['time']) < 6:
            df.loc[data['user'],'earlydawn'] +=1
        elif int(data['time']) >= 6 and int(data['time']) < 10:
            df.loc[data['user'],'morning'] +=1
        elif int(data['time'])>=10 and int(data['time']) < 14:
            df.loc[data['user'],'noon'] +=1
        elif int(data['time'])>=14 and int(data['time']) < 18:
            df.loc[data['user'],'afternoon'] +=1
        elif int(data['time'])>=18 and int(data['time']) <22:
            df.loc[data['user'],'night'] +=1
        else:
            df.loc[data['user'], 'midnight'] += 1

    return df

#1年分の投稿データの作成
def year_post(postlist):
    postcal_dict = {}
    for date in range(365,-1,-1):
        day = datetime.now()-timedelta(date)
        postcal_dict[day.strftime('%m-%d')] = 0
    
    for dates in postcal_dict.keys():
        for post_date in postlist:
            if  post_date['date'] == dates:
                postcal_dict[dates] += 1

    return postcal_dict

#フォロワーの追加
def addFriend(request):
    if "POST" == request.method:
    
        my_id = str(request.session["user"]["id"])
        y_id = str(request.POST["flag"])
        parameter={"my_num":my_id,"f_num":y_id}
        f = Friend(**parameter)
    
        #フレンド表に追加
        f.save()
    
        return redirect(request.META['HTTP_REFERER'])
    else:
        mypage(request)

#プロフィール画像の登録            
def samne(request):
    if "POST" == request.method:
        
        uid = request.session["user"]["id"]
        user = request.session["user"]["account_name"]
        
        form = UploadFileForm(request.POST,request.FILES)
        
        
        #ファイルの不正チェック
        if not form.is_valid():
            HttpResponse("エラー")
        
        photo = Photo()
        photo.image=form.cleaned_data["image"]
        
        photo.save()
        
        url = photo.image.url.split("/")[-1]
        url="media/samplesns/"+url
        
        #DBの内容を検索
        users = User.objects.filter(id=uid)
        user=users.first()
        #DB内容を更新
        user.samne=url
        user.save()
        
        #辞書型リストに変換して、0番目の辞書をuに再代入
        user = users.values()[0]
            
        #セッションに格納
        request.session["user"]=user

        return mypage(request)
    
    else:
        return mypage(request)

#自己紹介文の追加
def introduce(request):
    if "POST" == request.method:
        intro = request.POST["introduce"]
        uid = request.session["user"]["id"]
        user = User.objects.filter(id=uid)[0]
        user.introduce=intro
    
        #DB更新
        user.save()
    
        return redirect(request.META['HTTP_REFERER'])
    else:
        return mypage(request)

#タグ検索を行う
def tagSearch(request):
    if "tag_search" in request.POST:
        tag = request.POST["tag_search"]
        request.session["tag"]=tag
    else:
        tag=request.session["tag"]
        
    path=r"samplesns/static/files/u*"
    users = glob(path) #全ユーザのパスのリスト
    
    jlist=[] #全JSONデータ(ディクショナリ型)のリスト
    for user in users:
        tmp=user+"/*json"
        jsons =glob(tmp)
        for js in jsons:
            with open(file=js,mode="r",encoding="utf-8") as f:
                data =json.load(f)
                jlist.append(data)
                
    #tagキーワードが入っている全てのJSONを探そう
    result=[]
    
    
    for js in jlist:
        if tag in js["tag"]:#タグはリストとなっている。
            result.append(js)#完全一致で、追加
    con={"key":tag,"posts":result}       
    return render(request,"samplesns/tagsearch.html",con)

#パスワードの更新
#def updatePass(request):

#ユーザーの追加
#def create_user(request):

#ユーザーの削除
#def delete_user(request):


#おすすめユーザの検索

#トレンドワード分析
