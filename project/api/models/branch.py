from django.db import models

# Create your models here.
class Branch(models.Model):
    branch_id = models.IntegerField()
    branch_name = models.CharField(max_length=255)

    def __str__(self):
        return self.branch_name