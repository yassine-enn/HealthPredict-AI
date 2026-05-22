from flask import Flask, request, render_template_string
import os
import psycopg2


app = Flask(__name__)

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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        * {
            box-sizing: border-box;
            font-family: Arial, Helvetica, sans-serif;
        }

        body {
            margin: 0;
            min-height: 100vh;
            background: linear-gradient(135deg, #1f2937, #111827);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #111827;
        }

        .container {
            width: 100%;
            max-width: 420px;
            padding: 20px;
        }

        .card {
            background: #ffffff;
            border-radius: 18px;
            padding: 32px;
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.25);
        }

        .logo {
            width: 58px;
            height: 58px;
            border-radius: 16px;
            background: #2563eb;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 26px;
            font-weight: bold;
            margin: 0 auto 18px auto;
        }

        h1 {
            text-align: center;
            margin: 0;
            font-size: 26px;
            color: #111827;
        }

        .subtitle {
            text-align: center;
            color: #6b7280;
            font-size: 14px;
            margin: 10px 0 28px 0;
            line-height: 1.5;
        }

        label {
            display: block;
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 8px;
            color: #374151;
        }

        input {
            width: 100%;
            padding: 13px 14px;
            border: 1px solid #d1d5db;
            border-radius: 10px;
            font-size: 15px;
            outline: none;
            margin-bottom: 18px;
            transition: 0.2s;
        }

        input:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }

        button {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 10px;
            background: #2563eb;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            background: #1d4ed8;
            transform: translateY(-1px);
        }

        .message {
            margin-top: 22px;
            padding: 14px;
            border-radius: 10px;
            font-size: 14px;
            line-height: 1.5;
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

        .info-box {
            margin-top: 22px;
            padding: 14px;
            border-radius: 10px;
            background: #f3f4f6;
            color: #4b5563;
            font-size: 13px;
            line-height: 1.5;
        }

        .footer {
            text-align: center;
            margin-top: 18px;
            color: #9ca3af;
            font-size: 12px;
        }

        .user-card {
            margin-top: 16px;
            padding: 14px;
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
        }

        .user-card p {
            margin: 6px 0;
            font-size: 14px;
        }

        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 999px;
            background: #e0ecff;
            color: #1d4ed8;
            font-size: 12px;
            font-weight: bold;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="card">
            <div class="logo">U</div>

            <h1>Connexion</h1>
            <p class="subtitle">
                Accédez à votre espace utilisateur avec votre identifiant et votre mot de passe.
            </p>

            <form method="POST">
                <label for="username">Identifiant</label>
                <input
                    id="username"
                    name="username"
                    type="text"
                    placeholder="Exemple : admin"
                    required
                >

                <label for="password">Mot de passe</label>
                <input
                    id="password"
                    name="password"
                    type="password"
                    placeholder="Votre mot de passe"
                    required
                >

                <button type="submit">Se connecter</button>
            </form>

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
                <strong>TP sécurité :</strong> cette application contient volontairement une faiblesse SQL Injection.
                La requête SQL n'est plus affichée à l'écran, comme dans une application réelle.
            </div>
        </div>

        <div class="footer">
            Application de gestion d'utilisateurs — environnement local Docker
        </div>
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status = ""
    user_data = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Vulnérabilité volontaire pour le TP :
        # les entrées utilisateur sont concaténées directement dans la requête SQL.
        query = f"""
            SELECT id, username, email, role
            FROM users
            WHERE username = '{username}'
            AND password = '{password}'
        """

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query)
            user = cur.fetchone()

            cur.close()
            conn.close()

            if user:
                message = "Connexion réussie."
                status = "success"
                user_data = {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "role": user[3]
                }
            else:
                message = "Identifiant ou mot de passe incorrect."
                status = "error"

        except Exception:
            # Message volontairement générique pour éviter de révéler les erreurs SQL.
            message = "Une erreur est survenue pendant la connexion."
            status = "error"

    return render_template_string(
        HTML_TEMPLATE,
        message=message,
        status=status,
        user=user_data
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
