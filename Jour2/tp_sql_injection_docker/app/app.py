import os
import psycopg2
from flask import Flask, request, render_template_string
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>TP SQL Injection</title>
</head>
<body>
    <h2>Connexion</h2>
    <form method="POST">
        <label>Identifiant</label><br>
        <input name="username" placeholder="admin"><br><br>

        <label>Mot de passe</label><br>
        <input name="password" type="password" placeholder="admin123"><br><br>

        <button type="submit">Se connecter</button>
    </form>

    <p><strong>{{ message }}</strong></p>

    {% if query %}
    <h3>Requête SQL exécutée</h3>
    <pre>{{ query }}</pre>
    {% endif %}
</body>
</html>
"""


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "tp_users"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    query = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Vulnérabilité volontaire pour le TP : concaténation directe des entrées utilisateur.
        query = f"SELECT id, username, email, role FROM users WHERE username = '{username}' AND password = '{password}'"

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query)
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                message = f"Connexion réussie : {user[1]} | email : {user[2]} | rôle : {user[3]}"
            else:
                message = "Identifiant ou mot de passe incorrect."
        except Exception as e:
            message = f"Erreur SQL : {e}"

    return render_template_string(HTML, message=message, query=query)


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
