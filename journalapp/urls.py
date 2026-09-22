from django.urls import path
from . import views
#from .views import contact_view


urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views.about,name='about'),
    path('publications/',views.publications,name='publications'),
    path('download-volume-papers/<int:volume_id>/', views.download_volume_papers, name='download_volume_papers'),
    path('view-paper/<int:paper_id>/', views.view_paper, name='view_paper'),
    path('download-paper/<int:paper_id>/', views.download_paper, name='download_paper'),
    path("query/", views.query_view, name="query"),
    # path('contact/',views.contact,name='contact'),
     #path('contact/', contact_view, name='contact'),
    path('contact/', views.contact, name='contact'), 
    path('authors/', views.all_authors, name='all_authors'),
    path('gallery/', views.gallery, name='gallery'),
    path('editorial-board/', views.EditorialBoardListView.as_view(), name='editorial_board'),
    path('authors-instruction/', views.authors_instruction, name='authors_instruction'),
    # path('upload/', views.upload_paper, name='upload_paper'),
    # path('paper/<int:paper_id>/', views.paper_detail, name='paper_detail'),
    # path('search/', views.search_papers, name='search_papers'),
]