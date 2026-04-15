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
    form = MangaForm()
    form.author_id.choices = [(a.id, a.name) for a in Author.query.all()]
    print(form.author_id.choices)  # Debug: Affiche les choix d'auteurs dans la console
    if form.validate_on_submit():
        manga = Manga(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            cover_url=form.cover_url.data,
            author_id=form.author_id.data
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

    # On crée la liste des auteurs, mais on ajoute une option vide au début
    # (0, "--- Aucun auteur ---") sert de valeur par défaut
    authors = Author.query.all()
    form.author_id.choices = [(0, "--- Aucun auteur ---")] + [(a.id, a.name) for a in authors]

    if form.validate_on_submit():
        # Si l'utilisateur a choisi "Aucun" (ID 0), on remet à None en BDD
        author_id_value = form.author_id.data
        if author_id_value == 0:
            author_id_value = None

        manga.title = form.title.data
        manga.description = form.description.data
        manga.price = form.price.data
        manga.stock = form.stock.data
        manga.cover_url = form.cover_url.data
        manga.author_id = author_id_value

        db.session.commit()
        flash('Manga mis à jour.', 'success')
        return redirect(url_for('admin_dashboard'))

    # Si le manga n'a pas d'auteur, on sélectionne l'option 0 dans le formulaire
    if request.method == 'GET' and not manga.author_id:
        form.author_id.data = 0

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
    results = []
    query_text = ""

    # Pour un formulaire GET, on vérifie si search_query est dans request.args
    # ET on utilise validate() qui fonctionnera car c'est une requête GET
    if request.args.get('search_query') and form.validate():
        query_text = form.search_query.data
        results = Manga.query.filter(Manga.title.icontains(query_text)).all()
    
    return render_template('search_results.html', 
                           title='Résultats de recherche', 
                           form=form, 
                           mangas=results, 
                           query=query_text)
