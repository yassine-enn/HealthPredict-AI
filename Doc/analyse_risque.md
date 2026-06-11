# Analyse des vulnérabilités et gestion des risques

## 1. Cartographie des vulnérabilités du système

### Architecture du système

```text
Utilisateur
     ↓
Application Flask
     ↓
PostgreSQL
     ↓
Docker
     ↓
Prometheus / Grafana
```

### Vulnérabilités identifiées

| ID | Vulnérabilité | Description |
|----|---------------|-------------|
| V1 | SQL Injection | L'application utilisait une concaténation directe des entrées utilisateur dans les requêtes SQL. |
| V2 | Stockage des mots de passe en clair | Les mots de passe étaient stockés sans protection dans la base de données. |
| V3 | Absence de limitation des tentatives de connexion | Possibilité d'attaques par force brute. |
| V4 | Absence de HTTPS | Les identifiants peuvent être interceptés sur le réseau. |
| V5 | Exposition de PostgreSQL sur le port 5432 | Accès direct possible à la base depuis l'extérieur. |
| V6 | Journalisation insuffisante | Difficulté à détecter les comportements malveillants. |
| V7 | Gestion des privilèges limitée | Les utilisateurs disposent potentiellement de privilèges excessifs. |
| V8 | Absence d'authentification forte | Authentification basée uniquement sur un mot de passe. |

---

# 2. Identification des risques

## Risques liés aux accès non autorisés

| Risque | Cause |
|----------|----------|
| Contournement de l'authentification | SQL Injection |
| Vol de compte utilisateur | Force brute |
| Utilisation abusive des comptes | Mots de passe faibles |
| Accès administrateur non autorisé | Mauvaise gestion des privilèges |

---

## Risques liés aux fuites de données

| Risque | Cause |
|----------|----------|
| Exposition des données utilisateurs | Faille applicative |
| Vol des mots de passe | Base de données compromise |
| Interception des identifiants | Absence de HTTPS |
| Divulgation d'informations sensibles | Logs mal protégés |

---

## Risques liés aux pertes de données

| Risque | Cause |
|----------|----------|
| Suppression accidentelle | Erreur humaine |
| Corruption de la base | Incident logiciel |
| Perte après panne serveur | Absence de sauvegarde |
| Perte après attaque ransomware | Chiffrement malveillant des données |

---

## Risques liés aux mauvaises configurations Cloud / Docker

| Risque | Cause |
|----------|----------|
| Exposition des ports sensibles | Mauvaise configuration Docker |
| Accès non autorisés aux conteneurs | Contrôles insuffisants |
| Secrets exposés dans les fichiers de configuration | Mauvaise gestion des variables d'environnement |
| Surveillance insuffisante | Absence d'alertes et de monitoring |

---

# 3. Matrice des risques

| ID | Risque | Probabilité | Gravité | Criticité |
|----|---------|------------|----------|------------|
| R1 | SQL Injection | Élevée | Critique | Critique |
| R2 | Vol des mots de passe | Moyenne | Critique | Élevée |
| R3 | Force brute sur les comptes | Élevée | Élevée | Élevée |
| R4 | Accès non autorisé à PostgreSQL | Moyenne | Élevée | Élevée |
| R5 | Fuite de données utilisateurs | Moyenne | Critique | Élevée |
| R6 | Perte de données après panne | Faible | Critique | Moyenne |
| R7 | Mauvaise configuration Docker | Moyenne | Élevée | Élevée |
| R8 | Absence de supervision | Moyenne | Moyenne | Moyenne |
| R9 | Exposition des secrets d'application | Faible | Critique | Élevée |
| R10 | Interception des identifiants | Faible | Élevée | Moyenne |

---

## Échelle utilisée

### Probabilité

| Niveau | Description |
|----------|----------|
| Faible | Peu probable |
| Moyenne | Possible |
| Élevée | Très probable |

### Gravité

| Niveau | Description |
|----------|----------|
| Faible | Impact limité |
| Moyenne | Impact significatif |
| Élevée | Impact important |
| Critique | Impact majeur sur le système |

---

# 4. Recommandations de sécurité

## Priorité 1 — Critique

### Utilisation systématique des requêtes préparées

Objectif :

- empêcher les injections SQL
- protéger l'authentification

Justification :

La SQL Injection est la vulnérabilité la plus critique identifiée.

---

### Hachage des mots de passe avec bcrypt

Objectif :

- protéger les identifiants utilisateurs

Justification :

Empêche la récupération directe des mots de passe en cas de fuite de la base.

---

### Mise en place de sauvegardes automatiques

Objectif :

- limiter les pertes de données

Justification :

Permet une restauration rapide après incident.

---

## Priorité 2 — Élevée

### Limitation des tentatives de connexion

Objectif :

- bloquer les attaques par force brute

Mesures :

- verrouillage temporaire
- délai progressif
- CAPTCHA

---

### Restriction de l'accès à PostgreSQL

Objectif :

- empêcher les connexions non autorisées

Mesures :

- filtrage réseau
- limitation aux conteneurs internes
- suppression de l'exposition publique du port 5432

---

### Gestion des rôles et privilèges

Objectif :

- appliquer le principe du moindre privilège

Mesures :

- comptes dédiés
- rôles séparés
- limitation des droits administrateur

---

## Priorité 3 — Moyenne

### Mise en place du HTTPS

Objectif :

- protéger les données en transit

Justification :

Empêche l'interception des identifiants.

---

### Renforcement de la supervision

Objectif :

- détecter les comportements anormaux

Mesures :

- Grafana
- Prometheus
- alertes automatiques

---

### Centralisation des logs

Objectif :

- améliorer la détection des incidents

Mesures :

- logs applicatifs
- logs PostgreSQL
- logs Docker

---

# Conclusion

L'analyse du système a permis d'identifier plusieurs vulnérabilités affectant l'authentification, la protection des données et la configuration de l'infrastructure.

La vulnérabilité principale était la SQL Injection permettant le contournement de l'authentification. Cette faille a été corrigée grâce à l'utilisation de requêtes préparées et au hachage des mots de passe avec bcrypt.

La mise en place de la journalisation et de Grafana améliore également la capacité de détection des comportements anormaux et renforce la supervision globale du système.