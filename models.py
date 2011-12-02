from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Course(models.Model):
    professor = models.CharField(max_length=100)
    department = models.CharField(max_length=2)
    code = models.IntegerField()
    section = models.CharField(max_length=2)
    exam = models.DateField()
    midterm = models.DateField()
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.department + ' ' + str(self.code) + ' ' + self.section
    
class Student(models.Model):
    FUTURE_CHOICES = (
        ("A","I will return to college here next term and graduate from Wartburg"),
        ("B","I will return here next term but eventually transfer elsewhere to graduate"),
        ("C", "I will not return here but will transfer elsewhere at the end of the term."),
        ("D","I do not intend to return here or to enroll elsewhere next term."),
        ("E","I have other plans/I am undecided about my plans."),
        ("F","I will graduate this term"),
        )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    course = models.ForeignKey(Course)
    interest = models.IntegerField()
    taken = models.BooleanField()
    future = models.CharField(max_length=1,choices=FUTURE_CHOICES)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name + ' ('+self.course.__unicode__() + ')'
    
'''
class Session(models.Model):
    date = models.DateField()
    sutdent = models.ForeignKey(Student)
'''
class Session(models.Model):
    date = models.DateField()
    course = models.ForeignKey(Course)
    student = models.ManyToManyField(Student,blank=True)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return str(self.date)
    class Meta:
        unique_together = ('date','course')

