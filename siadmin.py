from django.contrib.admin import AdminSite,ModelAdmin
from si.forms import SessionForm
from si.models import Student,Course,Session
from django.contrib.auth.models import User,Group
from django.contrib.auth.admin import GroupAdmin,UserAdmin
from django.core.urlresolvers import reverse
import urllib2
import urllib
from django.http import HttpResponse
from settings import STATIC_URL

def generate_excel(modeladmin,request,queryset):
    php_script = STATIC_URL + 'gen_excel.php'
    post_data = []
    count = 0;
    for course in queryset:
        csv = ''
        csv += str(course.year) + ','
        csv += str(course.term) + ','
        csv += str(course.department) + ','
        csv += str(course.code) + ','
        csv += str(course.section) + ','
        csv += str(course.professor) + ','
        first_test = str(course.exam)
        csv += first_test + ','
        midterm = str(course.midterm)
        total_sessions = str(len(Session.objects.filter(course=course)))
        csv += total_sessions + ','
        csv += str(course.user.first_name) + ' ' + str(course.user.last_name) + ','
        studs = Student.objects.filter(course=course)
        for stud in studs:
            csv += str(stud.last_name) + ','
            csv += str(stud.first_name) + ','
            csv += str(stud.interest) + ','
            csv += str(stud.taken) + ','
            csv += str(stud.future) + ','
            csv += str(len(Session.objects.filter(
                    student=stud,course=course,date__lte=first_test))) + ','
            csv += str(len(Session.objects.filter(
                        student=stud,course=course,date__lte=midterm))) + ','

            csv += str(len(Session.objects.filter(
                        student=stud,course=course,date__gt=midterm))) + ','
            
        csv = csv[:-1]
        post_data.append(('csv' + str(count),csv))
        count += 1

    result = urllib2.urlopen(php_script,urllib.urlencode(post_data))
    content = result.read()
    response = HttpResponse(content,content_type='Content-Type: application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=report.xls'
    return response

class SiAdminSite(AdminSite):
    login_template = 'si/login.html'
    index_template = 'si/index.html'
    logout_template='si/logged_out.html'

class StudentAdmin(ModelAdmin):
    search_fields= ['first_name','last_name','course__department','course__code'
,'course__section']
    list_display = ('first_name','last_name','course')
    #list_filter = ('course__department','course__code','course__section','course__id')
    '''list_display = ('first_name','last_name','course')
    list_filter = ('course__department','course__code','course__section','course__id')'''
    exclude = ["user"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course" and not request.user.is_superuser:
            kwargs["queryset"] = Course.objects.filter(user=request.user)
        return super(StudentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self,request):
        qs = super(StudentAdmin,self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

    def save_model(self,request,obj,form,change):
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()
    
    def has_change_permission(self,request,obj=None):
        if not obj:
            return True
        if request.user.is_superuser or obj.user == request.user:
            return True
        else:
            return False
    has_delete_permission = has_change_permission


class CourseAdmin(ModelAdmin):
    exclude = ["user"]
    search_fields= ['course__department','course__code','course__section']
    actions = [generate_excel]
    def queryset(self,request):
        qs = super(CourseAdmin,self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

    def save_model(self,request,obj,form,change):
        obj.user = request.user
        obj.save()
    
    def has_change_permission(self,request,obj=None):
        if not obj:
            return True
        if request.user.is_superuser or obj.user == request.user:
            return True
        else:
            return False
    has_delete_permission = has_change_permission


class SessionAdmin(ModelAdmin):
    list_display = ('date','signin_link','course')
    exclude = ["user"]
    filter_horizontal = ['student']
    form = SessionForm
    
    def signin_link(self,obj):        
        return u'<a href="%ssignin/%s/">%s</a>' % (str(reverse('si.views.index')),obj.id, str(obj) + ' (' + str(obj.course) + ')')
    
    signin_link.allow_tags = True
    signin_link.short_description = "Signin Page"
    '''
    def __init__(self,*args,**kwargs):
        super(SessionAdmin,self).__init__(*args,**kwargs)
        #self.list_display_links = (None,)
        '''
    def formfield_for_manytomany(self,db_field,request,**kwargs):
        if db_field.name == 'student' and not request.user.is_superuser:
            kwargs['queryset'] = Student.objects.filter(user=request.user)
        return super(SessionAdmin,self).formfield_for_manytomany(db_field,request,**kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'course' and not request.user.is_superuser:
            kwargs['queryset'] = Course.objects.filter(user=request.user)
        return super(SessionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self,request):
        qs = super(SessionAdmin,self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

    def save_model(self,request,obj,form,change):
        if not request.user.is_superuser:
            obj.user = request.user

        obj.save()
    
    def has_change_permission(self,request,obj=None):
        if not obj:
            return True
        if request.user.is_superuser or obj.user == request.user:
            return True
        else:
            return False
    has_delete_permission = has_change_permission
    
site = SiAdminSite(name="SI")

site.register(Session,SessionAdmin)
site.register(Student,StudentAdmin)
site.register(Course,CourseAdmin)
site.register(User,UserAdmin)
site.register(Group,GroupAdmin)
