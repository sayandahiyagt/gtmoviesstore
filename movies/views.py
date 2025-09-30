from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, MovieRequest, Petition, PetitionVote
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Q
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from .forms import PetitionForm

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies

    if request.user.is_authenticated:
        template_data['my_requests'] = MovieRequest.objects.filter(
            user=request.user
        ).order_by('-date')
    else:
        template_data['my_requests'] = []

    return render(request, 'movies/index.html', {'template_data': template_data})


def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})


@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)


@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
                      {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)


@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)


@login_required
def create_movie_request(request):
    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        description = (request.POST.get('description') or '').strip()
        if title:
            MovieRequest.objects.create(
                title=title,
                description=description,
                user=request.user
            )
        return redirect('movies.index')
    return redirect('movies.index')


@login_required
def delete_movie_request(request, req_id):
    mr = get_object_or_404(MovieRequest, id=req_id, user=request.user)
    if request.method == 'POST':
        mr.delete()
    return redirect('movies.index')

@login_required
def petition_index(request):
    # list all petitions with public visibility
    petitions = (
        Petition.objects
        .annotate(
            yes_count=Count("votes", filter=Q(votes__is_yes=True)),
            no_count=Count("votes", filter=Q(votes__is_yes=False)),
            total_votes=Count("votes"),
        )
        .select_related("created_by")
    )


    form = PetitionForm()
    return render(
    request,
    "movies/petition_index.html",
    {"petitions": petitions, "form": form},
    )

@login_required
@require_POST
def create_petition(request):
    form = PetitionForm(request.POST)
    if form.is_valid():
        petition = form.save(commit=False)
        petition.created_by = request.user
        petition.save()
        messages.success(request, "Petition created! You can share it for votes.")
    return redirect('movies.petition_index')


@login_required
@require_POST
def vote_yes(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    try:
        PetitionVote.objects.create(petition=petition, user=request.user, is_yes=True)
        messages.success(request, "Vote recorded. Thanks!")
    except IntegrityError:
        messages.info(request, "You've already voted on this petition.")
    return redirect("movies.petition_index")

@login_required
@require_POST
def unvote(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    try:
        PetitionVote.objects.get(petition=petition, user=request.user).delete()
        messages.success(request, "Your vote was removed.")
    except PetitionVote.DoesNotExist:
        messages.info(request, "You haven't voted on this petition yet.")
    return redirect("movies.petition_index")



