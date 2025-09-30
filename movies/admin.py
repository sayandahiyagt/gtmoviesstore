from django.contrib import admin

from .models import Movie, Review, Petition, PetitionVote



class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    autocomplete_fields = ('created_by',)

@admin.register(PetitionVote)
class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ('petition', 'user', 'vote', 'created_at')
    list_filter = ('vote',)
    search_fields = ('petition__title', 'user__username')
    autocomplete_fields = ('petition', 'user')