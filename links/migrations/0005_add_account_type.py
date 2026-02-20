from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0004_add_cancelled_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='negativelink',
            name='type',
            field=models.CharField(
                choices=[
                    ('post', 'Post'),
                    ('comment', 'Comment'),
                    ('video', 'Video'),
                    ('article', 'Article'),
                    ('account', 'Account'),
                ],
                help_text='Type of content',
                max_length=20,
            ),
        ),
    ]
