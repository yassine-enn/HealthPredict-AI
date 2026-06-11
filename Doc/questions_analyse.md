# Questions d'analyse

## Quelle est la vulnérabilité exploitée ?

La vulnérabilité exploitée est une **SQL Injection**.

L’utilisateur peut injecter du code SQL dans les champs du formulaire car les entrées ne sont pas sécurisées avant d’être envoyées à la base de données.

---

## Pourquoi l’application accepte une connexion invalide ?

L’application accepte la connexion car l’injection SQL modifie la logique de la requête.

Avec :

```sql
admin' --
```

la condition :

```sql
AND password = '...'
```

est ignorée.

La requête ne vérifie plus le mot de passe.

---

## Quelles données peuvent être compromises ?

Un attaquant pourrait accéder :

- aux comptes utilisateurs ;
- aux adresses email ;
- aux mots de passe ;
- aux rôles administrateurs ;
- aux données internes de l’entreprise.

Dans certains cas, il pourrait aussi :
- modifier des données ;
- supprimer des tables ;
- récupérer toute la base de données.

---

## Cette faille vient-elle de la base de données ou de l’application ?

La faille vient principalement de l’application.

PostgreSQL fonctionne correctement.

Le problème provient du code applicatif qui construit les requêtes SQL de manière non sécurisée.

---

## Quels sont les risques pour une entreprise ?

Les risques sont importants :

- vol de données sensibles ;
- compromission de comptes administrateurs ;
- fuite d’informations confidentielles ;
- suppression ou modification de données ;
- interruption de service ;
- atteinte à l’image de l’entreprise ;
- sanctions légales liées à la protection des données.

Une SQL Injection peut permettre à un attaquant de prendre le contrôle complet d’une application connectée à une base de données.
