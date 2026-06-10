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
    <title>Connexion sécurisée - TP SQL Injection</title>
</head>
<body>
    <h1>Connexion sécurisée</h1>

    <form method="POST">
        <label>Identifiant</label>
        <input name="username" type="text" required>

        <label>Mot de passe</label>
        <input name="password" type="password" required>

        <button type="submit">Se connecter</button>
    </form>

    {% if message %}
        <p><strong>{{ message }}</strong></p>

        {% if user %}
            <p>Utilisateur : {{ user.username }}</p>
            <p>Email : {{ user.email }}</p>
            <p>Rôle : {{ user.role }}</p>
        {% endif %}
    {% endif %}
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

            return "Utilisateur créé"

        except Exception as e:
            return f"Erreur : {e}"

    return """
    <form method="POST">
        Username:<br>
        <input name="username"><br><br>

        Email:<br>
        <input name="email"><br><br>

        Password:<br>
        <input type="password" name="password"><br><br>

        <button type="submit">Créer le compte</button>
    </form>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)