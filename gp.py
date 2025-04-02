from flask import Flask, render_template, request, redirect, url_for, session
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
 app.secret_key = 'una_chiave_segreta'  # Necessaria per usare session
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
 
 # 📍 Destinazioni con punteggi assegnati
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
 @@ -214,6 +312,7 @@ def survey():
                            q_index=q_index,
                            total=len(questions),
                            form_action="/survey")
 
 @app.route('/localsurvey', methods=['GET', 'POST'])
 def localsurvey():
     q_index = request.args.get('q', 0, type=int)
 @@ -259,7 +358,6 @@ def localsurvey():
                            total=len(local_questions),
                            form_action="/localsurvey")
 
 
 @app.route('/destination/<city>')
 def destination(city):
     return render_template('destination.html', city=city)
 @@ -268,23 +366,21 @@ def destination(city):
 def about():
     return render_template('about.html')
 
 
 @app.route('/contact', methods=['GET', 'POST'])
 def contact():
     if request.method == 'POST':
         name = request.form.get("name")
         email = request.form.get("email")  # Ora prendi l'email
         email = request.form.get("email")
         message = request.form.get("message")
         sender_email = "lavoro.knod@gmail.com"  # L'email del mittente
         receiver_email = "depalano.cope@gmail.com"  # L'email del destinatario
         sender_email = "lavoro.knod@gmail.com"  # Email del mittente
         receiver_email = "depalano.cope@gmail.com"  # Email del destinatario
 
         # Aggiungi l'email dell'utente al corpo del messaggio
         email_body = f"Da: {name}\n\nEmail: {email}\n\nMessaggio:\n{message}"
 
         try:
             server = smtplib.SMTP("smtp.gmail.com", 587)
             server.starttls()
             server.login(sender_email, "ibnq iene tgiy lanv")  # Inserisci la tua password per l'app
             server.login(sender_email, "ibnq iene tgiy lanv")  # Inserisci la password per l'app
             server.sendmail(sender_email, receiver_email, email_body)
             server.quit()
             return "Email inviata con successo!"
 @@ -293,7 +389,7 @@ def contact():
 
     return render_template('contact.html')
 
 
 
 if __name__ == '__main__':
     with app.app_context():
         db.create_all()  # Crea il database se non esiste
     app.run(host='0.0.0.0', port=5000, debug=True)
