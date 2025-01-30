from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
from .models import Post, Tag
from app.users.models import User
from app import db




@post_bp.route('/')
def get_posts():
    stmt = db.select(Post).order_by(Post.posted.desc())
    posts =  db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    post = db.get_or_404(Post, id)

    return render_template("detail_post.html", post=post)

@post_bp.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    # Отримуємо пост із бази даних
    post = db.get_or_404(Post, id)
    # Видаляємо пост із бази даних
    db.session.delete(post)
    db.session.commit()

    # Виводимо повідомлення про успішне видалення
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('posts.get_posts'))  # Повертаємося до списку постів


@post_bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    # Отримуємо пост із бази даних
    post = db.get_or_404(Post, id)
    # Ініціалізуємо форму з даними поста
    form = PostForm(obj=post)
    form.publish_date.data = post.posted
    if form.validate_on_submit():
        # Оновлюємо дані поста з форми
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data

        # Зберігаємо зміни у базі даних
        db.session.commit()

        flash('Post updated successfully!', 'success')
        return redirect(url_for('.get_posts'))  # Повертаємося до списку постів

    return render_template('edit_post.html', form=form, post=post)

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    
    # Підвантаження тегів з БД
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    authors = User.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]

    if form.validate_on_submit():
        # Створюємо новий об'єкт Post
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,  # Збереження дати з форми
            user_id=form.author_id.data  # Прив'язка автора
        )
        
        # Прив'язка тегів до поста
        selected_tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]  # Отримуємо теги за їх ID
        new_post.tags = selected_tags  # Прив'язуємо теги до поста

        # Додаємо пост у сесію
        db.session.add(new_post)
        db.session.commit()  # Фіксуємо зміни в базі

        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))  # Повертаємося до списку постів

    return render_template('add_post.html', form=form)
