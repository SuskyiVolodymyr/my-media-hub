# Generated by Django 5.0.6 on 2024-07-01 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0002_anime_description_cartoon_description_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="genre",
            options={"ordering": ["name"]},
        ),
    ]
