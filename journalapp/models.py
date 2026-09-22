from django.db import models

class BookVolume(models.Model):
    volume_number = models.CharField(max_length=10, unique=True)  # e.g., "Vol. 1"
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.volume_number

    class Meta:
        ordering = ['-created_date']

class ResearchPaper(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    abstract = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='research_papers/')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    volume = models.ForeignKey(BookVolume, on_delete=models.SET_NULL, null=True, blank=True, related_name='papers')
    view_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']

class News(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"

class AboutContent(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About Us Content"

    class Meta:
        verbose_name = "About Us Content"
        verbose_name_plural = "About Us Content"

class ContactInfo(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=20)
    emails = models.TextField()
    website = models.URLField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Contact Information"

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

class EditorialBoardMember(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='editorial_photos/', blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Editorial Board Member"
        verbose_name_plural = "Editorial Board Members"
        ordering = ['sort_order', 'name']

class HitCounter(models.Model):
    total_hits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Total Hits: {self.total_hits}"

class AuthorsInstructionPDF(models.Model):
    pdf = models.FileField(upload_to='authors_instruction/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Authors Instruction PDF"

    class Meta:
        verbose_name = "Authors Instruction PDF"
        verbose_name_plural = "Authors Instruction PDF"