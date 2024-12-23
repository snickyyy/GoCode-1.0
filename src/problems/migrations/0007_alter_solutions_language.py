# Generated by Django 4.2.15 on 2024-11-15 22:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0006_alter_solutions_task"),
    ]

    operations = [
        migrations.AlterField(
            model_name="solutions",
            name="language",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="solution_language",
                to="problems.language",
            ),
        ),
    ]
