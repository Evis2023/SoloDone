from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.tvshow import Tvshow
from flask import flash


@app.route('/create')
def createForm():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id']
    }
    return render_template('create.html', loggedUser= User.get_user_by_id(data),)


@app.route('/create/show', methods = ['POST'])
def createShow():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tvshow.validate_tvshows(request.form):
        return redirect(request.referrer)
   
    Tvshow.create_tvshow(request.form)
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'tvshow_id': id,
        'user_id': session['user_id']
    }
    currentShow = Tvshow.get_tvshows_by_id(data)

    if not session['user_id'] == currentShow['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')

    Tvshow.delete(data)
    return redirect(request.referrer)


@app.route('/show/<int:id>')
def showOne(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'tvshow_id': id,
        'user_id': session['user_id']
    }
    userLikedPosts = User.get_logged_user_liked_posts(data)

    return render_template('show.html', loggedUser= User.get_user_by_id(data),show = Tvshow.get_tvshows_by_id(data), userLikedPosts = userLikedPosts)

@app.route('/edit/<int:id>')
def editForm(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
            'tvshow_id': id,
            'user_id': session['user_id']
        }
    currentTvshow = Tvshow.get_tvshows_by_id(data)

    if not session['user_id'] == currentTvshow['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')
   
    return render_template('update.html', loggedUser= User.get_user_by_id(data), show = Tvshow.get_tvshows_by_id(data))

@app.route('/update/<int:id>', methods = ['POST'])
def updateRecipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tvshow.validate_tvshows(request.form):
        return redirect(request.referrer)
    
    currentTvshow = Tvshow.get_tvshows_by_id(request.form)

    if not session['user_id'] == currentTvshow['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')
    
    Tvshow.update_tvshow(request.form)

    return redirect('/')


@app.route('/like/<int:id>')
def addLike(id):
    data = {
        'tvshow_id': id,
        'user_id': session['user_id']
    }
    Tvshow.addLike(data)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def removeLike(id):
    data = {
        'tvshow_id': id,
        'user_id': session['user_id']
    }
    Tvshow.removeLike(data)
    return redirect(request.referrer)
