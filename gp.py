from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import smtplib

# Import per autenticazione e database
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

app = Flask(__name__)
app.secret_key = 'ISA&Isa1221'  # Sostituisci con una chiave sicura

# Configurazione database (usiamo SQLite per semplicità)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

# Configurazione Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ---------------------------
# Modello Utente
# ---------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    newsletter = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



destinations = {
    "Pavia": 0,
    "Milano": 0,
    "Roma": 0,
    "Napoli": 0,
    "Firenze": 0,
    # Francia
    "Parigi": 0,
    "Nizza": 0,
    "Montpellier": 0,
    "Marsiglia": 0,
    "Lione": 0,
    "Lille": 0,
    "Bordeaux": 0,
    "Carcassonne": 0,
    "Tolosa": 0,
    "Strasburgo": 0,
    "Nantes": 0,
    "Ajaccio": 0,
    # Germania
    "Berlino": 0,
    "Amburgo": 0,
    "Monaco": 0,
    "Stoccarda": 0,
    "Francoforte": 0,
    "Colonia": 0,
    "Norimberga": 0,
    "Dresda": 0,
    # Spagna
    "Barcellona": 0,
    "Madrid": 0,
    "Valencia": 0,
    "Bilbao": 0,
    "Siviglia": 0,
    "Granada": 0,
    "Cordova": 0,
    "Toledo": 0,
    "Malaga": 0,
    # Inghilterra
    "York": 0,
    "Liverpool": 0,
    "Bath": 0,
    "Oxford": 0,
    "Londra": 0,
    "Cambridge": 0,
    "Manchester": 0,
    "Brighton": 0,
    # Paesi Bassi
    "Amsterdam": 0,
    "Utrecht": 0,
    "Rotterdam-Aia": 0,
    "Groningen": 0,
    # EUcentrale
    "Praga": 0,
    "Vienna": 0,
    "Bratislava": 0,
    "Varsavia": 0,
    "Cracovia": 0,
    # Svizzera, Portogallo, Danimarca
    "CERN": 0,
    "Copenaghen": 0,
    "Zurigo": 0,
    "Berna": 0,
    "Lisbona": 0,
    "Porto": 0,
    # Balcani
    "Budapest": 0,
    "Sarajevo": 0,
    "Tirana": 0,
    "Atene": 0,
    "Delfi": 0,
    "Zagabria": 0,
    "Lubiana": 0,
    # LOCAL
    "Centro Storico": 0,
    "Mercato Locale": 0,
    "Parco Naturale": 0,
    "Museo Locale": 0,
}

# Domande per il sondaggio locale
local_questions = [
    {
        "question": "Quale tipo di esperienza locale preferisci?",
        "options": {
            "Cibo tradizionale": {"Centro Storico": 5, "Mercato Locale": 2},
            "Passeggiata in natura": {"Parco Naturale": 5, "Centro Storico": 2},
            "Eventi culturali": {"Centro Storico": 3, "Museo Locale": 5}
        }
    },
    {
        "question": "Quale budget pensi di spendere per una gita locale?",
        "options": {
            "Basso": {"Mercato Locale": 5, "Parco Naturale": 3},
            "Medio": {"Museo Locale": 5, "Centro Storico": 2},
            "Alto": {"Centro Storico": 4, "Museo Locale": 3}
        }
    },
    {
        "question": "Quanto preferisci che duri la gita locale?",
        "options": {
            "Mezza giornata": {"Centro Storico": 5, "Mercato Locale": 3},
            "Giornata intera": {"Parco Naturale": 5, "Centro Storico": 2},
            "Più di una giornata": {"Museo Locale": 4, "Parco Naturale": 3}
        }
    },
    {
        "question": "Quale attività ti piacerebbe fare durante la gita locale?",
        "options": {
            "Visita musei locali": {"Museo Locale": 5, "Centro Storico": 3},
            "Escursione all'aperto": {"Parco Naturale": 5, "Mercato Locale": 2},
            "Degustazione di prodotti locali": {"Mercato Locale": 4, "Museo Locale": 4}
        }
    },
    {
        "question": "Che tipo di atmosfera preferisci?",
        "options": {
            "Tradizionale": {"Centro Storico": 5, "Mercato Locale": 3},
            "Moderna": {"Museo Locale": 5, "Parco Naturale": 2},
            "Rilassata": {"Parco Naturale": 4, "Centro Storico": 4}
        }
    }
]

# Domande per il sondaggio in Europa
questions = [








    
#1
    {
        "question": "Qual è il clima desiderato per il viaggio?",
        "options": {
            "Indifferente": {},
            "Caldo": {                      "Pavia": 0,
                                            "Milano": 0,
                                            "Roma": 9,
                                            "Napoli": 9,
                                            "Firenze": 8,
                                            # Francia
                                            "Parigi": 6,
                                            "Nizza": 8,
                                            "Montpellier": 7,
                                            "Marsiglia": 8,
                                            "Lione": 6,
                                            "Lille": 5,
                                            "Bordeaux": 8,
                                            "Carcassonne": 7,
                                            "Tolosa": 7,
                                            "Strasburgo": 6,
                                            "Nantes": 7,
                                            "Ajaccio": 9,
                                            # Germania
                                            "Berlino": 4,
                                            "Amburgo": 3,
                                            "Monaco": 4,
                                            "Stoccarda": 3,
                                            "Francoforte": 4,
                                            "Colonia": 5,
                                            "Norimberga": 3,
                                            "Dresda": 3,
                                            # Spagna
                                            "Barcellona": 9,
                                            "Madrid": 9,
                                            "Valencia": 9,
                                            "Bilbao": 7,
                                            "Siviglia": 9,
                                            "Granada": 8,
                                            "Cordova": 8,
                                            "Toledo": 9,
                                            "Malaga": 9,
                                            # Inghilterra
                                            "York": 3,
                                            "Liverpool": 4,
                                            "Bath": 3,
                                            "Oxford": 3,
                                            "Londra": 5,
                                            "Cambridge": 4,
                                            "Manchester": 3,
                                            "Brighton": 4,
                                            # Paesi Bassi
                                            "Amsterdam": 4,
                                            "Utrecht": 3,
                                            "Rotterdam-Aia": 4,
                                            "Groningen": 2,
                                            # EUcentrale
                                            "Praga": 5,
                                            "Vienna": 5,
                                            "Bratislava": 4,
                                            "Varsavia": 3,
                                            "Cracovia": 3,
                                            # Svizzera, Portogallo, Danimarca
                                            "CERN": 3,
                                            "Copenaghen": 2,
                                            "Zurigo": 4,
                                            "Berna": 3,
                                            "Lisbona": 8,
                                            "Porto": 8,
                                            # Balcani
                                            "Budapest": 5,
                                            "Sarajevo": 6,
                                            "Tirana": 6.5,
                                            "Atene": 8,
                                            "Delfi": 8,
                                            "Zagabria": 7,
                                            "Lubiana": 5,
    },
            "Freddo": {                     "Pavia": 0,
                                            "Milano": 0,
                                            "Roma": 3,
                                            "Napoli": 3,
                                            "Firenze": 4,
                                            # Francia
                                            "Parigi": 5,
                                            "Nizza": 3,
                                            "Montpellier": 3,
                                            "Marsiglia": 2,
                                            "Lione": 5,
                                            "Lille": 6,
                                            "Bordeaux": 4,
                                            "Carcassonne": 4,
                                            "Tolosa": 4,
                                            "Strasburgo": 5,
                                            "Nantes": 6,
                                            "Ajaccio": 2,
                                            # Germania
                                            "Berlino": 8,
                                            "Amburgo": 9,
                                            "Monaco": 7,
                                            "Stoccarda": 8,
                                            "Francoforte": 7,
                                            "Colonia": 7,
                                            "Norimberga": 7,
                                            "Dresda": 8,
                                            # Spagna
                                            "Barcellona": 2,
                                            "Madrid": 2,
                                            "Valencia": 2,
                                            "Bilbao": 4,
                                            "Siviglia": 2,
                                            "Granada": 2,
                                            "Cordova": 2,
                                            "Toledo":2,
                                            "Malaga": 1,
                                            # Inghilterra
                                            "York": 9,
                                            "Liverpool": 9,
                                            "Bath": 8,
                                            "Oxford": 8,
                                            "Londra": 8,
                                            "Cambridge": 8,
                                            "Manchester": 9,
                                            "Brighton": 8,
                                            # Paesi Bassi
                                            "Amsterdam": 8,
                                            "Utrecht": 8,
                                            "Rotterdam-Aia": 8,
                                            "Groningen": 9,
                                            # EUcentrale
                                            "Praga": 8,
                                            "Vienna": 8,
                                            "Bratislava": 8,
                                            "Varsavia": 9,
                                            "Cracovia": 8,
                                            # Svizzera, Portogallo, Danimarca
                                            "CERN": 8,
                                            "Copenaghen": 10,
                                            "Zurigo": 8,
                                            "Berna": 8,
                                            "Lisbona": 3,
                                            "Porto": 3,
                                            # Balcani
                                            "Budapest": 6.5,
                                            "Sarajevo": 6,
                                            "Tirana": 6,
                                            "Atene": 4,
                                            "Delfi": 4,
                                            "Zagabria": 4,
                                            "Lubiana": 5,

                },
            "Moderato": {
                                            "Pavia": 0,
                                            "Milano": 0,
                                            "Roma": 0,
                                            "Napoli": 0,
                                            "Firenze": 0,
                                            # Francia
                                            "Parigi": 6,
                                            "Nizza": 6,
                                            "Montpellier": 6,
                                            "Marsiglia": 6,
                                            "Lione": 6,
                                            "Lille": 6,
                                            "Bordeaux": 6,
                                            "Carcassonne": 6,
                                            "Tolosa":6,
                                            "Strasburgo": 5,
                                            "Nantes": 6,
                                            "Ajaccio": 5,
                                            # Germania
                                            "Berlino": 4,
                                            "Amburgo": 4,
                                            "Monaco": 5,
                                            "Stoccarda": 5,
                                            "Francoforte": 5,
                                            "Colonia": 4.5,
                                            "Norimberga": 5.5,
                                            "Dresda": 5,
                                            # Spagna
                                            "Barcellona": 5,
                                            "Madrid": 5,
                                            "Valencia": 5,
                                            "Bilbao": 6.5,
                                            "Siviglia": 5,
                                            "Granada": 5,
                                            "Cordova": 5,
                                            "Toledo": 5,
                                            "Malaga": 5,
                                            # Inghilterra
                                            "York": 3,
                                            "Liverpool": 3,
                                            "Bath": 4,
                                            "Oxford": 4,
                                            "Londra": 4,
                                            "Cambridge": 4,
                                            "Manchester": 3,
                                            "Brighton": 4,
                                            # Paesi Bassi
                                            "Amsterdam": 5,
                                            "Utrecht": 5,
                                            "Rotterdam-Aia": 5,
                                            "Groningen": 4,
                                            # EUcentrale
                                            "Praga": 5,
                                            "Vienna": 6,
                                            "Bratislava": 5,
                                            "Varsavia": 4,
                                            "Cracovia": 5,
                                            # Svizzera, Portogallo, Danimarca
                                            "CERN": 5,
                                            "Copenaghen": 4,
                                            "Zurigo": 5,
                                            "Berna": 5,
                                            "Lisbona": 6,
                                            "Porto": 6,
                                            # Balcani
                                            "Budapest": 6,
                                            "Sarajevo": 6,
                                            "Tirana": 6,
                                            "Atene": 6,
                                            "Delfi": 6,
                                            "Zagabria": 6,
                                            "Lubiana": 5,
                }
        }
    },




#2
    {
        "question": "Qual è il metodo di trasporto voluto (il tipo di mezzo influisce sul prezzo)?",
        "options": {
            "Pullman": {
                                        "Pavia": 0,
                                        "Milano": 0,
                                        "Roma": 0,
                                        "Napoli": 0,
                                        "Firenze": 0,
                                        # Francia
                                        "Parigi": 2,
                                        "Nizza": 7,
                                        "Montpellier": 7,
                                        "Marsiglia": 7,
                                        "Lione": 5,
                                        "Lille": 2,
                                        "Bordeaux": 3,
                                        "Carcassonne": 3,
                                        "Tolosa": 3,
                                        "Strasburgo": 3,
                                        "Nantes": 2,
                                        "Ajaccio": 1,
                                        # Germania
                                        "Berlino": 2,
                                        "Amburgo": 1,
                                        "Monaco": 5,
                                        "Stoccarda": 5,
                                        "Francoforte": 4,
                                        "Colonia": 2,
                                        "Norimberga": 4,
                                        "Dresda": 2,
                                        # Spagna
                                        "Barcellona": 3,
                                        "Madrid": 2,
                                        "Valencia": 1,
                                        "Bilbao": 1,
                                        "Siviglia": 1,
                                        "Granada": 1,
                                        "Cordova": 1,
                                        "Toledo": 2,
                                        "Malaga": 1,
                                        # Inghilterra
                                        "York": -2,
                                        "Liverpool": -2,
                                        "Bath": -2,
                                        "Oxford": -2,
                                        "Londra": -2,
                                        "Cambridge": -2,
                                        "Manchester": -2,
                                        "Brighton": -2,
                                        # Paesi Bassi
                                        "Amsterdam": 1,
                                        "Utrecht": 1,
                                        "Rotterdam-Aia": 1,
                                        "Groningen": 0,
                                        # EUcentrale
                                        "Praga": 5,
                                        "Vienna": 6,
                                        "Bratislava": 6,
                                        "Varsavia": 4,
                                        "Cracovia": 5,
                                        # Svizzera, Portogallo, Danimarca
                                        "CERN": 7,
                                        "Copenaghen": 0,
                                        "Zurigo": 7,
                                        "Berna": 7,
                                        "Lisbona": 0,
                                        "Porto": 0,
                                        # Balcani
                                        "Budapest": 3,
                                        "Sarajevo": 5,
                                        "Tirana": 4,
                                        "Atene": 3,
                                        "Delfi": 3,
                                        "Zagabria": 7,
                                        "Lubiana": 8,
                },
            "Treno": {
                                        # Francia
                                        "Parigi": 6.5,
                                        "Nizza": 9,
                                        "Montpellier": 7.5,
                                        "Marsiglia": 8,
                                        "Lione": 8,
                                        "Lille": 6,
                                        "Bordeaux": 6,
                                        "Carcassonne": 6.5,
                                        "Tolosa": 6.5,
                                        "Strasburgo": 6,
                                        "Nantes": 6,
                                        "Ajaccio": -18,
                                        # Germania
                                        "Berlino": 6,
                                        "Amburgo": 3,
                                        "Monaco": 8,
                                        "Stoccarda": 7.5,
                                        "Francoforte": 6.5,
                                        "Colonia": 4,
                                        "Norimberga": 7,
                                        "Dresda": 4.5,
                                        # Spagna
                                        "Barcellona": 4,
                                        "Madrid": 2,
                                        "Valencia": 1,
                                        "Bilbao": 1,
                                        "Siviglia": 1,
                                        "Granada": 1,
                                        "Cordova": 1,
                                        "Toledo": 1,
                                        "Malaga": 1,
                                        # Inghilterra
                                        "York": -5,
                                        "Liverpool": -5,
                                        "Bath": -5,
                                        "Oxford": -5,
                                        "Londra": -1,
                                        "Cambridge": -1,
                                        "Manchester": -5,
                                        "Brighton": -1,
                                        # Paesi Bassi
                                        "Amsterdam": 2,
                                        "Utrecht": 2,
                                        "Rotterdam-Aia": 2,
                                        "Groningen": 1,
                                        # EUcentrale
                                        "Praga": 6,
                                        "Vienna": 7,
                                        "Bratislava": 7,
                                        "Varsavia": 2,
                                        "Cracovia": 4,
                                        # Svizzera, Portogallo, Danimarca
                                        "CERN": 8,
                                        "Copenaghen": 0,
                                        "Zurigo": 9,
                                        "Berna": 9,
                                        "Lisbona": 0,
                                        "Porto": 0,
                                        # Balcani
                                        "Budapest": 3,
                                        "Sarajevo": 6,
                                        "Tirana": 4,
                                        "Atene": 2,
                                        "Delfi": 2,
                                        "Zagabria": 8,
                                        "Lubiana": 8,
                },
            "Aereo": {

                                        "Pavia": 0,
                                        "Milano": 0,
                                        "Roma": 0,
                                        "Napoli": 0,
                                        "Firenze": 0,
                                        # Francia
                                        "Parigi": 10,
                                        "Nizza": 6,
                                        "Montpellier": 5,
                                        "Marsiglia": 5,
                                        "Lione": 6,
                                        "Lille": 7,
                                        "Bordeaux": 6,
                                        "Carcassonne": 5,
                                        "Tolosa": 6,
                                        "Strasburgo": 6,
                                        "Nantes": 6,
                                        "Ajaccio": 9,
                                        # Germania
                                        "Berlino": 10,
                                        "Amburgo": 8,
                                        "Monaco": 6,
                                        "Stoccarda": 6,
                                        "Francoforte": 9,
                                        "Colonia": 7,
                                        "Norimberga": 7,
                                        "Dresda": 7,
                                        # Spagna
                                        "Barcellona": 10,
                                        "Madrid": 10,
                                        "Valencia": 9,
                                        "Bilbao": 8,
                                        "Siviglia": 8,
                                        "Granada": 8,
                                        "Cordova": 8,
                                        "Toledo": 9,
                                        "Malaga": 8,
                                        # Inghilterra
                                        "York": 9,
                                        "Liverpool": 10,
                                        "Bath": 9,
                                        "Oxford": 9,
                                        "Londra": 10,
                                        "Cambridge": 9,
                                        "Manchester": 10,
                                        "Brighton": 9,
                                        # Paesi Bassi
                                        "Amsterdam": 10,
                                        "Utrecht": 8,
                                        "Rotterdam-Aia": 9,
                                        "Groningen": 8,
                                        # EUcentrale
                                        "Praga": 6,
                                        "Vienna": 6,
                                        "Bratislava": 6,
                                        "Varsavia": 8,
                                        "Cracovia": 8,
                                        # Svizzera, Portogallo, Danimarca
                                        "CERN": 4,
                                        "Copenaghen": 10,
                                        "Zurigo": 4,
                                        "Berna": 4,
                                        "Lisbona": 10,
                                        "Porto": 9,
                                        # Balcani
                                        "Budapest": 10,
                                        "Sarajevo": 7,
                                        "Tirana": 8.25,
                                        "Atene": 10,
                                        "Delfi": 9,
                                        "Zagabria": 7,
                                        "Lubiana": 6,
                }
        }
    },
#3
    {
        "question": "Quanto deve durare il viaggio?",
        "options": {
            "1-2 giorni": {
                                        "Parigi": 0,
                                        "Nizza": 4,
                                        "Montpellier": 4,
                                        "Marsiglia": 4,
                                        "Lione": 4,
                                        "Lille": 0,
                                        "Bordeaux": 0,
                                        "Carcassonne": 4,
                                        "Tolosa": 4,
                                        "Strasburgo": 0,
                                        "Nantes": 0,
                                        "Ajaccio": 3,
                                        # Germania
                                        "Berlino": 0,
                                        "Amburgo": 0,
                                        "Monaco": 3,
                                        "Stoccarda": 1,
                                        "Francoforte": 2,
                                        "Colonia": 2,
                                        "Norimberga": 2,
                                        "Dresda": 1,
                                        # Spagna
                                        "Barcellona": 1,
                                        "Madrid": 0,
                                        "Valencia": 2,
                                        "Bilbao": 2,
                                        "Siviglia": 2,
                                        "Granada": 2,
                                        "Cordova": 2,
                                        "Toledo": 0,
                                        "Malaga": 2,
                                        # Inghilterra
                                        "York": 0,
                                        "Liverpool": 0,
                                        "Bath": 0,
                                        "Oxford": 0,
                                        "Londra": 0,
                                        "Cambridge": 0,
                                        "Manchester": 0,
                                        "Brighton": 0,
                                        # Paesi Bassi
                                        "Amsterdam": 2,
                                        "Utrecht": 2,
                                        "Rotterdam-Aia": 2,
                                        "Groningen": 1,
                                        # EUcentrale
                                        "Praga": 2,
                                        "Vienna": 2,
                                        "Bratislava": 1,
                                        "Varsavia": 2,
                                        "Cracovia": 3,
                                        # Svizzera, Portogallo, Danimarca
                                        "CERN": 5,
                                        "Copenaghen": 0,
                                        "Zurigo": 3,
                                        "Berna": 3,
                                        "Lisbona": 0,
                                        "Porto": 0,
                                        # Balcani
                                        "Budapest": 0,
                                        "Sarajevo": 0,
                                        "Tirana": 0,
                                        "Atene": 0,
                                        "Delfi": 0,
                                        "Zagabria": 2,
                                        "Lubiana": 3,

                },
            "3-4 giorni": {
                                        "Parigi": 7,
                                        "Nizza": 7,
                                        "Montpellier": 7,
                                        "Marsiglia": 7,
                                        "Lione": 7,
                                        "Lille": 6,
                                        "Bordeaux": 8,
                                        "Carcassonne": 6,
                                        "Tolosa": 8,
                                        "Strasburgo": 8,
                                        "Nantes": 8,
                                        "Ajaccio": 8,
                                        # Germania
                                        "Berlino": 7,
                                        "Amburgo": 7,
                                        "Monaco": 6,
                                        "Stoccarda": 6,
                                        "Francoforte": 8,
                                        "Colonia": 8,
                                        "Norimberga": 9,
                                        "Dresda": 9,
                                        # Spagna
                                        "Barcellona": 8,
                                        "Madrid": 8,
                                        "Valencia": 7.5,
                                        "Bilbao": 8,
                                        "Siviglia": 8,
                                        "Granada": 8,
                                        "Cordova": 7,
                                        "Toledo": 8,
                                        "Malaga": 8,
                                        # Inghilterra
                                        "York": 8,
                                        "Liverpool": 7,
                                        "Bath": 8,
                                        "Oxford": 8,
                                        "Londra": 7.5,
                                        "Cambridge": 8,
                                        "Manchester": 8,
                                        "Brighton": 7,
                                        # Paesi Bassi
                                        "Amsterdam": 9,
                                        "Utrecht": 9,
                                        "Rotterdam-Aia": 8,
                                        "Groningen": 8,
                                        # EUcentrale
                                        "Praga": 8,
                                        "Vienna": 8,
                                        "Bratislava": 7,
                                        "Varsavia": 8,
                                        "Cracovia": 8,
                                        # Svizzera, Portogallo, Danimarca
                                        "CERN": 7,
                                        "Copenaghen": 9,
                                        "Zurigo": 8,
                                        "Berna": 8,
                                        "Lisbona": 9,
                                        "Porto": 8.5,
                                        # Balcani
                                        "Budapest": 8,
                                        "Sarajevo": 7.5,
                                        "Tirana": 8,
                                        "Atene": 8,
                                        "Delfi": 7.5,
                                        "Zagabria": 7,
                                        "Lubiana": 7,

                },
            "Più di 4 giorni": {
                                        # Francia
                                        "Parigi": 9,
                                        "Nizza": 8,
                                        "Montpellier": 7.5,
                                        "Marsiglia": 7.5,
                                        "Lione": 7.5,
                                        "Lille": 7.5,
                                        "Bordeaux": 6,
                                        "Carcassonne": 6,
                                        "Tolosa": 6,
                                        "Strasburgo": 6,
                                        "Nantes": 6,
                                        "Ajaccio": 7,
                                        # Germania
                                        "Berlino": 9,
                                        "Amburgo": 8,
                                        "Monaco": 6.5,
                                        "Stoccarda": 7,
                                        "Francoforte": 8.5,
                                        "Colonia": 7.5,
                                        "Norimberga": 7,
                                        "Dresda": 6,
                                        # Spagna
                                        "Barcellona": 9.5,
                                        "Madrid": 9.5,
                                        "Valencia": 8,
                                        "Bilbao": 7,
                                        "Siviglia": 8,
                                        "Granada": 7,
                                        "Cordova": 6,
                                        "Toledo": 7,
                                        "Malaga": 7,
                                        # Inghilterra
                                        "York": 9,
                                        "Liverpool": 9,
                                        "Bath": 8.5,
                                        "Oxford": 8,
                                        "Londra": 9.5,
                                        "Cambridge": 9,
                                        "Manchester": 9,
                                        "Brighton": 8,
                                        # Paesi Bassi
                                        "Amsterdam": 9.5,
                                        "Utrecht": 8,
                                        "Rotterdam-Aia": 9,
                                        "Groningen": 6.75,
                                        # EUcentrale
                                        "Praga": 8,
                                        "Vienna": 8,
                                        "Bratislava": 6.75,
                                        "Varsavia": 7,
                                        "Cracovia": 7,
                                        # Svizzera, Portogallo, Danimarca
                                        "CERN": 5,
                                        "Copenaghen": 9,
                                        "Zurigo": 7.25,
                                        "Berna": 7.25,
                                        "Lisbona": 9,
                                        "Porto": 9,
                                        # Balcani
                                        "Budapest": 8.75,
                                        "Sarajevo": 8,
                                        "Tirana": 7.75,
                                        "Atene": 9,
                                        "Delfi": 8,
                                        "Zagabria": 8,
                                        "Lubiana": 7,
                }
        }
    },
#4
    {
        "question": "Qual è la materia da approfondire?",
        "options": {
            "Storia e Storia dell'arte": {"Firenze": 4, "Roma": 3},
            "Scienze": {"Napoli": 4, "Milano": 2},
            "Cultura generale/Esperienza": {"Milano": 5, "Roma": 2},
            "Lingua inglese": {"Milano": 5, "Roma": 2},
            "Lingua francese": {"Milano": 5, "Roma": 2},
            "Lingua spagnola": {"Milano": 5, "Roma": 2},
            "Lingua tedesca": {"Milano": 5, "Roma": 2}


        }
    },
#5
    {
        "question": "quanto è importante la differenza linguistica?",
        "options": {
            "Voglio l'italiano": {"Napoli": 5, "Roma": 3},
            "L'inglese va bene": {"Roma": 5, "Firenze": 3},
            "Classiche lingue di indirizzo": {"Milano": 5, "CERN": 1},
            "Qualsiasi lingua": {"Milano": 5, "CERN": 1}
        }
    },

#6
    {
        "question": "Quanto deve essere conosiuta la destinazione (in base al turismo)?",
        "options": {
            "Famosa": {"Napoli": 5, "Roma": 3},
            "Medioconosciuta": {"Roma": 5, "Firenze": 3},
            "Poco conosciuta": {"Milano": 5, "CERN": 1}
        }
    },
#7
    {
        "question": "Quanto turistica deve essere la città",
        "options": {
            "Famosa": {"Napoli": 5, "Roma": 3},
            "Medioconosciuta": {"Roma": 5, "Firenze": 3},
            "Poco conosciuta": {"Milano": 5, "CERN": 1}
        }
    },
#8
    {
        "question": "C'è un'attivita particolare tra le seguenti che si vuole svolgere?",
        "options": {
            "Bagno": {"Napoli": 5, "Roma": 3},
            "Sport specifici": {"Roma": 5, "Firenze": 3},
            "Trekking": {"Milano": 5, "CERN": 1}
        }
    },
#9
    {
        "question": "Quanti musei locali si vogliono visitare?",
        "options": {
            "Tanti": {"Napoli": 5, "Roma": 3},
            "Qualcosa sì": {"Roma": 5, "Firenze": 3},
            "Indifferente": {"Milano": 5, "CERN": 1}
        }
    },
#10
    {
        "question": "C'è uno stato in particolare da escludere?",
        "options": {
            "Inghilterra": {"Napoli": 5, "Roma": 3},
            "Italia": {"Roma": 5, "Firenze": 3},
            "Spagna": {"Milano": 5, "CERN": 1},
            "Portogallo": {"Milano": 5, "CERN": 1},
            "Francia": {"Milano": 5, "CERN": 1},
            "Germania": {"Milano": 5, "CERN": 1},
            "Paesi Bassi": {"Milano": 5, "CERN": 1},
            "Est europa": {"Milano": 5, "CERN": 1}

            
        }
    },

    
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    q_index = request.args.get('q', 0, type=int)

    answers = session.get('survey_answers')
    if not answers or len(answers) != len(questions):
        answers = [None] * len(questions)
    session['survey_answers'] = answers

    if request.method == 'POST':
        current_index = int(request.form.get('question_index'))
        answer = request.form.get('answer').strip()

        answers[current_index] = answer
        session['survey_answers'] = answers

        if current_index < len(questions) - 1:
            return redirect(url_for('survey', q=current_index + 1))
        else:
            # Elaborazione risultati
            for key in destinations:
                destinations[key] = 0
            for i, question in enumerate(questions):
                ans = answers[i]
                if ans in question["options"]:
                    for city, pts in question["options"][ans].items():
                        destinations[city] += pts
                else:
                    print("KeyError: La risposta non è valida:", repr(ans))

            max_score = max(destinations.values())
            best_destinations = [city for city, score in destinations.items() if score == max_score]
            chosen_destination = random.choice(best_destinations)
            session.pop('survey_answers', None)
            return redirect(url_for('destination', city=chosen_destination))

    current_question = questions[q_index]
    return render_template('survey.html',
                           question=current_question,
                           q_index=q_index,
                           total=len(questions),
                           form_action="/survey")

def localsurvey():
    q_index = request.args.get('q', 0, type=int)
    if 'local_survey_answers' not in session:
        session['local_survey_answers'] = [None] * len(local_questions)
    if request.method == 'POST':
        current_index = int(request.form.get('question_index'))
        answer = request.form.get('answer').strip()
        answers = session.get('local_survey_answers', [None] * len(local_questions))
        answers[current_index] = answer
        session['local_survey_answers'] = answers

        # Debug: stampa chiavi disponibili e risposta ricevuta
        available_keys = list(local_questions[current_index]["options"].keys())
        print("Domanda:", local_questions[current_index]["question"])
        print("Chiavi disponibili:", available_keys)
        print("Risposta ricevuta:", repr(answer))

        if current_index < len(local_questions) - 1:
            return redirect(url_for('localsurvey', q=current_index + 1))
        else:
            local_scores = {}
            for question in local_questions:
                for opt in question["options"].values():
                    for dest, pts in opt.items():
                        local_scores.setdefault(dest, 0)
            for i, question in enumerate(local_questions):
                ans = session['local_survey_answers'][i]
                if ans in question["options"]:
                    for dest, pts in question["options"][ans].items():
                        local_scores[dest] += pts
                else:
                    print("KeyError: La risposta non è valida:", repr(ans))
            max_score = max(local_scores.values())
            best_local_destinations = [dest for dest, score in local_scores.items() if score == max_score]
            chosen_destination = random.choice(best_local_destinations)
            session.pop('local_survey_answers', None)
            return redirect(url_for('destination', city=chosen_destination))
    current_question = local_questions[q_index]
    return render_template('survey.html',
                           question=current_question,
                           q_index=q_index,
                           total=len(local_questions),
                           form_action="/localsurvey")

@app.route('/destination/<city>')
def destination(city):
    return render_template('destination.html', city=city)

@app.route('/toggle_favorite', methods=['POST'])
def toggle_favorite():
    data = request.get_json()
    city = data.get('city')
    favorites = session.get('favorites', [])
    if city in favorites:
        favorites.remove(city)
        status = 'removed'
    else:
        favorites.append(city)
        status = 'added'
    session['favorites'] = favorites
    return jsonify({'status': status})

@app.route('/preferiti')
def preferiti():
    favorites = session.get('favorites', [])
    return render_template('preferiti.html', favorites=favorites)

@app.route('/lista')
def lista():
    # Mostra tutte le destinazioni in blocchi (4 per riga)
    destinations_list = list(destinations.keys())
    return render_template('list.html', destinations=destinations_list)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        sender_email = "lavoro.knod@gmail.com"  # Email del mittente
        receiver_email = "depalano.cope@gmail.com"  # Email del destinatario

        email_body = f"Da: {name}\n\nEmail: {email}\n\nMessaggio:\n{message}"

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, "ibnq iene tgiy lanv")  # Inserisci la password per l'app
            server.sendmail(sender_email, receiver_email, email_body)
            server.quit()
            return "Email inviata con successo!"
        except Exception as e:
            return f"Errore nell'invio: {str(e)}"
    
    return render_template('contact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea il database se non esiste
    app.run(host='0.0.0.0', port=5000, debug=True)
