from django.urls import path

from . import views

urlpatterns=[
    path('test',views.test,name='test'),
    path('testDash',views.testDash,name='testDash'),
    path('testClassify',views.testClassify,name='testClassify'),
    path('testSummary',views.testSummary,name='testSummary'),
    path('testLibrary',views.testLibrary,name='testLibrary'),
    path('testSetting',views.testSetting,name='testSetting'),   
    path('testLogin',views.loginPage,name='testLogin'),   



    path('login',views.loginPage,name="login"),
    path('logout',views.logoutUser,name="logout"),
    path('register',views.registerPage,name="register"),
    path('profile/<str:pk>/',views.userProfile,name="user-profile"),

    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>/',views.deleteRoom,name="delete-room"),
    path('delete-message/<str:pk>/',views.deleteMessage,name="delete-message")

]