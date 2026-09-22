# admin_dashboard/forms.py
from django import forms
from journalapp.models import ResearchPaper
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from journalapp.models import News, GalleryImage 
from journalapp.models import AboutContent
from journalapp.models import ContactInfo
from journalapp.models import EditorialBoardMember
from journalapp.models import AuthorsInstructionPDF
from journalapp.models import BookVolume

class ArticleUploadForm(forms.ModelForm):
    class Meta:
        model = ResearchPaper
        fields = ['title', 'author', 'abstract', 'pdf', 'thumbnail', 'volume']
        help_texts = {
            'author': 'Use superscript affiliation numbers in the author list, e.g. John Doe¹, Jane Roe².',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter the paper title',
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter author names with superscript numbers, e.g. John Doe¹, Jane Roe²',
            }),
            'abstract': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'rows': 5,
                'placeholder': 'Enter a short abstract for the paper',
            }),
            'pdf': forms.FileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': 'application/pdf',
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': 'image/*',
            }),
            'volume': forms.Select(attrs={
                'class': 'form-select form-select-lg',
            }),
        }

class BookVolumeForm(forms.ModelForm):
    class Meta:
        model = BookVolume
        fields = ['volume_number']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_staff = forms.BooleanField(label='Make user staff?', required=False)
    is_superuser = forms.BooleanField(label='Make user admin?', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'is_superuser']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description']

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'title'] 
        
class AboutContentForm(forms.ModelForm):
    class Meta:
        model = AboutContent
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
        }
        

#Contact Form
class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['address', 'phone', 'emails', 'website']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emails': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Enter emails, separated by commas (e.g., info@bmd.gov.bd,journal@bmd.gov.bd)'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def clean_emails(self):
        emails = self.cleaned_data['emails']
        # Split and validate emails
        email_list = [email.strip() for email in emails.split(',') if email.strip()]
        for email in email_list:
            if not forms.EmailField().clean(email):  # Validate each email
                raise forms.ValidationError(f"Invalid email address: {email}")
        return emails
    

# Editorial board members form
class EditorialBoardMemberForm(forms.ModelForm):
    class Meta:
        model = EditorialBoardMember
        fields = ['name', 'designation', 'sort_order', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'sort_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
class AuthorsInstructionPDFForm(forms.ModelForm):
    class Meta:
        model = AuthorsInstructionPDF
        fields = ['pdf']
        widgets = {
            'pdf': forms.FileInput(attrs={'accept': 'application/pdf'}),
        }