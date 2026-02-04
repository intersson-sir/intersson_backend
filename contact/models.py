from django.db import models

class DiscussProject(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_method = models.CharField(max_length=100, help_text="Preferred method of contact (e.g., Email, Phone)")
    project_description = models.TextField()
    attachment = models.FileField(upload_to='project_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Project Inquiry from {self.full_name} ({self.created_at.date()})"
