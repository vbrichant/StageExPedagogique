from django.contrib import admin

# Register your models here.
from .models import Formateur, Formation, SessionFormation, Student, Inscription


class SessionInLine(admin.TabularInline):
    model = SessionFormation
    extra = 2


class FormationAdmin(admin.ModelAdmin):
    fieldsets = [('name', {'fields': ['name']}),
                 ('description', {'fields': ['description']}),
                 ('formateur', {'fields': ['formateur']})]
    inlines = [SessionInLine]
    list_display = ('name', 'description', 'formateur')


admin.site.register(Formation, FormationAdmin)


class FormationInLine(admin.TabularInline):
    model = Formation
    extra = 1


class FormateurAdmin(admin.ModelAdmin):
    fieldsets = [('name', {'fields': ['name']})]
    inlines = [FormationInLine]


admin.site.register(Formateur, FormateurAdmin)


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


class StudentAdmin(admin.ModelAdmin):
    fieldsets = [('matricule', {'fields': ['matricule']}),
                 ('name', {'fields': ['firstname']}),
                 (None, {'fields': ['lastname']})]
    inlines = [InscriptionInLine]


admin.site.register(Student, StudentAdmin)
