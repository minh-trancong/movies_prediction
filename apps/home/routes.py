# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - Minh Tran
"""
from apps.backend.forms import PredictGrossForm
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
# from apps.backend.K_mean import fetch_movies_data
from apps.authentication.models import *
from apps.backend.K_mean import *


@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    movies = Movies.query.paginate(page=page, per_page=10)
    form = PredictGrossForm()
    genre_data = list_genres()
    if request.method == 'POST':
        form = PredictGrossForm(request.form)
        genre_set = set()
        for movie in get_movies():
            genre_set.add(movie.genre)
        form.genre.choices = [(genre, genre) for genre in genre_set]

        if form.validate():
            genre = form.genre.data
            budget = form.budget.data
            rating = form.rating.data
            runtime = form.runtime.data
            predicted_gross = predict_gross(genre, budget, rating, runtime)
            return render_template('home/index.html', segment='index', user_id=current_user.id, movies=movies,
                                   gross=predicted_gross, form=form, genre_data=genre_data)
    genre_set = set()
    for movie in get_movies():
        genre_set.add(movie.genre)
    form.genre.choices = [(genre, genre) for genre in genre_set]
    # Sửa đổi dòng code dưới đây để hiển thị biểu đồ trên trang index
    genre = request.args.get('genre')
    if genre:
        matplotlib.use('Agg')
        plot_url = generate_plot_url(genre)
        return render_template('home/index.html', segment='index', user_id=current_user.id, movies=movies,
                               plot_url=plot_url, form=form, genre_data=genre_data)

    return render_template('home/index.html', segment='index', user_id=current_user.id, movies=movies, form=form, genre_data=genre_data)



@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
