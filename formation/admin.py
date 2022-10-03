from django.contrib import admin

# Register your models here.
from .models import Formateur, Formation, SessionFormation, Student, Inscription


class SessionInLine(admin.TabularInline):
    model = SessionFormation
    extra = 2


class FormationAdmin(admin.ModelAdmin):
    fieldsets = [('formateur', {'fields': ['formateur']}),
                 ('name', {'fields': ['name']}),
                 ('description', {'fields': ['description']})]
    inlines = [SessionInLine]
    list_display = ('name', 'description')


admin.site.register(Formation, FormationAdmin)


class FormationInLine(admin.TabularInline):
    model = Formation
    extra = 1


class InscriptionInLine(admin.TabularInline):
    model = Inscription
    extra = 5


class SessionFormationAdmin(admin.ModelAdmin):
    fieldsets = [('formation', {'fields': ['formation']}),
                 ('date', {'fields': ['date']}),
                 ('place', {'fields': ['place']}),
                 ('max_students', {'fields': ['max_students']})]
    inlines = [InscriptionInLine]


admin.site.register(SessionFormation, SessionFormationAdmin)


class InscriptionAdmin(admin.ModelAdmin):
    fieldsets = [('session', {'fields': ['session']}),
                 ('student', {'fields': ['student']})]


admin.site.register(Inscription, InscriptionAdmin)


# User Models
class FormateurAdmin(admin.ModelAdmin):
    fieldsets = [('user', {'fields': ['user']}),
                 ('matricule', {'fields': ['matricule']})
                 ]
    inlines = [FormationInLine]


admin.site.register(Formateur, FormateurAdmin)


class StudentAdmin(admin.ModelAdmin):
    fieldsets = [('user', {'fields': ['user']}),
                 ('matricule', {'fields': ['matricule']})
                 ]
    inlines = [InscriptionInLine]


admin.site.register(Student, StudentAdmin)
