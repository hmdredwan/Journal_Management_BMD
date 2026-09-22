from django.shortcuts import render

# Create your views here.
from journalapp.models import ResearchPaper
from .forms import NewsForm, GalleryItemForm  
from journalapp.models import News, GalleryImage, BookVolume  
from journalapp.models import AboutContent
from journalapp.models import ContactInfo
from journalapp.models import EditorialBoardMember
from journalapp.models import AuthorsInstructionPDF

# admin_dashboard/views.py
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect,get_object_or_404
from journalapp.models import ResearchPaper
from .forms import ArticleUploadForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator  
from django.contrib.auth import logout
from django.contrib import messages
from .forms import EditProfileForm, CreateUserForm
from .forms import AboutContentForm
from .forms import ContactInfoForm
from .forms import EditorialBoardMemberForm
from .forms import AuthorsInstructionPDFForm, BookVolumeForm

# @login_required
# def dashboard(request):
#     articles = ResearchPaper.objects.all()
#     return render(request, 'admin_dashboard/dashboard.html', {'articles': articles})

# @login_required
# def upload_article(request):
#     if request.method == 'POST':
#         form = ArticleUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('admin_dashboard')
#     else:
#         form = ArticleUploadForm()
#     return render(request, 'admin_dashboard/upload.html', {'form': form})
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


# @staff_required
# def logout_view(request):
#     logout(request)
#     return redirect('home')

# @staff_required
# def dashboard(request):
#       papers = ResearchPaper.objects.all()
#       news = News.objects.all()
#       gallery = GalleryImage.objects.all()
#       pdf = AuthorsInstructionPDF.objects.first()
#       return render(request, 'admin_dashboard/dashboard.html',{ 'papers': papers, 'news': news, 'gallery': gallery, 'pdf': pdf,})
@staff_required
def dashboard(request):
    pdf = AuthorsInstructionPDF.objects.first()
    book_volumes = BookVolume.objects.all()
    print(f"Dashboard PDF: {pdf}")
    return render(request, 'admin_dashboard/dashboard.html', {
        'pdf': pdf,
        'papers': ResearchPaper.objects.all(),
        'news': News.objects.all(),
        'gallery': GalleryImage.objects.all(),
        'book_volumes': book_volumes,
    })

@staff_required
def upload_paper(request):
    if request.method == 'POST':
        form = ArticleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = ArticleUploadForm()
    return render(request, 'admin_dashboard/upload.html', {'form': form, 'type': 'Research Paper'})

@staff_required
def edit_paper(request, paper_id):
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    if request.method == 'POST':
        form = ArticleUploadForm(request.POST, request.FILES, instance=paper)
        if form.is_valid():
            form.save()
            return redirect('research_papers')
    else:
        form = ArticleUploadForm(instance=paper)
    return render(request, 'admin_dashboard/upload.html', {'form': form, 'edit': True, 'type': 'Research Paper'})

@staff_required
def delete_paper(request, paper_id):
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    paper.delete()
    return redirect('research_papers')

# @staff_required
# def edit_profile(request):
#     user_form = EditProfileForm(instance=request.user)
#     password_form = PasswordChangeForm(user=request.user)
#     create_user_form = CreateUserForm()

#     if request.method == 'POST':
#         user_form = EditProfileForm(request.POST, instance=request.user)
#         password_form = PasswordChangeForm(request.user, request.POST)

#         if user_form.is_valid() and password_form.is_valid():
#             user_form.save()
#             user = password_form.save()
#             update_session_auth_hash(request, user)  
#             return redirect('edit_profile')

#     return render(request, 'admin_dashboard/edit_profile.html', {
#         'user_form': user_form,
#         'password_form': password_form,
#         'create_user_form': create_user_form,
#     })

@staff_required
def edit_profile(request):
    user_form = EditProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'profile':
            user_form = EditProfileForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('edit_profile')
            else:
                messages.error(request, 'Please correct the errors in the profile form.')

        elif form_type == 'password':
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('edit_profile')
            else:
                messages.error(request, 'Please correct the errors in the password form.')

    return render(request, 'admin_dashboard/edit_profile.html', {
        'user_form': user_form,
        'password_form': password_form,
    })


@staff_required
def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('edit_profile')
    return redirect('edit_profile')

@staff_required
def upload_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_list')  # Redirect to dashboard or a news list page
    else:
        form = NewsForm()
    return render(request, 'admin_dashboard/upload.html', {'form': form, 'type': 'News'})

@staff_required
def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm(instance=news)
    return render(request, 'admin_dashboard/upload.html', {'form': form, 'edit': True, 'type': 'News'})

@staff_required
def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.delete()
    return redirect('news_list')




@staff_required
def upload_gallery(request):
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard or gallery list
    else:
        form = GalleryItemForm()
    return render(request, 'admin_dashboard/upload.html', {'form': form, 'type': 'Gallery'})

@staff_required
def edit_gallery(request, gallery_id):
    image = get_object_or_404(GalleryImage, id=gallery_id)
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = GalleryItemForm(instance=image)
    return render(request, 'admin_dashboard/upload.html', {'form': form, 'edit': True, 'type': 'Gallery'})

@staff_required
def delete_gallery(request, gallery_id):
    image = get_object_or_404(GalleryImage, id=gallery_id)
    image.delete()
    return redirect('dashboard')


# @staff_required
# def research_papers(request):
#     papers = ResearchPaper.objects.all()
#     return render(request, 'admin_dashboard/research_papers.html', {'papers': papers})
@staff_required
def research_papers(request):
    
    papers = ResearchPaper.objects.all().order_by('-upload_date')
    
    per_page = request.GET.get('per_page', 5)
    try:
        per_page = int(per_page)
        if per_page not in [5, 10, 20]:
            per_page = 5  
    except ValueError:
        per_page = 5 
    
    paginator = Paginator(papers, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_dashboard/research_papers.html', {
        'papers': page_obj,
        'per_page': per_page
    })

@staff_required
def news_list(request):
    news = News.objects.all()
    return render(request, 'admin_dashboard/news_list.html', {'news': news})

@staff_required
def gallery_list(request):
    gallery = GalleryImage.objects.all()
    return render(request, 'admin_dashboard/gallery_list.html', {'gallery': gallery})

@staff_required
def edit_about_content(request):
    # Get or create the AboutContent instance
    about_content, created = AboutContent.objects.get_or_create(pk=1)
    if request.method == 'POST':
        form = AboutContentForm(request.POST, instance=about_content)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AboutContentForm(instance=about_content)
    return render(request, 'admin_dashboard/edit_about_content.html', {'form': form})

@staff_required
def edit_contact_info(request):
    contact_info, created = ContactInfo.objects.get_or_create(pk=1)
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=contact_info)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ContactInfoForm(instance=contact_info)
    return render(request, 'admin_dashboard/edit_contact_info.html', {'form': form})

@staff_required
def upload_editorial_member(request):
    if request.method == 'POST':
        form = EditorialBoardMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EditorialBoardMemberForm()
    return render(request, 'admin_dashboard/upload.html', {'form': form, 'type': 'Editorial Member'})

@staff_required
def edit_editorial_member(request, member_id):
    member = get_object_or_404(EditorialBoardMember, id=member_id)
    if request.method == 'POST':
        form = EditorialBoardMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EditorialBoardMemberForm(instance=member)
    return render(request, 'admin_dashboard/upload.html', {'form': form, 'edit': True, 'type': 'Editorial Member'})

@staff_required
def delete_editorial_member(request, member_id):
    member = get_object_or_404(EditorialBoardMember, id=member_id)
    member.delete()
    return redirect('dashboard')

@staff_required
def editorial_board_list(request):
    sort_field = request.GET.get('sort', 'sort_order')
    sort_dir = request.GET.get('dir', 'asc')
    allowed_fields = {'name', 'designation', 'created_at', 'sort_order'}
    if sort_field not in allowed_fields:
        sort_field = 'sort_order'
    if sort_dir not in {'asc', 'desc'}:
        sort_dir = 'asc'
    order_prefix = '' if sort_dir == 'asc' else '-'
    members = EditorialBoardMember.objects.all().order_by(f"{order_prefix}{sort_field}", 'name')
    return render(request, 'admin_dashboard/editorial_board_list.html', {
        'members': members,
        'sort': sort_field,
        'sort_dir': sort_dir,
    })

@staff_required
def manage_authors_instruction_pdf(request):
    pdf_instance, created = AuthorsInstructionPDF.objects.get_or_create(pk=1)
    if request.method == 'POST':
        form = AuthorsInstructionPDFForm(request.POST, request.FILES, instance=pdf_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Authors Instruction PDF updated successfully.')
            return redirect('dashboard')
        else:
            print(form.errors)  # Debug form errors
    else:
        form = AuthorsInstructionPDFForm(instance=pdf_instance)
    return render(request, 'admin_dashboard/upload.html', {'form': form, 'type': 'Authors Instruction PDF', 'edit': not created})


@staff_required
def book_volume_list(request):
    volumes = BookVolume.objects.all()
    return render(request, 'admin_dashboard/book_volume_list.html', {'volumes': volumes})

@staff_required
def upload_book_volume(request):
    if request.method == 'POST':
        form = BookVolumeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book Volume created successfully.', extra_tags='admin')
            return redirect('book_volume_list')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = BookVolumeForm()
    return render(request, 'admin_dashboard/upload_book_volume.html', {
        'form': form,
        'type': 'Book Volume',
        'edit': False,
    })

@staff_required
def edit_book_volume(request, volume_id):
    volume = get_object_or_404(BookVolume, id=volume_id)
    if request.method == 'POST':
        form = BookVolumeForm(request.POST, instance=volume)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book Volume updated successfully.', extra_tags='admin')
            return redirect('book_volume_list')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = BookVolumeForm(instance=volume)
    return render(request, 'admin_dashboard/upload_book_volume.html', {
        'form': form,
        'type': 'Book Volume',
        'edit': True,
    })

@staff_required
def delete_book_volume(request, volume_id):
    volume = get_object_or_404(BookVolume, id=volume_id)
    if request.method == 'POST':
        volume.delete()
        messages.success(request, 'Book Volume deleted successfully.', extra_tags='admin')
        return redirect('book_volume_list')
    return render(request, 'admin_dashboard/confirm_delete.html', {
        'object': volume,
        'type': 'Book Volume',
    })
    
@staff_required
def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User created successfully.', extra_tags='admin')
            return redirect('edit_profile')
        else:
            print(f"Form errors: {form.errors}")
    return redirect('edit_profile')

