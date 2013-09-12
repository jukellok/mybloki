# -*- coding: utf-8 -*-
# Copyright (c) 2013 Juha Kellokoski

from flask import request, redirect, url_for, render_template, flash, \
    session, g
from flask.ext.login import LoginManager, login_user, logout_user, \
    login_required, current_user
from myblog import app, db
from models import User, Post, Tag
from forms import PostForm, TagForm, SearchForm

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/<int:page>')
def view_posts(page=1):
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 8, False)
    return render_template('view_posts.html', posts=posts)


@app.route('/add_post', methods=['POST'])
@login_required
def add_post():
    form = PostForm(request.form)
    if not form.validate():
        flash('Post title or content not valid')
        return redirect(url_for('view_posts'))
    item = Post(request.form['title'], request.form['body'])
    db.session.add(item)
    db.session.commit()
    flash('New post was added')
    return redirect(url_for('view_posts'))


@app.route('/delete_post/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    item = Post.query.get(id)
    if item is None:
        flash('Post was not found')
    else:
        db.session.delete(item)
        db.session.commit()
        flash('Post deleted')
    return redirect(url_for('view_posts'))


@app.route('/start_edit_post/<int:id>')
@login_required
def start_edit_post(id):
    item = Post.query.get(id)
    if item is None:
        flash('Post was not found')
        return redirect(url_for('view_posts'))
    session['current_post'] = id
    return render_template('edit_post.html', post=item)


@app.route('/finish_edit_post', methods=['POST'])
@login_required
def finish_edit_post():
    item = None
    if 'current_post' in session:
        item = Post.query.get(session.get('current_post'))
    if item is None:
        session.pop('current_post', None)
        flash('Post was not found')
        return redirect(url_for('view_posts'))
    form = PostForm(request.form)
    if not form.validate():
        session.pop('current_post', None)
        flash('Post title or content not valid')
        return render_template('view_post.html', post=item)
    item.title = request.form['title']
    item.body = request.form['body']
    db.session.commit()
    session.pop('current_post', None)
    flash('Post was updated')
    return render_template('view_post.html', post=item)


@app.route('/start_edit_post_tags/<int:id>')
@login_required
def start_edit_post_tags(id):
    item = Post.query.get(id)
    if item is None:
        flash('Post was not found')
        return redirect(url_for('view_posts'))
    session['current_post'] = id
    alltags = Tag.query.order_by(Tag.name)
    return render_template('edit_post_tags.html', post=item, alltags=alltags)


@app.route('/add_post_tag/<int:id>')
@login_required
def add_post_tag(id):
    item = None
    if 'current_post' in session:
        item = Post.query.get(session.get('current_post'))
    if item is None:
        session.pop('current_post', None)
        flash('Post was not found')
        return redirect(url_for('view_posts'))
    tag = Tag.query.get(id)
    if tag is None:
        session.pop('current_post', None)
        flash('Tag was not found')
        return redirect(url_for('view_posts'))
    item.tags.append(tag)
    db.session.commit()
    flash('Tag was added')
    alltags = Tag.query.order_by(Tag.name)
    return render_template('edit_post_tags.html', post=item, alltags=alltags)


@app.route('/delete_post_tag/<int:id>')
@login_required
def delete_post_tag(id):
    item = None
    if 'current_post' in session:
        item = Post.query.get(session.get('current_post'))
    if item is None:
        session.pop('current_post', None)
        flash('Post was not found')
        return redirect(url_for('view_posts'))
    tag = Tag.query.get(id)
    if tag is None:
        session.pop('current_post', None)
        flash('Tag was not found')
        return redirect(url_for('view_posts'))
    item.tags.remove(tag)
    db.session.commit()
    flash('Tag was removed')
    alltags = Tag.query.order_by(Tag.name)
    return render_template('edit_post_tags.html', post=item, alltags=alltags)


@app.route('/edit_tags')
@login_required
def edit_tags():
    tags = Tag.query.order_by(Tag.name)
    return render_template('edit_tags.html', tags=tags)


@app.route('/add_tag', methods=['POST'])
@login_required
def add_tag():
    form = TagForm(request.form)
    if not form.validate():
        flash('Tag name not valid')
    else:
        item = Tag(request.form['tag'])
        db.session.add(item)
        db.session.commit()
        flash('New tag created')
    return redirect(url_for('edit_tags'))


@app.route('/delete_tag/<int:id>')
@login_required
def delete_tag(id):
    item = Tag.query.get(id)
    if item is None:
        flash('Tag was not found')
    else:
        db.session.delete(item)
        db.session.commit()
        flash('Tag deleted')
    return redirect(url_for('edit_tags'))


@app.route('/rename_tag/<int:id>', methods=['POST'])
@login_required
def rename_tag(id):
    item = Tag.query.get(id)
    if item is None:
        flash('Tag was not found')
    else:
        form = TagForm(request.form)
        if not form.validate():
            flash('Tag name not valid')
        else:
            item.name = request.form['tag']
            db.session.commit()
            flash('Tag was updated')
    return redirect(url_for('edit_tags'))


@app.route('/search', methods=['POST'])
#@login_required
def search():
    form = SearchForm(request.form)
    if not form.validate():
        return render_template('search.html', term="", results=None)
    term = request.form['searchfield']
    results = db.session.execute("SELECT * FROM post WHERE to_tsvector(\
        'english', title || ' ' || body) @@ to_tsquery(\
        'english', '" + term + "') ORDER BY timestamp DESC LIMIT 20")
    return render_template('search.html', term=term, results=results)


@app.route('/view_post/<int:id>')
#@login_required
def view_post(id):
    item = Post.query.get(id)
    if item is None:
        flash('Post was not found')
        return redirect(url_for('view_posts'))
    return render_template('view_post.html', post=item)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('view_posts'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None or request.form['username'] != user.username or \
                request.form['password'] != user.password:
            flash('Username and password did not match')
        else:
            session.pop('current_post', None)
            login_user(user)
            flash('You signed in')
    return redirect(url_for('view_posts'))


@app.route('/logout')
@login_required
def logout():
    session.pop('current_post', None)
    logout_user()
    flash('You signed out')
    return redirect(url_for('view_posts'))
