from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from .models import ResearchPaper, News, GalleryImage, AboutContent, ContactInfo, EditorialBoardMember, AuthorsInstructionPDF, BookVolume
from .forms import ContactForm

from django.contrib import messages
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse, FileResponse
import zipfile
import os
from io import BytesIO


def home(request):
    papers = ResearchPaper.objects.all().order_by('-upload_date')[:6]
    total_papers = ResearchPaper.objects.count()
    total_authors = ResearchPaper.objects.values('author').distinct().count()
    news_list = News.objects.all().order_by('-created_at')
    gallery_images = GalleryImage.objects.all()
    return render(request, 'journal/home.html', {
        'papers': papers,
        'total_papers': total_papers,
        'total_authors': total_authors,
        'news_list': news_list,
        'gallery_images': gallery_images
    })

def authors_instruction(request):
    pdf = AuthorsInstructionPDF.objects.first()
    return render(request, 'journal/authors_instruction.html', {'pdf': pdf})

def about(request):
    about_content = AboutContent.objects.first()
    return render(request, 'journal/about.html', {'about_content': about_content})

# def publications(request):
#     query = request.GET.get('search', '')
#     if query:
#         papers = ResearchPaper.objects.filter(author__icontains=query) | ResearchPaper.objects.filter(title__icontains=query)
#     else:
#         papers = ResearchPaper.objects.all()
#     return render(request, 'journal/publications.html', {'papers': papers, 'query': query})



# def publications(request):
#     query = request.GET.get('search', '')
#     papers = ResearchPaper.objects.all().order_by('-upload_date')

#     if query:
#         papers = papers.filter(
#             Q(title__icontains=query) | Q(author__icontains=query) | Q(abstract__icontains=query)
#         )
    # Get per_page from query parameter, default to 5
    # per_page = request.GET.get('per_page', 5)
    # try:
    #     per_page = int(per_page)
    #     if per_page not in [5, 10, 20]:
    #         per_page = 5
    # except ValueError:
    #     per_page = 5
    # Paginate the papers
    # paginator = Paginator(papers, per_page)
    # page_number = request.GET.get('page', 1)
    # page_obj = paginator.get_page(page_number)

    # return render(request, 'journal/publications.html', {
    #     'papers': page_obj,
    #     'query': query,
    #     'per_page': per_page,
    # })

def publications(request):
    query = request.GET.get('search', '')
    per_page = request.GET.get('per_page', 5)
    volume_id = request.GET.get('volume_id', None)

    try:
        per_page = int(per_page)
        if per_page not in [5, 10, 20]:
            per_page = 5
    except ValueError:
        per_page = 5

    volumes = BookVolume.objects.all().order_by('-created_date', '-id')
    latest_volume = volumes.first()

    selected_volume = latest_volume
    if volume_id:
        selected_volume = get_object_or_404(BookVolume, id=volume_id)

    volume_papers = ResearchPaper.objects.none()
    if selected_volume:
        volume_papers = selected_volume.papers.all().order_by('-upload_date')
        if query:
            volume_papers = volume_papers.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(abstract__icontains=query)
            )

    page_number = request.GET.get('page', 1)
    volume_paginator = Paginator(volume_papers, per_page)
    volume_page_obj = volume_paginator.get_page(page_number)

    context = {
        'volumes': volumes,
        'selected_volume': selected_volume,
        'volume_papers': volume_page_obj,
        'query': query,
        'per_page': per_page,
        'latest_volume': latest_volume,
        'volume_id': volume_id,
    }
    return render(request, 'journal/publications.html', context)

def view_paper(request, paper_id):
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    ResearchPaper.objects.filter(id=paper.id).update(view_count=F('view_count') + 1)
    if paper.pdf:
        return redirect(paper.pdf.url)
    return HttpResponse("Paper file not found.", status=404)


def download_paper(request, paper_id):
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    ResearchPaper.objects.filter(id=paper.id).update(download_count=F('download_count') + 1)
    if paper.pdf and os.path.exists(paper.pdf.path):
        response = FileResponse(open(paper.pdf.path, 'rb'), as_attachment=True, filename=os.path.basename(paper.pdf.name))
        return response
    return HttpResponse("Paper file not found.", status=404)

def download_volume_papers(request, volume_id):
    volume = get_object_or_404(BookVolume, id=volume_id)
    papers = volume.papers.all()

    if not papers.exists():
        return HttpResponse("No papers available for this volume.", status=404)

    # Create a ZIP file in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for paper in papers:
            if paper.pdf and os.path.exists(paper.pdf.path):
                # Sanitize filename
                filename = f"{paper.title.replace(' ', '_').replace('/', '_')}.pdf"
                zip_file.write(paper.pdf.path, filename)

    # Prepare response
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{volume.volume_number}_papers.zip"'
    return response

def query(request):
    return render(request, 'journal/query.html')

def all_authors(request):
    authors = ResearchPaper.objects.values_list('author', flat=True).distinct()
    return render(request, 'journal/all_authors.html', {'authors': authors})

def contact(request):
    contact_info = ContactInfo.objects.first()
    email_list = contact_info.emails.split(',') if contact_info and contact_info.emails else []
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            try:
                # Use EmailMessage to set custom headers
                email_msg = EmailMessage(
                    subject,
                    full_message,
                    email,  
                    ['editordewdrop@bmd.gov.bd'], 
                )
                email_msg.extra_headers = {'Reply-To': email}  
                email_msg.send(fail_silently=False)
                messages.success(request, "Your message has been sent successfully!")
                return redirect("contact")
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
                messages.error(request, f"An error occurred while sending your message: {str(e)}. Please try again.")
    else:
        form = ContactForm()

    return render(request, "journal/contact.html", {
        "form": form,
        "contact_info": contact_info,
        "email_list": email_list
    })

def query_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        attachment = request.FILES.get("attachment")

        max_file_size = 25 * 1024 * 1024
        if attachment and attachment.size > max_file_size:
            messages.error(request, "Attached PDF file must not be more than 25MB.", extra_tags='query')
            return redirect("query")
        if attachment and attachment.content_type != "application/pdf":
            messages.error(request, "Please attach a PDF file only.", extra_tags='query')
            return redirect("query")

        # Prepare email content
        subject = f"Query from {name}"
        full_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"

        try:
            # Optional: Save file
            if attachment:
                fs = FileSystemStorage()
                filename = fs.save(attachment.name, attachment)
                uploaded_file_url = fs.url(filename)
                full_message += f"\n\nAttachment URL: {request.build_absolute_uri(uploaded_file_url)}"

            email_msg = EmailMessage(
                subject,
                full_message,
                email,
                ['editordewdrop@bmd.gov.bd'],
            )
            email_msg.extra_headers = {'Reply-To': email}
            email_msg.send(fail_silently=False)
            messages.success(request, "Your paper has been submitted successfully!", extra_tags='query')
        except Exception as e:
            print(f"Email sending failed with user's email: {str(e)}")
            try:
                email_msg = EmailMessage(
                    subject,
                    full_message,
                    EMAIL_HOST_USER,
                    ['editordewdrop@bmd.gov.bd'],
                )
                email_msg.extra_headers = {'Reply-To': email}
                email_msg.send(fail_silently=False)
                messages.success(request, "Your query has been sent successfully with reply-to set!", extra_tags='query')
            except Exception as e2:
                messages.error(request, f"An error occurred while sending your query: {str(e2)}. Please try again.", extra_tags='query')

        return redirect("query")

    return render(request, "journal/query.html")


# def authors_instruction(request):
#     pdf= AuthorsInstructionPDF.objects.first()
#     return render(request, 'journal/authors_instruction.html', {'pdf': pdf})
@xframe_options_exempt
def authors_instruction(request):
    pdf = AuthorsInstructionPDF.objects.first()
    context = {'pdf': pdf}
    if pdf:
        context['pdf_url'] = request.build_absolute_uri(pdf.pdf.url)
    return render(request, 'journal/authors_instruction.html', context)

def gallery(request):
    gallery_images = GalleryImage.objects.all()
    return render(request, 'journal/gallery.html', {'gallery_images': gallery_images})

class EditorialBoardListView(ListView):
    model = EditorialBoardMember
    template_name = 'journal/editorial_board.html'
    context_object_name = 'members'
    queryset = EditorialBoardMember.objects.all().order_by('sort_order', 'name')