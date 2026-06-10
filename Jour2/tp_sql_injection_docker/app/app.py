from flask import Flask, request, render_template_string
import os
import psycopg2
import bcrypt
import logging

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "tp_users")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Connexion sécurisée</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        * {
            box-sizing: border-box;
            font-family: Inter, Arial, sans-serif;
        }

        body {
            margin: 0;
            min-height: 100vh;
            background:
                radial-gradient(circle at top left, #2563eb 0, transparent 35%),
                linear-gradient(135deg, #020617, #111827);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #111827;
        }

        .container {
            width: 100%;
            max-width: 430px;
            padding: 24px;
        }

        .card {
            background: rgba(255, 255, 255, 0.96);
            border-radius: 24px;
            padding: 34px;
            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(12px);
        }

        .logo {
            width: 64px;
            height: 64px;
            border-radius: 20px;
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 28px;
            margin: 0 auto 18px;
        }

        h1 {
            text-align: center;
            margin: 0;
            font-size: 28px;
        }

        .subtitle {
            text-align: center;
            color: #6b7280;
            font-size: 14px;
            margin: 10px 0 30px;
            line-height: 1.5;
        }

        label {
            display: block;
            font-size: 14px;
            font-weight: 700;
            color: #374151;
            margin-bottom: 8px;
        }

        input {
            width: 100%;
            padding: 14px;
            border: 1px solid #d1d5db;
            border-radius: 12px;
            font-size: 15px;
            margin-bottom: 18px;
            outline: none;
            transition: 0.2s;
            background: #f9fafb;
        }

        input:focus {
            background: white;
            border-color: #2563eb;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
        }

        button {
            width: 100%;
            border: none;
            padding: 15px;
            border-radius: 12px;
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            color: white;
            font-size: 16px;
            font-weight: 800;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(37, 99, 235, 0.35);
        }

        .message {
            margin-top: 22px;
            padding: 15px;
            border-radius: 14px;
            font-size: 14px;
        }

        .success {
            background: #dcfce7;
            color: #166534;
            border: 1px solid #86efac;
        }

        .error {
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }

        .user-card {
            margin-top: 14px;
            background: #f9fafb;
            border-radius: 12px;
            padding: 14px;
            border: 1px solid #e5e7eb;
        }

        .user-card p {
            margin: 6px 0;
        }

        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            background: #dbeafe;
            color: #1d4ed8;
            font-weight: 800;
            font-size: 12px;
        }

        .links {
            margin-top: 18px;
            text-align: center;
            font-size: 14px;
        }

        .links a {
            color: #2563eb;
            text-decoration: none;
            font-weight: 700;
        }

        .links a:hover {
            text-decoration: underline;
        }

        .info-box {
            margin-top: 22px;
            padding: 14px;
            border-radius: 14px;
            background: #f3f4f6;
            color: #4b5563;
            font-size: 13px;
            line-height: 1.5;
        }

        .footer {
            text-align: center;
            color: #9ca3af;
            font-size: 12px;
            margin-top: 18px;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="card">
            <div class="logo">HP</div>

            <h1>Connexion sécurisée</h1>
            <p class="subtitle">
                Accédez à votre espace utilisateur protégé contre les injections SQL.
            </p>

            <form method="POST">
                <label for="username">Identifiant</label>
                <input id="username" name="username" type="text" placeholder="Exemple : admin" required>

                <label for="password">Mot de passe</label>
                <input id="password" name="password" type="password" placeholder="Votre mot de passe" required>

                <button type="submit">Se connecter</button>
            </form>

            <div class="links">
                Pas encore de compte ?
                <a href="/register">Créer un compte</a>
            </div>

            {% if message %}
                <div class="message {{ status }}">
                    {{ message }}

                    {% if user %}
                        <div class="user-card">
                            <p><strong>Utilisateur :</strong> {{ user.username }}</p>
                            <p><strong>Email :</strong> {{ user.email }}</p>
                            <p><strong>Rôle :</strong> <span class="badge">{{ user.role }}</span></p>
                        </div>
                    {% endif %}
                </div>
            {% endif %}

            <div class="info-box">
                <strong>TP sécurité :</strong> authentification sécurisée avec bcrypt, requêtes préparées et journalisation.
            </div>
        </div>

        <div class="footer">
            HealthPredict-AI — Environnement local Docker
        </div>
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    user_data = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        ip = request.remote_addr

        try:
            conn = get_connection()
            cur = conn.cursor()

            query = """
                SELECT id, username, password_hash, email, role
                FROM users
                WHERE username = %s
            """

            cur.execute(query, (username,))
            user = cur.fetchone()

            cur.close()
            conn.close()

            if user is None:
                logging.warning(
                    f"LOGIN_FAILED ip={ip} username={username} reason=user_not_found"
                )
                message = "Identifiant ou mot de passe incorrect."
                return render_template_string(
                    HTML_TEMPLATE,
                    message=message,
                    user=user_data
                )

            stored_hash = user[2]

            password_valid = bcrypt.checkpw(
                password.encode("utf-8"),
                stored_hash.encode("utf-8")
            )

            if password_valid:
                logging.info(
                    f"LOGIN_SUCCESS ip={ip} username={username}"
                )

                message = "Connexion réussie."
                user_data = {
                    "id": user[0],
                    "username": user[1],
                    "email": user[3],
                    "role": user[4]
                }
            else:
                logging.warning(
                    f"LOGIN_FAILED ip={ip} username={username} reason=bad_password"
                )
                message = "Identifiant ou mot de passe incorrect."

        except Exception as e:
            logging.error(f"LOGIN_ERROR ip={ip} error={str(e)}")
            message = "Une erreur est survenue pendant la connexion."

    return render_template_string(
        HTML_TEMPLATE,
        message=message,
        user=user_data
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO users
                (username, password_hash, email, role)
                VALUES (%s, %s, %s, %s)
            """,
            (username, password_hash, email, "USER"))

            conn.commit()

            cur.close()
            conn.close()

            return """
<h2 style='font-family:Arial;text-align:center;margin-top:80px;color:green'>
✅ Compte créé avec succès
</h2>

<p style='text-align:center'>
<a href='/'>Se connecter</a>
</p>
"""

        except Exception as e:
            return f"Erreur : {e}"

    return """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Inscription sécurisée</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        *{
            box-sizing:border-box;
            font-family:Inter,Arial,sans-serif;
        }

        body{
            margin:0;
            min-height:100vh;
            display:flex;
            justify-content:center;
            align-items:center;
            background:
                radial-gradient(circle at top right,#7c3aed 0,transparent 30%),
                linear-gradient(135deg,#020617,#111827);
        }

        .container{
            width:100%;
            max-width:450px;
            padding:24px;
        }

        .card{
            background:white;
            border-radius:24px;
            padding:35px;
            box-shadow:0 25px 60px rgba(0,0,0,.35);
        }

        .logo{
            width:64px;
            height:64px;
            margin:auto;
            margin-bottom:18px;
            border-radius:18px;
            background:linear-gradient(135deg,#2563eb,#7c3aed);
            display:flex;
            justify-content:center;
            align-items:center;
            color:white;
            font-weight:bold;
            font-size:28px;
        }

        h1{
            text-align:center;
            margin:0;
            color:#111827;
        }

        .subtitle{
            text-align:center;
            color:#6b7280;
            margin-top:10px;
            margin-bottom:30px;
            font-size:14px;
        }

        label{
            display:block;
            margin-bottom:8px;
            font-weight:600;
            color:#374151;
        }

        input{
            width:100%;
            padding:14px;
            border:1px solid #d1d5db;
            border-radius:12px;
            margin-bottom:18px;
            font-size:15px;
            transition:.2s;
            background:#f9fafb;
        }

        input:focus{
            outline:none;
            border-color:#2563eb;
            background:white;
            box-shadow:0 0 0 4px rgba(37,99,235,.15);
        }

        button{
            width:100%;
            border:none;
            padding:15px;
            border-radius:12px;
            background:linear-gradient(135deg,#2563eb,#7c3aed);
            color:white;
            font-size:16px;
            font-weight:700;
            cursor:pointer;
            transition:.2s;
        }

        button:hover{
            transform:translateY(-2px);
            box-shadow:0 12px 25px rgba(37,99,235,.35);
        }

        .links{
            text-align:center;
            margin-top:20px;
        }

        .links a{
            color:#2563eb;
            text-decoration:none;
            font-weight:600;
        }

        .links a:hover{
            text-decoration:underline;
        }

        .footer{
            text-align:center;
            margin-top:18px;
            color:#9ca3af;
            font-size:12px;
        }
    </style>
</head>

<body>

<div class="container">

    <div class="card">

        <div class="logo">HP</div>

        <h1>Créer un compte</h1>

        <p class="subtitle">
            Inscription sécurisée avec hachage bcrypt des mots de passe.
        </p>

        <form method="POST">

            <label>Nom d'utilisateur</label>
            <input
                type="text"
                name="username"
                placeholder="Choisissez un identifiant"
                required
            >

            <label>Email</label>
            <input
                type="email"
                name="email"
                placeholder="exemple@email.com"
                required
            >

            <label>Mot de passe</label>
            <input
                type="password"
                name="password"
                placeholder="Choisissez un mot de passe"
                required
            >

            <button type="submit">
                Créer mon compte
            </button>

        </form>

        <div class="links">
            Déjà inscrit ?
            <a href="/">Se connecter</a>
        </div>

    </div>

    <div class="footer">
        HealthPredict-AI — TP Sécurité
    </div>

</div>

</body>
</html>
"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)