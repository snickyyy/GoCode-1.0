# Generated by Django 4.2.15 on 2024-11-25 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0003_alter_comments_conversation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comments",
            name="content",
            field=models.TextField(
                blank=True,
                help_text="The maximum number of characters is 2000.",
                max_length=2000,
            ),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="content",
            field=models.TextField(
                blank=True,
                help_text="The maximum number of characters is 5000.",
                max_length=5000,
            ),
        ),
    ]
