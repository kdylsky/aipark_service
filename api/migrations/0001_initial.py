# Generated by Django 4.1.3 on 2022-11-11 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("project_title", models.CharField(max_length=50)),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                ("updated_time", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "projects",
                "abstract": False,
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Text",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("updated_time", models.DateTimeField(auto_now=True)),
                ("index", models.IntegerField()),
                (
                    "project",
                    models.ForeignKey(
                        db_column="project_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.project",
                    ),
                ),
            ],
            options={
                "db_table": "texts",
                "abstract": False,
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="SavePoint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("savepoint", models.CharField(max_length=50)),
                (
                    "project",
                    models.OneToOneField(
                        db_column="project_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.project",
                    ),
                ),
            ],
            options={
                "db_table": "savepoints",
                "abstract": False,
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Audio",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("speed", models.BooleanField(default=False)),
                (
                    "savepoint",
                    models.ForeignKey(
                        db_column="savepoint_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.savepoint",
                    ),
                ),
                (
                    "text",
                    models.OneToOneField(
                        db_column="text_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.text",
                    ),
                ),
            ],
            options={
                "db_table": "audios",
                "abstract": False,
                "managed": True,
            },
        ),
    ]
