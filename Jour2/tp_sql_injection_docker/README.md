# TP SQL Injection dockerisé

Projet volontairement vulnérable pour comprendre une injection SQL dans un environnement local contrôlé.

## Lancer le projet

```bash
docker compose up --build
```

Application : http://127.0.0.1:5000

## Tests manuels

Connexion valide :

```text
username = admin
password = admin123
```

Connexion invalide :

```text
username = admin
password = fauxmotdepasse
```

Injection SQL :

```text
username = admin' --
password = test
```

Autre injection :

```text
username = admin' OR '1'='1' --
password = test
```

## Lancer les tests automatiques

Dans un autre terminal :

```bash
pip install requests
python tests/test_injections.py
```

## Correction sécurisée

Remplacer la requête vulnérable :

```python
query = f"SELECT id, username, email, role FROM users WHERE username = '{username}' AND password = '{password}'"
cur.execute(query)
```

par une requête préparée :

```python
query = "SELECT id, username, email, role FROM users WHERE username = %s AND password = %s"
cur.execute(query, (username, password))
```
