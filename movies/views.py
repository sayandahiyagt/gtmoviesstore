from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, MovieRequest, Petition, PetitionVote
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages


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


def petitions_index(request):
    """Public page listing all petitions and their vote totals."""
    petitions = Petition.objects.order_by('-created_at').all()
    template_data = {
        'petitions': petitions,
    }
    return render(request, 'movies/petitions_index.html', {'template_data': template_data})


@login_required
def petitions_create(request):
    """Create a new petition (auth required)."""
    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        description = (request.POST.get('description') or '').strip()
        if not title:
            messages.error(request, 'Title is required.')
            return redirect('petitions.create')
        Petition.objects.create(
            title=title,
            description=description,
            created_by=request.user
        )
        messages.success(request, 'Your petition was created.')
        return redirect('petitions.index')
    return render(request, 'movies/petitions_create.html', {})


@login_required
def petitions_vote(request, id):
    """Cast a YES/NO vote. If user already voted, we update their vote."""
    if request.method != 'POST':
        return redirect('petitions.index')

    petition = get_object_or_404(Petition, id=id)
    vote_str = request.POST.get('vote')
    if vote_str not in ('yes', 'no'):
        messages.error(request, 'Invalid vote.')
        return redirect('petitions.index')

    vote_bool = (vote_str == 'yes')

    obj, created = PetitionVote.objects.get_or_create(
        petition=petition,
        user=request.user,
        defaults={'vote': vote_bool}
    )
    if not created:
        # Update existing vote if changed
        if obj.vote != vote_bool:
            obj.vote = vote_bool
            obj.save(update_fields=['vote'])

    messages.success(request, f'Your vote has been {"recorded" if created else "updated"}.')
    return redirect('petitions.index')