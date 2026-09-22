
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html',redirect_authenticated_user=True), name='login'),
    path('', views.dashboard, name='dashboard'),
    
    path('book-volumes/', views.book_volume_list, name='book_volume_list'),
    path('upload/book-volume/', views.upload_book_volume, name='upload_book_volume'),
    path('edit/book-volume/<int:volume_id>/', views.edit_book_volume, name='edit_book_volume'),
     path('delete/book-volume/<int:volume_id>/', views.delete_book_volume, name='delete_book_volume'),
    
    path('upload/', views.upload_paper, name='upload_paper'),
    path('edit/<int:paper_id>/', views.edit_paper, name='edit_paper'),
    path('delete/<int:paper_id>/', views.delete_paper, name='delete_paper'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('create-user/', views.create_user, name='create_user'),
    
    path('upload/news/', views.upload_news, name='upload_news'),
    path('news/edit/<int:news_id>/', views.edit_news, name='edit_news'),
    path('news/delete/<int:news_id>/', views.delete_news, name='delete_news'),
     
    path('upload/gallery/', views.upload_gallery, name='upload_gallery'),
    path('gallery/edit/<int:gallery_id>/', views.edit_gallery, name='edit_gallery'),
    path('gallery/delete/<int:gallery_id>/', views.delete_gallery, name='delete_gallery'),
    
    path('research_papers/', views.research_papers, name='research_papers'),
    path('news/', views.news_list, name='news_list'),
    path('gallery/', views.gallery_list, name='gallery_list'),
    
    path('edit-about-content/', views.edit_about_content, name='edit_about_content'),
    
    path('edit_contact-info/', views.edit_contact_info, name='edit_contact_info'),
    
    path('upload_editorial_member/', views.upload_editorial_member, name='upload_editorial_member'),
    path('edit_editorial_member/<int:member_id>/', views.edit_editorial_member, name='edit_editorial_member'),
    path('delete_editorial_member/<int:member_id>/', views.delete_editorial_member, name='delete_editorial_member'),
    path('editorial_board_list/', views.editorial_board_list, name='editorial_board_list'),
    
     path('manage-authors-instruction-pdf/', views.manage_authors_instruction_pdf, name='manage_authors_instruction_pdf'),


]
