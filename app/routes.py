from functools import wraps
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db
from app.forms import RegistrationForm, LoginForm, MangaForm, AuthorForm, SearchForm
from app.models import User, Manga, Author, WishlistItem, CartItem
from flask_login import login_user, current_user, logout_user, login_required

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# --- PUBLIC ROUTES ---
@app.route("/")
@app.route("/home")
def index():
    mangas = Manga.query.all()
    return render_template('index.html', mangas=mangas)


# --- AUTH ROUTES ---
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Votre compte a été créé ! Vous pouvez maintenant vous connecter', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='S\'inscrire', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Échec de la connexion. Veuillez vérifier l\'email et le mot de passe', 'danger')
    return render_template('login.html', title='Se connecter', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


# --- ADMIN ROUTES ---
@app.route("/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    mangas = Manga.query.all()
    authors = Author.query.all()
    return render_template('admin/dashboard.html', mangas=mangas, authors=authors)

@app.route("/admin/author/add", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author(name=form.name.data, bio=form.bio.data)
        db.session.add(author)
        db.session.commit()
        flash('Auteur ajouté avec succès.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/author_form.html', form=form, title='Ajouter un Auteur')

@app.route("/admin/author/view/<int:author_id>")
@login_required
@admin_required
def admin_view_author(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template('admin/view_author.html', author=author, title="Détails de l'Auteur")

@app.route("/admin/author/edit/<int:author_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_author(author_id):
    author = Author.query.get_or_404(author_id)
    form = AuthorForm(obj=author)
    if form.validate_on_submit():
        form.populate_obj(author)
        db.session.commit()
        flash('Auteur mis à jour.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/author_form.html', form=form, title='Modifier l\'Auteur')

@app.route("/admin/author/delete/<int:author_id>", methods=['POST'])
@login_required
@admin_required
def admin_delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    flash('Auteur supprimé.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route("/admin/manga/add", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_manga():
    form = MangaForm() # Les choix se chargent tout seuls ici !
    if form.validate_on_submit():
        manga = Manga(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            cover_url=form.cover_url.data,
            author=form.author.data # On passe directement l'objet auteur (ou None)
        )
        db.session.add(manga)
        db.session.commit()
        flash('Manga ajouté avec succès.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/manga_form.html', form=form, title='Ajouter un Manga')

@app.route("/admin/manga/view/<int:manga_id>")
@login_required
@admin_required
def admin_view_manga(manga_id):
    manga = Manga.query.get_or_404(manga_id)
    return render_template('admin/view_manga.html', manga=manga, title="Détails du Manga")

@app.route("/admin/manga/edit/<int:manga_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_manga(manga_id):
    manga = Manga.query.get_or_404(manga_id)
    form = MangaForm(obj=manga)

    if form.validate_on_submit():
        # Mise à jour simplifiée
        manga.title = form.title.data
        manga.description = form.description.data
        manga.price = form.price.data
        manga.stock = form.stock.data
        manga.cover_url = form.cover_url.data
        manga.author = form.author.data # Si "Aucun" est choisi, form.author.data sera None

        db.session.commit()
        flash('Manga mis à jour.', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/manga_form.html', form=form, title='Modifier le Manga')

@app.route("/admin/manga/delete/<int:manga_id>", methods=['POST'])
@login_required
@admin_required
def admin_delete_manga(manga_id):
    manga = Manga.query.get_or_404(manga_id)
    db.session.delete(manga)
    db.session.commit()
    flash('Manga supprimé.', 'info')
    return redirect(url_for('admin_dashboard'))



# Pour une recherche simple
@app.route("/search")
def search():
    # On initialise le formulaire avec les arguments de l'URL
    form = SearchForm(request.args)
    # 1. On commence par une requête de base qui sélectionne tous les mangas
    query_db = Manga.query

    # 2. Si le titre est rempli, on filtre par titre
    if form.search_query.data:
        query_db = query_db.filter(Manga.title.icontains(form.search_query.data))
    
    # 3. Si un auteur est sélectionné, on filtre par l'ID de cet auteur
    if form.author.data:
        query_db = query_db.filter(Manga.author_id == form.author.data.id)
    
    # 4. On exécute la requête finale
    results = query_db.all()
    
    return render_template('search_results.html', 
                           title='Résultats de recherche', 
                           form=form, 
                           mangas=results, 
                           query=form.search_query.data)
