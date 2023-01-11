from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.tvshow import Tvshow
from flask import flash
import os
from contextlib import nullcontext

from datetime import datetime
# Photo upload Imports
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

UPLOAD_FOLDER = 'flask_app/static/img/IMAGE_UPLOADS'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    
    if request.files['network'] == None:
        image = ''
    elif request.files['network'] != None:
        image = request.files['network']

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        time = datetime.now().strftime("%d%m%Y%S%f")
        time += filename
        filename= time
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    data = {
        'title': request.form['title'],
        'network': filename,
        'release_date': request.form['release_date'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    if not Tvshow.validate_tvshows(request.form):
        return redirect(request.referrer)
    Tvshow.create_tvshow(data)
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
