from django.urls import path
from . import views

urlpatterns = [
  path('',views.home,name='home'),
  path('levels/',views.levels_Screen,name='levels'),
  path('session/<int:session_id>/',views.solve_session,name='solve_session'),
  path('result/<int:session_id>/',views.result,name='result'),
  path('history/',views.history,name='history'),

]
