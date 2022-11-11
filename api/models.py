from django.db import models

class Project(models.Model):
    index = models.IntegerField()
    project_id = models.IntegerField()
    project_title = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects"
        abstract = False
        managed = True


class Text(models.Model):
    project = models.ForeignKey(
        Project,
        db_column="project_id",
        on_delete=models.CASCADE
    )
    text = models.TextField()
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "texts"
        abstract = False
        managed = True


class SavePoint(models.Model):
    project = models.OneToOneField(
        Project,
        db_column="project_id",
        on_delete=models.CASCADE
    )
    savepoint = models.CharField(max_length=50)

    class Meta:
        db_table = "savepoints"
        abstract = False
        managed = True


class Audio(models.Model):
    text = models.OneToOneField(
        Text,
        db_column="text_id",
        on_delete=models.CASCADE
    )
    savepoint = models.ForeignKey(
        SavePoint,
        db_column="savepoint_id",
        on_delete=models.CASCADE
    )
    speed = models.BooleanField(default=False)
    index = models.IntegerField()

    class Meta:
        db_table = "audios"
        abstract = False
        managed = True