# HealthPredict-AI

```mermaid
flowchart LR
    subgraph EXT["External"]
        U{User}
    end

    subgraph APP["Application"]
        FE["Frontend<br/>(Web App - Health Questionnaire)"]
        API["API Backend"]
    end

    subgraph CLOUD["Cloud"]
        S3["Cloud Storage<br/>(AWS S3)"]
        ML["Machine Learning Model<br/>(Health Risk Prediction)"]
    end

    subgraph INT["Internal"]
        LOG["Logging System<br/>(logs, IP, navigation data)"]
        DASH["Internal Dashboard<br/>(for staff)"]
    end

    U -->|"Personal data<br/>(name, email, age)"| FE
    U ==>|"Sensitive health data<br/>(symptoms, medical history)"| FE

    FE -->|"Secure data transmission<br/>(HTTPS)"| API

    API -->|"Stores collected data<br/>(personal, health, technical)"| S3
    S3 -->|"Stored data<br/>for analysis / training"| ML

    API ==>|"Health data + personal data<br/>for risk analysis"| ML
    ML ==>|"Prediction results<br/>(health risk score)"| API

    API -->|"Prediction results"| FE
    FE -->|"Prediction results"| U

    API -.->|"Technical data<br/>(IP, logs, navigation)"| LOG

    API ==>|"Personal data + health data<br/>+ predictions"| DASH

    classDef external fill:#f4a3e8,stroke:#c13bb0,stroke-width:2px,color:#222;
    classDef app fill:#cfe2ff,stroke:#3b73d9,stroke-width:2px,color:#222;
    classDef cloud fill:#d9ead3,stroke:#4f8f3a,stroke-width:2px,color:#222;
    classDef internal fill:#fff2cc,stroke:#d6a100,stroke-width:2px,color:#222;
    classDef sensitive fill:#f8d7da,stroke:#dc3545,stroke-width:3px,color:#222;

    class U external;
    class FE,API app;
    class S3,ML cloud;
    class LOG,DASH internal;
    class ML,DASH sensitive;
```
# Liste des données classifiées – HealthPredict AI

## Description

L’application HealthPredict AI collecte et traite plusieurs types de données afin de prédire des risques de maladies via un modèle d’intelligence artificielle.

Ces données sont classées selon leur nature et leur niveau de sensibilité conformément aux principes du RGPD.

---

## Classification des données

| Donnée | Exemple | Type de donnée | Catégorie RGPD | Niveau de sensibilité | Finalité |
|-------|--------|---------------|----------------|----------------------|---------|
| Nom | Dupont | Identité | Donnée personnelle | Moyenne | Identifier l’utilisateur |
| Email | user@email.com | Contact | Donnée personnelle | Moyenne | Authentification / communication |
| Âge | 35 ans | Profil | Donnée personnelle | Moyenne | Analyse du risque |
| Symptômes | toux, fatigue | Santé | Donnée sensible | Très élevée | Analyse médicale par IA |
| Historique médical | maladies passées | Santé | Donnée sensible | Très élevée | Amélioration de la précision du modèle |
| Adresse IP | 192.168.x.x | Technique | Donnée personnelle | Moyenne | Sécurité / traçabilité |
| Logs | connexions, erreurs | Technique | Donnée technique | Faible à moyenne | Monitoring / audit |
| Navigation | pages visitées | Comportementale | Donnée personnelle | Moyenne | Amélioration UX |
| Prédiction IA | score de risque | Donnée dérivée | Donnée sensible | Très élevée | Résultat fourni à l’utilisateur |

---

## Données critiques

Les données suivantes sont considérées comme **hautement sensibles** :

- Données de santé :
  - symptômes
  - historique médical
- Données dérivées :
  - prédictions du modèle IA

Ces données nécessitent :
- un **consentement explicite**
- un **niveau de sécurité renforcé**
- une **gestion stricte des accès**

---

## Remarque

Les données de santé sont classées comme **données sensibles** selon le RGPD (article 9), ce qui implique des obligations légales strictes pour leur traitement et leur stockage.