from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100)
    resume_file = models.FileField(upload_to='resumes/')
    summary = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    score = models.FloatField(default=0)


    def __str__(self):
        return self.name
