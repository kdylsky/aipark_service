from django.db      import models

from users.models   import User

class Project(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id"
    )
    project_title   = models.CharField(max_length=50)
    created_time    = models.DateTimeField(auto_now_add=True)
    updated_time    = models.DateTimeField(auto_now=True)
    savedpoint      = models.CharField(max_length=50)

    class Meta:
        db_table = "projects"
        abstract = False
        managed  = True


class Text(models.Model):
    project = models.ForeignKey(
        Project,
        db_column="project_id",
        on_delete=models.CASCADE
    )
    text         = models.TextField()
    updated_time = models.DateTimeField(auto_now=True)
    index        = models.IntegerField()
    speed        = models.BooleanField(default=False)
    
    class Meta:
        db_table = "texts"
        abstract = False
        managed  = True