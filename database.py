"""
database.py — Gestion SQLite pour InsertCam
"""

import sqlite3
import pandas as pd
import random
from datetime import date, timedelta

DB_PATH = "insertcam.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS profils (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            -- Identité
            nom                 TEXT NOT NULL,
            prenom              TEXT NOT NULL,
            age                 INTEGER NOT NULL,
            sexe                TEXT NOT NULL,
            region              TEXT NOT NULL,
            ville               TEXT NOT NULL,
            -- Formation
            niveau_etude        TEXT NOT NULL,
            filiere             TEXT NOT NULL,
            etablissement       TEXT NOT NULL,
            annee_diplome       INTEGER NOT NULL,
            -- Recherche emploi
            duree_recherche     TEXT NOT NULL,
            secteur_vise        TEXT NOT NULL,
            methodes_recherche  TEXT NOT NULL,
            nb_candidatures     INTEGER,
            -- Situation actuelle
            statut_actuel       TEXT NOT NULL,
            type_contrat        TEXT,
            salaire_fourchette  TEXT,
            adequation          TEXT,
            -- Meta
            created_at          TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def insert_profil(data: dict):
    conn = get_connection()
    now = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
        INSERT INTO profils (
            nom, prenom, age, sexe, region, ville,
            niveau_etude, filiere, etablissement, annee_diplome,
            duree_recherche, secteur_vise, methodes_recherche, nb_candidatures,
            statut_actuel, type_contrat, salaire_fourchette, adequation,
            created_at
        ) VALUES (
            :nom, :prenom, :age, :sexe, :region, :ville,
            :niveau_etude, :filiere, :etablissement, :annee_diplome,
            :duree_recherche, :secteur_vise, :methodes_recherche, :nb_candidatures,
            :statut_actuel, :type_contrat, :salaire_fourchette, :adequation,
            :created_at
        )
    """, {**data, "created_at": now})
    conn.commit()
    conn.close()


def get_all_profils() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM profils ORDER BY created_at DESC", conn)
    conn.close()
    return df


def count_profils() -> int:
    conn = get_connection()
    n = conn.execute("SELECT COUNT(*) FROM profils").fetchone()[0]
    conn.close()
    return n


def get_summary_stats() -> dict:
    conn = get_connection()
    c = conn.cursor()
    total    = c.execute("SELECT COUNT(*) FROM profils").fetchone()[0]
    employes = c.execute("SELECT COUNT(*) FROM profils WHERE statut_actuel='Employé(e)'").fetchone()[0]
    auto_ent = c.execute("SELECT COUNT(*) FROM profils WHERE statut_actuel='Auto-entrepreneur(e)'").fetchone()[0]
    regions  = c.execute("SELECT COUNT(DISTINCT region) FROM profils").fetchone()[0]
    conn.close()
    return {"total": total, "employes": employes, "auto_ent": auto_ent, "regions": regions}


def seed_demo_data():
    """Données de démonstration si la base est vide."""
    if count_profils() > 0:
        return

    random.seed(99)

    noms    = ["Mbarga","Nkomo","Fotso","Bello","Enow","Ndong","Ayuk","Tabi","Abba","Sali",
               "Kamga","Eto'o","Messi","Owona","Manga","Bekolo","Essama","Ngono","Biya","Ateba"]
    prenoms = ["Jean","Marie","Paul","Fatima","Pierre","Aïcha","Samuel","Grace","Moïse","Ruth",
               "Hervé","Laure","Boris","Sandra","Cédric","Lydie","Alain","Vanessa","Thierry","Inès"]
    regions = ["Centre","Littoral","Ouest","Nord","Adamaoua","Est","Sud","Nord-Ouest","Sud-Ouest","Extrême-Nord"]
    villes  = {"Centre":["Yaoundé","Mbalmayo","Obala"],"Littoral":["Douala","Nkongsamba","Edéa"],
               "Ouest":["Bafoussam","Dschang","Mbouda"],"Nord":["Garoua","Guider","Figuil"],
               "Adamaoua":["Ngaoundéré","Meiganga"],"Est":["Bertoua","Batouri"],
               "Sud":["Ebolowa","Kribi"],"Nord-Ouest":["Bamenda","Kumbo"],
               "Sud-Ouest":["Buea","Limbé","Kumba"],"Extrême-Nord":["Maroua","Mora","Kousseri"]}
    niveaux  = ["BTS/DUT","Licence (Bac+3)","Master (Bac+5)","Ingénieur","Doctorat"]
    filieres = ["Informatique & Réseaux","Économie & Gestion","Droit","Médecine & Santé",
                "Génie Civil & BTP","Sciences de l'Éducation","Agriculture","Comptabilité",
                "Marketing & Commerce","Journalisme & Communication"]
    etablissements = ["Université de Yaoundé I","Université de Yaoundé II","Université de Douala",
                      "Université de Dschang","Université de Ngaoundéré","École Polytechnique de Yaoundé",
                      "ESSEC Douala","IUC","SUP'PTIC","ISTDI"]
    secteurs   = ["Informatique & Télécoms","Finance & Banque","Santé","Éducation",
                  "BTP & Immobilier","Agriculture","Commerce & Distribution","Administration publique",
                  "Médias & Communication","ONG & Développement"]
    methodes   = ["Candidatures en ligne","Réseau personnel","Agences d'emploi (FNE/ONEFOP)",
                  "Réseaux sociaux (LinkedIn)","Recommandations","Salon de l'emploi"]
    statuts    = ["En recherche d'emploi","Employé(e)","Auto-entrepreneur(e)","En stage","En formation complémentaire"]
    contrats   = ["CDI","CDD","Stage","Freelance","Temps partiel"]
    salaires   = ["Moins de 100 000 FCFA","100 000 – 200 000 FCFA","200 000 – 400 000 FCFA",
                  "400 000 – 700 000 FCFA","Plus de 700 000 FCFA","Non applicable"]
    adequations= ["Très bonne adéquation","Bonne adéquation","Adéquation partielle","Aucune adéquation"]
    durees     = ["Moins de 6 mois","6 à 12 mois","1 à 2 ans","Plus de 2 ans"]

    conn = get_connection()
    now  = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    for _ in range(80):
        region = random.choice(regions)
        statut = random.choice(statuts)
        conn.execute("""
            INSERT INTO profils (
                nom,prenom,age,sexe,region,ville,
                niveau_etude,filiere,etablissement,annee_diplome,
                duree_recherche,secteur_vise,methodes_recherche,nb_candidatures,
                statut_actuel,type_contrat,salaire_fourchette,adequation,created_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            random.choice(noms), random.choice(prenoms),
            random.randint(21, 35),
            random.choice(["Masculin","Féminin"]),
            region, random.choice(villes[region]),
            random.choice(niveaux), random.choice(filieres),
            random.choice(etablissements), random.randint(2018, 2024),
            random.choice(durees), random.choice(secteurs),
            random.choice(methodes), random.randint(3, 150),
            statut,
            random.choice(contrats) if statut == "Employé(e)" else "—",
            random.choice(salaires) if statut == "Employé(e)" else "Non applicable",
            random.choice(adequations) if statut == "Employé(e)" else "—",
            now
        ))

    conn.commit()
    conn.close()
