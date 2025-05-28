from locust import HttpUser, task, between, events
from urllib.parse import quote, quote_plus  # quote_plus pour gérer les espaces
import random
import json

# Chargement des données JSON
def load_clubs():
    with open("clubs.json") as f:
        return json.load(f)["clubs"]

def load_competitions():
    with open("competitions.json") as f:
        return json.load(f)["competitions"]

# Compteur d'erreurs global
error_counter = {
    "404": 0,
    "500": 0,
    "points_error": 0,
    "places_error": 0,
    "unknown_error": 0
}

class ClubSecretary(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:5000/"  # Assurez-vous que ce port correspond à votre serveur Flask

    clubs = load_clubs()
    competitions = load_competitions()

    def on_start(self):
        # Connexion (POST /showSummary)
        self.club = random.choice(self.clubs)
        email = self.club["email"]
        response = self.client.post("/showSummary", data={"email": email})

        if response.status_code != 200:
            print(f"[ERREUR] Connexion échouée pour {email}")

    @task(2)
    def book_places(self):
        club = random.choice(self.clubs)
        competition = random.choice(self.competitions)

        
        # Utiliser quote_plus mais ensuite remplacer '+' par '%20' (ce qui est standard dans les URL)
        encoded_comp = quote(competition["name"]).replace("+", "%20")
        encoded_club = quote(club["name"]).replace("+", "%20")

        print(f"URL demandée : /book/{encoded_comp}/{encoded_club}")

        # Debug : afficher l'URL avant de l'utiliser
        booking_url = f"/book/{encoded_comp}/{encoded_club}"
        print(f"[DEBUG] URL générée : {booking_url}")  # Afficher l'URL générée pour le débogage


        # GET booking page
        res = self.client.get(f"/book/{encoded_comp}/{encoded_club}")
       
        if res.status_code != 200:
            print(f"[404] Page /book non trouvée")
            error_counter["404"] += 1
            return

        try:
            max_places = min(int(competition["numberOfPlaces"]), int(club["points"]), 12)
            if max_places <= 0:
                return
            places = random.randint(1, max_places)
        except Exception:
            error_counter["unknown_error"] += 1
            return

        response = self.client.post("/purchasePlaces", data={
            "club": club["name"],
            "competition": competition["name"],
            "places": str(places)
        })

        if response.status_code == 200:
            if "Réservation confirmée" in response.text:
                print(f"[OK] {places} places réservées pour {club['name']} à {competition['name']}")
            elif "Pas assez de places" in response.text:
                error_counter["places_error"] += 1
            elif "pas assez de points" in response.text:
                error_counter["points_error"] += 1
            else:
                error_counter["unknown_error"] += 1
        elif response.status_code == 500:
            error_counter["500"] += 1
        elif response.status_code == 404:
            error_counter["404"] += 1
        else:
            error_counter["unknown_error"] += 1

    @task(1)
    def view_points(self):
        self.client.get("/points")

# Afficher les erreurs à la fin des tests
@events.quitting.add_listener
def display_summary(environment, **_kwargs):
    print("\n==== Résumé des erreurs ====")
    for key, count in error_counter.items():
        print(f"{key} : {count}")
    print("============================")
