import csv
from datetime import datetime
from backend.database import get_db
from backend.models import Transaction


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


if __name__ == "__main__":
    # Spécifier le fichier CSV à lire
    csv_file = "transactions.csv"
    load_transactions_from_csv(csv_file)
