# Matrice des risques — HealthPredict

| ID | Risque identifié | Causes possibles | Probabilité | Impact | Niveau de risque | Mesures recommandées |
|---|---|---|---|---|---|---|
| R1 | Fuite de données médicales | Mauvaise configuration cloud, faille API, absence de chiffrement | Élevée | Critique | Critique | Chiffrement, contrôle d’accès strict, audits sécurité |
| R2 | Accès abusif interne | Trop d’accès employés, absence de contrôle des permissions | Élevée | Élevé | Critique | RBAC, journalisation, principe du moindre privilège |
| R3 | Mauvaise configuration AWS S3 | Erreur humaine, permissions publiques | Moyenne | Critique | Élevé | Configuration privée par défaut, audits cloud |
| R4 | Transfert de données hors UE | Utilisation d’un cloud américain soumis au Cloud Act | Moyenne | Critique | Élevé | SCC, chiffrement, hébergement européen |
| R5 | Utilisation des données IA sans consentement clair | Finalités mal définies | Moyenne | Élevé | Élevé | Consentement explicite, anonymisation |
| R6 | Conservation excessive des données | Absence de politique de rétention | Élevée | Moyen | Élevé | Suppression automatique, durée de conservation définie |
| R7 | Absence de DPIA/AIPD | Gouvernance RGPD insuffisante | Élevée | Élevé | Critique | Réaliser une analyse d’impact RGPD |
| R8 | Vol d’identifiants administrateurs | Phishing, mots de passe faibles, absence MFA | Moyenne | Critique | Élevé | MFA obligatoire, gestion IAM stricte |
| R9 | Attaque ransomware | Vulnérabilités ou phishing | Moyenne | Critique | Critique | Sauvegardes, segmentation réseau, EDR |
| R10 | Faille applicative web | Vulnérabilités XSS, SQLi, API non sécurisée | Moyenne | Élevé | Élevé | Pentests, DevSecOps, sécurisation API |