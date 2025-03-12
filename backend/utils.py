import os
import csv
from datetime import datetime
from backend.database import get_db
from backend.models import Transaction, Sale, Customer, CustomerTransaction


def load_transactions_from_csv(csv_file: str):
    """
    Intègre les transactions depuis un fichier CSV dans la table PostgreSQL.
    """
    # Obtenir une session DB avec get_db
    db_generator = get_db()
    db = next(db_generator)  # Utiliser le générateur pour démarrer une session

    try:
        with open(csv_file, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=';')  # Lire le CSV avec entêtes comme clés de dictionnaire
            transactions = []

            for row in reader:
                # Créer une instance de Transaction pour chaque ligne avec gestion des types
                transaction = Transaction(
                    transaction_id=int(row["transaction_id"]) if row["transaction_id"] else None,
                    etf_symbol=row["etf_symbol"],
                    amount=float(row["amount"]),
                    transaction_date=datetime.strptime(row["transaction_date"], "%d/%m/%Y %H:%M"),
                    parent_transaction_id=int(row["parent_transaction_id"]) if row["parent_transaction_id"]
                                                                               and row[
                                                                                   "parent_transaction_id"] != "NULL"
                    else None,
                )
                transactions.append(transaction)

            # Ajouter toutes les transactions dans la session
            db.add_all(transactions)
            db.commit()  # Valider les changements
            print(f"{len(transactions)} transactions ont été insérées avec succès.")
    except Exception as e:
        db.rollback()  # Annuler les modifications en cas d'erreur
        print(f"Erreur pendant l'intégration du CSV : {e}")
    finally:
        db.close()  # Toujours fermer la session DB
        print("Session fermée.")

def load_sales_from_csv(csv_file: str):
    """
    Charge les données des ventes depuis un fichier CSV et les insère dans la base PostgreSQL.
    """
    # Obtenir une session DB avec get_db
    db_generator = get_db()
    db = next(db_generator)  # Obtenez une instance de session

    try:
        # Ouvrir le fichier CSV
        with open(csv_file, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=';')  # Lire le CSV avec entêtes comme clés de dictionnaire
            sales = []

            for row in reader:
                # Créez une instance de Sale pour chaque ligne avec gestion des types
                sale = Sale(
                    sale_id=int(row["sale_id"]),
                    region=row["region"],
                    amount=float(row["amount"]),
                    sale_date=datetime.strptime(row["sale_date"], "%d/%m/%Y"),
                    etf_symbol=row["etf_symbol"]
                )
                sales.append(sale)

            # Ajouter toutes les ventes dans la session
            db.add_all(sales)
            db.commit()  # Valider les changements
            print(f"{len(sales)} ventes ont été insérées avec succès.")
    except Exception as e:
        db.rollback()  # Annuler les modifications en cas d'erreur
        print(f"Erreur pendant l'intégration du CSV : {e}")
    finally:
        db.close()  # Toujours fermer la session DB
        print("Session fermée.")

def load_customers_from_csv(csv_file: str):
    """
    Charge les données des clients depuis un fichier CSV et les insère dans la table PostgreSQL customers.
    """
    # Obtenir une session DB avec get_db
    db_generator = get_db()
    db = next(db_generator)  # Utiliser le générateur pour créer une session

    try:
        with open(csv_file, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=';')  # Lire le CSV avec des entêtes comme dictionnaire
            customers = []

            for row in reader:
                # Créer une instance Customer à partir de chaque ligne
                customer = Customer(
                    customer_id=int(row["customer_id"]),
                    name=row["name"],
                    signup_date=datetime.strptime(row["signup_date"], "%d/%m/%Y"),  # Convertir la date
                    country=row["country"]
                )
                customers.append(customer)

            # Ajouter tous les clients dans la session
            db.add_all(customers)
            db.commit()  # Valider les changements
            print(f"{len(customers)} clients ont été insérés avec succès.")
    except Exception as e:
        db.rollback()  # Annuler les modifications en cas d'erreur
        print(f"Erreur pendant l'intégration du fichier CSV des clients : {e}")
    finally:
        db.close()  # Toujours fermer la session
        print("Session fermée.")

def load_customer_transactions_from_csv(csv_file: str):
    # Obtenir une session DB avec get_db
    db_generator = get_db()
    db = next(db_generator)  # Utiliser le générateur pour démarrer une session

    try:
        with open(csv_file, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=';')  # Lire le CSV avec des colonnes/entêtes
            customer_transactions = []

            for row in reader:
                # Créer une instance de CustomerTransaction pour chaque ligne du CSV
                customer_transaction = CustomerTransaction(
                    transaction_id=int(row["transaction_id"]),
                    customer_id=int(row["customer_id"]),
                    amount=float(row["amount"]),
                    transaction_date=datetime.strptime(row["transaction_date"], "%d/%m/%Y"),  # Format DD/MM/YYYY
                    etf_symbol=row["etf_symbol"]
                )
                customer_transactions.append(customer_transaction)

            # Ajouter tous les enregistrements à la session
            db.add_all(customer_transactions)
            db.commit()  # Valider les changements
            print(f"{len(customer_transactions)} transactions clients ont été insérées avec succès.")
    except Exception as e:
        db.rollback()  # Annuler les modifications en cas d'erreur
        print(f"Erreur pendant l'intégration des transactions clients depuis le CSV : {e}")
    finally:
        db.close()  # Toujours fermer la session
        print("Session fermée.")

if __name__ == "__main__":
    # Spécifier le fichier CSV à lire

    # base_dir = os.path.dirname(__file__)
    # csv_file = os.path.join(base_dir, "task1_services", "transactions.csv")
    # load_transactions_from_csv(csv_file)

    # base_dir = os.path.dirname(__file__)
    # csv_file = os.path.join(base_dir, "task2_services", "sales.csv")
    # load_sales_from_csv(csv_file)

    # base_dir = os.path.dirname(__file__)
    # csv_file = os.path.join(base_dir, "task3_services", "customers.csv")
    # load_customers_from_csv(csv_file)

    base_dir = os.path.dirname(__file__)
    csv_file = os.path.join(base_dir, "task3_services", "customers_transaction.csv")
    load_customer_transactions_from_csv(csv_file)



