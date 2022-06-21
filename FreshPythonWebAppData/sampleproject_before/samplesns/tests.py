from django.test import TestCase

# Create your tests here.
from django.urls import reverse, resolve
from .views import index, home
from .models import User

#Userクラスのテスト
class UserModelTest(TestCase):
    def setUpClass():
        print('Userクラスのテスト実行前')

    def tearDownClass():
        print('Userクラスのテスト実行後')

    def setUp(self):
        self.user = User(account_name='TEST', password='TESTpass')
        self.user.save()

    def test_create_user(self):
        u = User.objects.filter(account_name='TEST')
        self.assertEqual(self.user, u[0])

    def test_change_user(self):
        u = User.objects.filter(account_name='TEST').first()
        u.password = 'CHANGEpass'
        u.save()

        c_u = User.objects.filter(account_name='TEST').first()
        self.assertEqual(c_u.password, 'CHANGEpass')

#初期ページの確認
class IndexTests(TestCase):
    def test_index_view_status_code(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    def test_index_url_resolves_home_view(self):
        view = resolve('/samplesns/')
        self.assertEquals(view.func, index)

#ホーム画面の確認
class HomeTest(TestCase):
    def setUp(self):
        self.user = User(account_name='TEST', password='TESTpass')
        self.user.save()

    def test_home_view_status_code(self):
        url = reverse('home')
        responese = self.client.post(url, {'name': 'TEST', 'password': 'TESTpass'})
        self.assertEquals(responese.context['user']['account_name'], self.user.account_name)


    def test_home_view_status_code2(self):
        url = reverse('home')
        responese = self.client.post(url, {'name': 'TEST', 'password': 'password'})
        self.assertTemplateUsed(responese,'samplesns/home.html')
        
