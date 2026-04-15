from app import app, db
from app.models import Author, Manga

def seed_database():
    with app.app_context():
        print("Nettoyage de la base de données (Auteurs et Mangas)...")
        Manga.query.delete()
        Author.query.delete()
        db.session.commit()

        print("Création des données avec de vraies couvertures...")

        # Liste complète des 20 mangas avec de vraies URLs d'images (MyAnimeList)
        catalogue = [
            {
                "author": {"name": "Eiichiro Oda", "bio": "Né en 1975, il est le créateur du manga le plus vendu au monde, One Piece, débuté en 1997."},
                "manga": {"title": "One Piece - Tome 1", "desc": "Monkey D. Luffy part à l'aventure pour trouver le One Piece et devenir le Roi des Pirates.", "price": 6.90, "stock": 150, "cover": "https://cdn.myanimelist.net/images/manga/2/253146.jpg"}
            },
            {
                "author": {"name": "Masashi Kishimoto", "bio": "Mangaka célèbre pour avoir créé Naruto, l'un des shōnens les plus populaires des années 2000."},
                "manga": {"title": "Naruto - Tome 1", "desc": "Naruto Uzumaki, un jeune ninja rejeté, rêve de devenir le Hokage de son village.", "price": 6.85, "stock": 120, "cover": "https://cdn.myanimelist.net/images/manga/3/249658.jpg"}
            },
        
            {
                "author": {"name": "Hiromu Arakawa", "bio": "Mangaka japonaise célèbre pour Fullmetal Alchemist et Silver Spoon. Elle vient d'une famille d'agriculteurs."},
                "manga": {"title": "Fullmetal Alchemist - Tome 1", "desc": "Edward et Alphonse Elric, deux frères alchimistes, cherchent la pierre philosophale pour retrouver leurs corps.", "price": 7.50, "stock": 45, "cover": "https://cdn.myanimelist.net/images/manga/3/243675.jpg"}
            },
            {
                "author": {"name": "Kohei Horikoshi", "bio": "Grand fan de comics américains, ce qui a fortement inspiré son œuvre majeure My Hero Academia."},
                "manga": {"title": "My Hero Academia - Tome 1", "desc": "Dans un monde où 80% de la population a des super-pouvoirs, Izuku Midoriya est né sans Alter.", "price": 6.90, "stock": 110, "cover": "https://cdn.myanimelist.net/images/manga/1/209370.jpg"}
            },
            {
                "author": {"name": "Koyoharu Gotouge", "bio": "Auteur(e) de Demon Slayer, dont l'adaptation en anime a battu tous les records au Japon."},
                "manga": {"title": "Demon Slayer - Tome 1", "desc": "Tanjiro devient un pourfendeur de démons pour sauver sa sœur Nezuko, transformée en démon.", "price": 7.29, "stock": 140, "cover": "https://cdn.myanimelist.net/images/manga/3/179882.jpg"}
            },
            {
                "author": {"name": "Gege Akutami", "bio": "Créateur de Jujutsu Kaisen, connu pour ses combats dynamiques et son système de magie complexe."},
                "manga": {"title": "Jujutsu Kaisen - Tome 1", "desc": "Yuji Itadori avale une relique maudite (le doigt de Sukuna) et rejoint une école d'exorcistes.", "price": 6.95, "stock": 135, "cover": "https://cdn.myanimelist.net/images/manga/3/210341.jpg"}
            },
            {
                "author": {"name": "Kentaro Miura", "bio": "Maître du dark fantasy (1966-2021), créateur du chef-d'œuvre Berserk, célèbre pour ses dessins ultra-détaillés."},
                "manga": {"title": "Berserk - Tome 1", "desc": "Guts, le Guerrier Noir, erre dans un monde médiéval sombre ravagé par les forces démoniaques.", "price": 6.90, "stock": 25, "cover": "https://cdn.myanimelist.net/images/manga/1/159654.jpg"}
            },
            {
                "author": {"name": "Tatsuki Fujimoto", "bio": "Auteur génial et atypique derrière Chainsaw Man et Fire Punch. Son style est très cinématographique."},
                "manga": {"title": "Chainsaw Man - Tome 1", "desc": "Denji, criblé de dettes, fusionne avec son chien-démon tronçonneuse Pochita pour survivre.", "price": 7.29, "stock": 100, "cover": "https://cdn.myanimelist.net/images/manga/3/216464.jpg"}
            },
            {
                "author": {"name": "Makoto Yukimura", "bio": "Auteur de Planetes et Vinland Saga, fasciné par l'histoire européenne et la conquête spatiale."},
                "manga": {"title": "Vinland Saga - Tome 1", "desc": "Thorfinn, un jeune viking islandais, cherche à venger son père tué par le mercenaire Askeladd.", "price": 7.65, "stock": 35, "cover": "https://cdn.myanimelist.net/images/manga/2/188925.jpg"}
            },
            {
                "author": {"name": "Naoki Urasawa", "bio": "Génie du thriller et du suspense (Monster, 20th Century Boys, Pluto)."},
                "manga": {"title": "Monster - Tome 1", "desc": "Le Dr Tenma sauve la vie d'un petit garçon, sans savoir que ce dernier deviendra un tueur en série.", "price": 10.50, "stock": 20, "cover": "https://cdn.myanimelist.net/images/manga/3/258224.jpg"}
            },
        ]

        for item in catalogue:
            # 1. Créer l'auteur
            author = Author(
                name=item["author"]["name"],
                bio=item["author"]["bio"]
            )
            db.session.add(author)
            db.session.flush() # Assigne l'ID de l'auteur pour pouvoir le lier immédiatement

            # 2. Créer le manga avec la vraie image
            manga = Manga(
                title=item["manga"]["title"],
                description=item["manga"]["desc"],
                price=item["manga"]["price"],
                stock=item["manga"]["stock"],
                cover_url=item["manga"]["cover"],  # Utilisation du vrai lien
                author_id=author.id
            )
            db.session.add(manga)

        # 3. Sauvegarder le tout dans la base de données
        db.session.commit()
        print(f"Succès ! {len(catalogue)} auteurs et {len(catalogue)} mangas (avec de vraies couvertures) ont été ajoutés.")

if __name__ == "__main__":
    seed_database()