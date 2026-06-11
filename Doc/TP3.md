# TP3 – Sécurisation d'une application vulnérable à la SQL Injection

## 1. Sécurisation de l'authentification

### 1.1 Mise en place du hachage des mots de passe

Afin de renforcer la sécurité des comptes utilisateurs, les mots de passe ne sont plus stockés en clair dans la base de données.

L'algorithme **bcrypt** a été utilisé pour :

- hacher les mots de passe lors de l'inscription ;
- vérifier les mots de passe lors de la connexion.

Exemple de génération du hash :

```python
password_hash = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")
```

Exemple de vérification :

```python
password_valid = bcrypt.checkpw(
    password.encode("utf-8"),
    stored_hash.encode("utf-8")
)
```

### Vérification

Après création de plusieurs utilisateurs, la table `users` contient uniquement des empreintes bcrypt :

```sql
SELECT username, password_hash
FROM users;
```

Résultat :

```text
admin   | $2b$12$...
yassine | $2b$12$...
user1   | $2b$12$...
test    | $2b$12$...
test2   | $2b$12$...
```

Les mots de passe ne sont donc plus stockés en clair.

---

### 1.2 Mise en place des requêtes préparées

#### Avant sécurisation

La requête SQL était construite par concaténation :

```python
query = f"""
    SELECT id, username, email, role
    FROM users
    WHERE username = '{username}'
    AND password = '{password}'
"""
```

Cette méthode est vulnérable aux injections SQL.

#### Après sécurisation

Une requête préparée est utilisée :

```python
query = """
    SELECT id, username, password_hash, email, role
    FROM users
    WHERE username = %s
"""

cur.execute(query, (username,))
```

Les entrées utilisateur sont traitées comme des données et non comme du code SQL.

---

# 2. Tests réalisés

## 2.1 Connexion valide

### Données utilisées

```text
Identifiant : test2
Mot de passe : ********
```

### Résultat

```text
Connexion réussie
```

### Conclusion

L'utilisateur est correctement authentifié.

---

## 2.2 Connexion invalide

### Données utilisées

```text
Identifiant : test2
Mot de passe : mauvaismotdepasse
```

### Résultat

```text
Identifiant ou mot de passe incorrect
```

### Conclusion

L'accès est refusé.

---

## 2.3 Vérification du fonctionnement avec des mots de passe hachés

Les utilisateurs peuvent toujours s'authentifier alors que les mots de passe stockés dans la base sont hachés.

Cela démontre le bon fonctionnement du mécanisme bcrypt.

---

# 3. Sécurité

## 3.1 Script SQL Injection utilisé au TP2

Exemple d'attaque :

```text
' OR '1'='1
```

ou

```text
admin' --
```

---

## 3.2 Résultats avant sécurisation

L'attaque permettait de contourner l'authentification.

Exemple :

```sql
SELECT *
FROM users
WHERE username = '' OR '1'='1'
AND password = 'test';
```

La condition devenait toujours vraie.

Résultat :

```text
Connexion réussie sans connaître le mot de passe.
```

---

## 3.3 Résultats après sécurisation

Résultat :

```text
Identifiant ou mot de passe incorrect.
```

L'accès est refusé.

---

## 3.4 Pourquoi l'attaque échoue ?

Les requêtes préparées séparent :

- le code SQL ;
- les données fournies par l'utilisateur.

L'entrée :

```text
' OR '1'='1
```

n'est plus interprétée comme du SQL mais comme une simple chaîne de caractères.

L'injection SQL devient donc impossible.

---

# 4. Journalisation

## 4.1 Logs applicatifs

Les événements suivants sont journalisés :

- connexions réussies ;
- connexions échouées ;
- erreurs applicatives ;
- erreurs SQL ;
- adresse IP de l'utilisateur.

Exemple :

```text
LOGIN_SUCCESS ip=172.20.0.1 username=test2

LOGIN_FAILED ip=172.20.0.1 username=test2 reason=bad_password

LOGIN_FAILED ip=172.20.0.1 username=' OR '1'='1 reason=user_not_found
```

---

## 4.2 Logs PostgreSQL

Les logs PostgreSQL ont été activés :

```yaml
command:
  - "postgres"
  - "-c"
  - "log_statement=all"
  - "-c"
  - "log_connections=on"
  - "-c"
  - "log_disconnections=on"
```

Exemples :

```text
LOG: connection received
LOG: statement: SELECT ...
LOG: disconnection
```

---

## 4.3 Logs Docker

Les logs des conteneurs sont consultables avec :

```bash
docker logs tp_flask_app
docker logs tp_postgres
```

Ces logs permettent de surveiller le fonctionnement global de l'application.

---

# 5. Supervision Grafana

## Architecture mise en place

```text
Flask
   ↓
PostgreSQL
   ↓
Postgres Exporter
   ↓
Prometheus
   ↓
Grafana
```

---

## Métriques PostgreSQL supervisées

Les métriques suivantes sont visualisées dans Grafana :

### Nombre de connexions

```promql
pg_stat_database_numbackends
```

### Transactions validées

```promql
rate(pg_stat_database_xact_commit[1m])
```

### Lectures disque

```promql
rate(pg_stat_database_blks_read[1m])
```

### Cache hits

```promql
rate(pg_stat_database_blks_hit[1m])
```

---

## Détection d'activités suspectes

Grafana permet d'identifier :

- une augmentation anormale des connexions ;
- un grand nombre d'échecs d'authentification ;
- une hausse des erreurs SQL ;
- une activité inhabituelle sur la base de données.

---

# Réponses aux questions d'analyse

## Quel est l'apport du hachage des mots de passe ?

Le hachage empêche le stockage des mots de passe en clair.

En cas de fuite de la base de données, les attaquants ne peuvent pas récupérer directement les mots de passe des utilisateurs.

---

## Pourquoi les requêtes préparées empêchent-elles une SQL Injection ?

Les requêtes préparées séparent le code SQL des données utilisateur.

Les entrées utilisateur sont interprétées comme des valeurs et non comme des commandes SQL.

---

## Le hachage seul protège-t-il contre cette attaque ?

Non.

Le hachage protège les mots de passe stockés mais ne bloque pas les injections SQL.

La protection contre les SQL Injection repose principalement sur l'utilisation des requêtes préparées.

---

## Quels événements doivent être journalisés ?

Les événements importants sont :

- connexions réussies ;
- connexions échouées ;
- erreurs SQL ;
- erreurs applicatives ;
- tentatives suspectes ;
- adresses IP ;
- accès aux ressources sensibles.

---

## Quelles métriques Grafana permettent de détecter une activité suspecte ?

Les métriques les plus utiles sont :

- nombre de connexions à PostgreSQL ;
- taux d'échec des connexions ;
- nombre de requêtes exécutées ;
- erreurs SQL ;
- activité disque ;
- activité mémoire ;
- temps de réponse des requêtes.

---

## Quelles recommandations proposeriez-vous pour renforcer la sécurité de l'application ?

- conserver l'utilisation de bcrypt ;
- utiliser systématiquement des requêtes préparées ;
- mettre en place une limitation des tentatives de connexion ;
- activer HTTPS ;
- mettre en place une authentification multifacteur (MFA) ;
- centraliser les logs ;
- surveiller les activités via Grafana ;
- réaliser régulièrement des audits de sécurité ;
- maintenir les dépendances à jour ;
- effectuer des sauvegardes régulières de la base de données.

---

# Conclusion

La sécurisation de l'application a permis d'éliminer la vulnérabilité SQL Injection identifiée lors du TP2.

L'utilisation de bcrypt protège les mots de passe stockés tandis que les requêtes préparées empêchent l'exécution de code SQL malveillant.

La mise en place des logs, de Prometheus et de Grafana améliore la visibilité sur le fonctionnement du système et facilite la détection d'activités suspectes.