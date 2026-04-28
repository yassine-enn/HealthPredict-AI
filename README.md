# HealthPredict-AI

flowchart LR
  subgraph External
    U["User"]
  end

  subgraph Application
    W["Web Application (Health Questionnaire)"]
    A["API Backend"]
  end

  subgraph Cloud
    S["Cloud Storage (AWS S3)"]
    M["Machine Learning Model (Health Risk Prediction)"]
  end

  subgraph Internal
    D["Internal Dashboard (for staff)"]
    L["Logging System (logs, IP, navigation data)"]
  end

  U -->|"Personal data (name, email, age)"| W
  U -->|"Sensitive health data (symptoms, medical history)"| W
  W -->|"Secure data transmission (HTTPS)"| A
  A -->|"Stores all collected data"| S
  A -->|"Data for analysis"| M
  M -->|"Prediction results"| A
  A -->|"Prediction results"| U
  A -->|"User data and predictions"| D
  A -->|"Technical data (IP, logs, navigation)"| L