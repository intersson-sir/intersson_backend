from django.db import models

class Review(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    review_text = models.TextField()
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.first_name} {self.last_name} ({self.company_name})"
