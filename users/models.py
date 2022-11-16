from django.db import models

class User(models.Model):
    email    = models.CharField(max_length=50)
    password = models.CharField(max_length=300)

    class Meta:
        db_table = "users"
        abstract = False
        managed  = True