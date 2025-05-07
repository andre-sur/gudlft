import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if not competition or not club:
        flash("Club ou compétition introuvable.")
        return render_template('welcome.html', club=club, competitions=competitions)

    try:
        places_required = int(request.form['places'])
    except ValueError:
        flash("Nombre de places invalide.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérification 1 : pas plus de 12 places par club
    if places_required > 12:
        flash("Impossible de réserver plus de 12 places par compétition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérification 2 : assez de points dans le club
    club_points = int(club['points'])
    if places_required > club_points:
        flash("Vous n'avez pas assez de points pour cette réservation.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérification 3 : assez de places restantes dans la compétition
    available_places = int(competition['numberOfPlaces'])
    if places_required > available_places:
        flash("Pas assez de places disponibles dans la compétition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Tout est OK : mise à jour des données
    competition['numberOfPlaces'] = available_places - places_required
    club['points'] = club_points - places_required

    flash('Réservation réussie !')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/points', methods=['GET'])
def showPoints():
    return render_template('points.html', clubs=clubs)