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
    "UNK": 0,
    "UNK": 0,
    "UNK": 0,
    "UNK": 0,
    "UNK": 0,
    "UNK": 0,
    "UNK": 0,
    "UNK": 0,
    "UNK": 0,
    "UNK": 0,
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
            "Caldo": {"CERN": 5, "Milano": 2},
            "Freddo": {"Napoli": 5, "Milano": 3},
            "Moderato": {"Napoli": 5, "Milano": 3}
        }
    },
#2
    {
        "question": "Qual è il metodo di trasporto voluto (il tipo di mezzo influisce sul prezzo)?",
        "options": {
            "Pullman": {"Napoli": 5, "Milano": 3},
            "Treno": {"Firenze": 4, "Roma": 3},
            "Aereo": {"CERN": 5, "Roma": 4}
        }
    },
#3
    {
        "question": "Quanto deve durare il viaggio?",
        "options": {
            "1-2 giorni": {"Milano": 5, "Firenze": 3},
            "3-4 giorni": {"Roma": 5, "CERN": 4},
            "Più di 4 giorni": {"Napoli": 5, "Roma": 4}
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
    if 'survey_answers' not in session:
        session['survey_answers'] = [None] * len(questions)
        
    if request.method == 'POST':
        current_index = int(request.form.get('question_index'))
        answer = request.form.get('answer').strip()
        answers = session.get('survey_answers', [None] * len(questions))
        
        if 0 <= current_index < len(answers):
            answers[current_index] = answer
            session['survey_answers'] = answers
        else:
            print("Indice domanda fuori range, si continua comunque.")
            return "Errore: indice domanda non valido", 400

        if current_index < len(questions) - 1:
            return redirect(url_for('survey', q=current_index + 1))
        else:
            for key in destinations:
                destinations[key] = 0
            for i, question in enumerate(questions):
                ans = session['survey_answers'][i]
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
