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

# ---------------------------
# Form di Registrazione e Login
# ---------------------------
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Conferma Password', validators=[DataRequired(), EqualTo('password')])
    newsletter = BooleanField('Iscriviti alla Newsletter')
    submit = SubmitField('Registrati')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Ricordami')
    submit = SubmitField('Accedi')

# ---------------------------
# Rotte per autenticazione
# ---------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            newsletter=form.newsletter.data
        )
        db.session.add(new_user)
        db.session.commit()

        # QUI: Puoi aggiungere la logica per inviare una notifica via email se l'utente si iscrive alla newsletter

        flash("Registrazione avvenuta con successo! Ora puoi accedere.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Accesso effettuato con successo!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Credenziali non valide", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sei stato disconnesso.", "info")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# ---------------------------
# Funzionalità esistenti (Sondaggi, Destinazioni, Contatti)
# ---------------------------
# Destinazioni con punteggi assegnati
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
    {
        "question": "Qual è il principale obiettivo del viaggio?",
        "options": {
            "Cultura": {"Roma": 5, "Firenze": 3},
            "Scienza": {"CERN": 5, "Milano": 2},
            "Divertimento": {"Napoli": 5, "Milano": 3}
        }
    },
    {
        "question": "Qual è il budget della scuola?",
        "options": {
            "Basso": {"Napoli": 5, "Milano": 3},
            "Medio": {"Firenze": 4, "Roma": 3},
            "Alto": {"CERN": 5, "Roma": 4}
        }
    },
    {
        "question": "Quanto deve durare il viaggio?",
        "options": {
            "1-2 giorni": {"Milano": 5, "Firenze": 3},
            "3-4 giorni": {"Roma": 5, "CERN": 4},
            "Più di 4 giorni": {"Napoli": 5, "Roma": 4}
        }
    },
    {
        "question": "Quale tipo di attività preferisci durante il viaggio?",
        "options": {
            "Visita musei": {"Firenze": 4, "Roma": 3},
            "Attività all'aperto": {"Napoli": 4, "Milano": 2},
            "Shopping": {"Milano": 5, "Roma": 2}
        }
    },
    {
        "question": "Quale cibo ti piace di più?",
        "options": {
            "Pizza": {"Napoli": 5, "Roma": 3},
            "Pasta": {"Roma": 5, "Firenze": 3},
            "Risotto": {"Milano": 5, "CERN": 1}
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
        answers[current_index] = answer
        session['survey_answers'] = answers
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

@app.route('/localsurvey', methods=['GET', 'POST'])
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
