from django.db import models
from django.core.exceptions import ValidationError

class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Prevent deletion programmatically (admin will also be restricted)
        raise ValidationError("Industries cannot be deleted.")

    def save(self, *args, **kwargs):
        if not self.pk:
            # Check if we already have 10 industries
            if Industry.objects.count() >= 10:
                raise ValidationError("Cannot create more than 10 industries.")
        super().save(*args, **kwargs)


class Template(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='templates')
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='template_pdfs/')
    hero_image = models.ImageField(upload_to='template_heroes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.industry.name})"

    def clean(self):
        # Validate max 3 templates per industry
        check_count = False
        if not self.pk:
            check_count = True
        else:
            try:
                old = Template.objects.get(pk=self.pk)
                if old.industry_id != self.industry_id:
                    check_count = True
            except Template.DoesNotExist:
                # Should not happen during save of existing object
                pass

        if check_count:
            if self.industry.templates.count() >= 3:
                raise ValidationError(f"Industry '{self.industry.name}' already has 3 templates.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
