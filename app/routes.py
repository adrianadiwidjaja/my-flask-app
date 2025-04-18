from flask import render_template, flash, redirect, url_for, request, Blueprint, abort
from flask_login import current_user, login_required
from . import db
from .models import Post, Comment, Like, Category
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    categories = Category.query.all()
    return render_template('index.html', title='Home', posts=posts, categories=categories)

@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    categories = Category.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category')
        if title and content:
            post = Post(title=title, content=content, author=current_user, category_id=category_id)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Title and content are required!', 'danger')
    return render_template('create_post.html', title='Create Post', categories=categories)

@main.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@main.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    categories = Category.query.all()
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.category_id = request.form.get('category')
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    return render_template('edit_post.html', title='Edit Post', post=post, categories=categories)

@main.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))

@main.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    if content:
        comment = Comment(content=content, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    return redirect(url_for('main.post', post_id=post_id))

@main.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        flash('You unliked this post!', 'info')
    else:
        like = Like(user=current_user, post=post)
        db.session.add(like)
        db.session.commit()
        flash('You liked this post!', 'success')
    return redirect(url_for('main.post', post_id=post_id))

@main.route('/category/<int:category_id>')
def category_posts(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category_id=category_id).order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    return render_template('category.html', title=f'Posts in {category.name}', category=category, posts=posts) 