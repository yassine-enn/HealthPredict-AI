# TP4 – Audit, Gouvernance et Amélioration Continue

# 1. Audit de l'application et de la base de données

## 1.1 Présentation de l'architecture

L'application repose sur l'architecture suivante :

```text
Utilisateur
     ↓
Application Flask
     ↓
PostgreSQL
     ↓
Docker
     ↓
Prometheus
     ↓
Grafana
```

Les composants principaux sont :

- Application web Flask
- Base de données PostgreSQL
- Conteneurs Docker
- Supervision Prometheus
- Visualisation Grafana

---

## 1.2 Analyse des logs

### Logs applicatifs

Les logs permettent de suivre :

- les connexions réussies ;
- les connexions échouées ;
- les erreurs applicatives ;
- les tentatives suspectes.

Exemples observés :

```text
LOGIN_SUCCESS ip=172.20.0.1 username=test2

LOGIN_FAILED ip=172.20.0.1 username=test2 reason=bad_password

LOGIN_FAILED ip=172.20.0.1 username=' OR '1'='1 reason=user_not_found
```

### Analyse

Les logs montrent :

- une traçabilité des accès ;
- la détection des tentatives d'authentification invalides ;
- l'identification des tentatives de SQL Injection.

---

### Logs PostgreSQL

Les journaux PostgreSQL permettent de suivre :

- les connexions ;
- les déconnexions ;
- les requêtes exécutées ;
- les erreurs SQL.

Exemples :

```text
LOG: connection received
LOG: statement: SELECT ...
LOG: disconnection
```

### Analyse

Les journaux montrent que :

- les requêtes sont exécutées correctement ;
- aucune erreur SQL critique n'a été observée ;
- les requêtes préparées empêchent l'exploitation de la SQL Injection.

---

### Logs Docker

Les logs Docker permettent de surveiller :

- le démarrage des services ;
- les erreurs de conteneurs ;
- les redémarrages inattendus.

Aucun comportement anormal n'a été détecté durant les tests.

---

## 1.3 Détection des comportements suspects

Les éléments suivants ont été recherchés :

- échecs répétés de connexion ;
- erreurs SQL ;
- tentatives d'injection ;
- pics inhabituels d'activité.

Résultat :

La tentative de SQL Injection utilisée lors du TP2 a été détectée et bloquée.

Aucune compromission du système n'a été observée.

---

# 2. Gouvernance des données

## 2.1 Identification des rôles

| Rôle | Responsabilités |
|--------|--------|
| Data Owner | Responsable métier des données |
| Data Steward | Garant de la qualité et de la cohérence des données |
| RSSI | Responsable de la sécurité du système d'information |
| DPO | Responsable de la conformité RGPD |
| Administrateur Base de Données | Gestion technique de PostgreSQL |
| Développeur | Maintenance de l'application |

---

## 2.2 Règles de gestion des données

Les règles suivantes sont appliquées :

- authentification obligatoire ;
- mots de passe hachés avec bcrypt ;
- utilisation de requêtes préparées ;
- journalisation des événements ;
- accès limités selon les rôles ;
- sauvegardes régulières.

---

## 2.3 Politique de gouvernance

### Objectifs

- assurer la qualité des données ;
- protéger les données utilisateurs ;
- garantir la conformité réglementaire ;
- assurer la disponibilité du système.

### Principes

- confidentialité ;
- intégrité ;
- disponibilité ;
- traçabilité ;
- responsabilité.

---

# 3. Stratégie de sauvegarde

## 3.1 Politique de sauvegarde

### Sauvegarde quotidienne

Une sauvegarde complète de la base PostgreSQL est réalisée chaque jour.

### Sauvegarde hebdomadaire

Une sauvegarde complète est conservée chaque semaine.

### Sauvegarde mensuelle

Une sauvegarde est conservée à long terme.

---

## 3.2 Durée de conservation

| Type | Conservation |
|--------|--------|
| Quotidienne | 7 jours |
| Hebdomadaire | 4 semaines |
| Mensuelle | 12 mois |

---

## 3.3 Procédure de restauration

### Export

```bash
pg_dump -U postgres tp_users > backup.sql
```

### Restauration

```bash
psql -U postgres tp_users < backup.sql
```

---

## Justification

Cette stratégie permet :

- une restauration rapide ;
- une limitation des pertes de données ;
- une couverture des incidents majeurs.

---

# 4. Évaluation des mesures de sécurité

## Mesures mises en place

| Mesure | État |
|-----------|-----------|
| Hachage bcrypt | Mis en place |
| Requêtes préparées | Mis en place |
| Logs applicatifs | Mis en place |
| Logs PostgreSQL | Mis en place |
| Docker | Mis en place |
| Grafana | Mis en place |
| Prometheus | Mis en place |

---

## Efficacité observée

### SQL Injection

Avant :

```text
Connexion contournée avec succès.
```

Après :

```text
Identifiant ou mot de passe incorrect.
```

La vulnérabilité est corrigée.

---

### Protection des mots de passe

Avant :

```text
Mot de passe stocké en clair.
```

Après :

```text
Hash bcrypt stocké.
```

La confidentialité des identifiants est améliorée.

---

# 5. Plan d'amélioration

## Priorité 1

### Mise en place du HTTPS

Objectif :

- sécuriser les communications réseau.

---

### Limitation des tentatives de connexion

Objectif :

- réduire les attaques par force brute.

---

### Politique de mots de passe renforcée

Objectif :

- améliorer la robustesse des comptes utilisateurs.

---

## Priorité 2

### Gestion des rôles

Objectif :

- appliquer le principe du moindre privilège.

---

### Sauvegardes automatisées

Objectif :

- réduire les risques de perte de données.

---

### Alertes Grafana

Objectif :

- détecter rapidement les comportements anormaux.

---

## Priorité 3

### Authentification multifacteur (MFA)

Objectif :

- renforcer l'authentification.

---

### Centralisation avancée des logs

Objectif :

- améliorer l'analyse de sécurité.

---

# Réponses aux questions d'analyse

## Les mesures mises en place sont-elles suffisantes ?

Les mesures actuelles corrigent la vulnérabilité principale identifiée lors du TP2.

Cependant, des améliorations restent possibles :

- HTTPS ;
- MFA ;
- limitation des tentatives ;
- alertes automatiques.

---

## Quels indicateurs permettent d'évaluer la sécurité de l'application ?

Les principaux indicateurs sont :

- nombre de connexions réussies ;
- nombre d'échecs d'authentification ;
- nombre d'erreurs SQL ;
- nombre de requêtes exécutées ;
- activité de la base de données ;
- disponibilité des services.

---

## Pourquoi l'audit est-il essentiel ?

L'audit permet :

- d'évaluer l'efficacité des mesures de sécurité ;
- de détecter les vulnérabilités résiduelles ;
- d'améliorer continuellement le système ;
- de démontrer la conformité et la maîtrise des risques.

---

## Quelle stratégie de sauvegarde recommander ?

Une stratégie de type :

- sauvegarde quotidienne ;
- conservation hebdomadaire ;
- archivage mensuel ;
- tests réguliers de restauration.

Cette approche garantit la disponibilité des données tout en limitant les pertes potentielles.

---

## Quelles actions proposer pour améliorer la sécurité ?

- activer HTTPS ;
- déployer le MFA ;
- renforcer la politique de mots de passe ;
- mettre en place des alertes Grafana ;
- automatiser les sauvegardes ;
- réaliser des audits réguliers ;
- appliquer le principe du moindre privilège.

---

# Conclusion

L'audit réalisé montre que les principales vulnérabilités identifiées lors des TP précédents ont été corrigées.

L'introduction du hachage bcrypt, des requêtes préparées, de la journalisation et de la supervision Grafana améliore significativement la sécurité globale du système.

Des améliorations complémentaires peuvent encore être mises en œuvre afin d'atteindre un niveau de maturité supérieur en matière de cybersécurité et de gouvernance des données.