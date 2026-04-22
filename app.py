"""
InsertCam — Suivi de l'insertion professionnelle des jeunes diplômés du Cameroun
TP INF232 EC2 | Python · Streamlit · SQLite · Plotly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import io
from database import init_db, insert_profil, get_all_profils, count_profils, seed_demo_data, get_summary_stats

@st.cache_data(ttl=60)
def load_data():
    return get_all_profils()

@st.cache_data(ttl=60)
def load_stats():
    return get_summary_stats()

# ── CONFIGURATION ────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="InsertCam | Insertion des Jeunes Diplômés",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@300;400;500;600&family=Outfit:wght@700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f8f9fb;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #003F2D 0%, #005F44 60%, #007A58 100%) !important;
}
section[data-testid="stSidebar"] * { color: #e0f2eb !important; }
section[data-testid="stSidebar"] .stRadio label { font-size: 0.95rem; padding: 4px 0; }

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #003F2D 0%, #006B4F 50%, #009966 100%);
    border-radius: 18px;
    padding: 2.4rem 3rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "🎓";
    font-size: 9rem;
    position: absolute;
    right: 2rem; top: -0.5rem;
    opacity: 0.1;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: #fff;
    margin: 0 0 0.4rem 0;
    letter-spacing: -1px;
}
.hero p { color: rgba(255,255,255,0.78); font-size: 1rem; margin: 0; }
.hero .badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.78rem;
    color: #fff;
    margin-bottom: 0.8rem;
    letter-spacing: 0.5px;
}

/* ── KPI CARDS ── */
.kpi-card {
    background: #fff;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    border-left: 5px solid #009966;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}
.kpi-card.red   { border-left-color: #CE1126; }
.kpi-card.gold  { border-left-color: #FCD116; }
.kpi-card.blue  { border-left-color: #2563EB; }
.kpi-label  { font-size: 0.78rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px; }
.kpi-value  { font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 800; color: #1a1a1a; line-height: 1; }
.kpi-sub    { font-size: 0.78rem; color: #6b7280; margin-top: 4px; }

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    color: #003F2D;
    margin: 1.6rem 0 1rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #e5e7eb;
}

/* ── FORM CARD ── */
.form-section {
    background: #fff;
    border-radius: 14px;
    padding: 1.8rem 2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    margin-bottom: 1.2rem;
}
.form-section h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #009966;
    margin: 0 0 1rem 0;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

/* ── SUCCESS / INFO ── */
.success-box {
    background: #d1fae5;
    border: 1px solid #6ee7b7;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    color: #065f46;
    font-weight: 500;
}

/* ── TABLE ── */
.dataframe thead th { background: #003F2D !important; color: #fff !important; }
.dataframe tbody tr:hover { background: #f0fdf4 !important; }
</style>
""", unsafe_allow_html=True)

# ── INIT ────────────────────────────────────────────────────────────────────

init_db()
seed_demo_data()

# ── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem 0;'>
        <div style='font-size:3rem;'>🎓</div>
        <div style='font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800;'>InsertCam</div>
        <div style='font-size:0.75rem; opacity:0.7; margin-top:4px;'>Insertion professionnelle<br>des jeunes diplômés</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["🏠  Tableau de bord", "📝  Soumettre mon profil",
         "📊  Analyse descriptive", "🗂️  Données collectées", "📤  Exporter les données"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    total = count_profils()
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.1); border-radius:10px; padding:0.8rem 1rem; text-align:center;'>
        <div style='font-size:0.72rem; opacity:0.7; margin-bottom:4px;'>PROFILS ENREGISTRÉS</div>
        <div style='font-family:Syne,sans-serif; font-size:2rem; font-weight:800;'>{total}</div>
    </div>
    """, unsafe_allow_html=True)

   st.markdown("""
    <div style='position:fixed; bottom:1rem; left:0; width:260px; text-align:center; font-size:0.72rem; line-height:1.7;'>
        <div style='width:60%; margin:0 auto 6px auto; border-top:1px solid rgba(255,255,255,0.25);'></div>
        <div style='font-weight:700; font-size:0.8rem; letter-spacing:0.5px;'>© 2024 InsertCam</div>
        <div style='opacity:0.65; font-size:0.68rem;'>Plateforme Nationale de Suivi<br>de l'Insertion Professionnelle<br>des Jeunes Diplômés du Cameroun<br><br>Développé par<br><strong>TENKAM</strong></div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — TABLEAU DE BORD
# ════════════════════════════════════════════════════════════════════════════

if "Tableau de bord" in page:

    st.markdown("""
    <div class="hero">
        <div class="badge">📍 CAMEROUN · 10 RÉGIONS</div>
        <h1>InsertCam</h1>
        <p>Plateforme nationale de suivi de l'insertion professionnelle des jeunes diplômés camerounais</p>
    </div>
    """, unsafe_allow_html=True)

    df = get_all_profils()

    if df.empty:
        st.info("Aucune donnée disponible. Commencez par soumettre un profil.")
        st.stop()

    # ── KPIs ──
    total       = len(df)
    employes    = len(df[df["statut_actuel"] == "Employé(e)"])
    auto_ent    = len(df[df["statut_actuel"] == "Auto-entrepreneur(e)"])
    taux_emploi = round((employes / total) * 100, 1) if total else 0
    moy_age     = round(df["age"].mean(), 1)
    regions_rep = df["region"].nunique()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Profils enregistrés</div>
            <div class="kpi-value">{total}</div>
            <div class="kpi-sub">{regions_rep} régions représentées</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card gold">
            <div class="kpi-label">Taux d'emploi</div>
            <div class="kpi-value">{taux_emploi}%</div>
            <div class="kpi-sub">{employes} diplômés employés</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card blue">
            <div class="kpi-label">Auto-entrepreneurs</div>
            <div class="kpi-value">{auto_ent}</div>
            <div class="kpi-sub">{round(auto_ent/total*100,1)}% des répondants</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card red">
            <div class="kpi-label">Âge moyen</div>
            <div class="kpi-value">{moy_age}</div>
            <div class="kpi-sub">ans · 15-35 ans</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">📊 Vue d\'ensemble</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            df, names="statut_actuel", hole=0.5,
            color_discrete_sequence=["#009966","#FCD116","#CE1126","#2563EB","#8b5cf6"],
            title="Situation actuelle des répondants"
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_family="Inter", title_font_size=14)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        reg_count = df["region"].value_counts().reset_index()
        reg_count.columns = ["Région","Profils"]
        fig2 = px.bar(
            reg_count, x="Profils", y="Région", orientation="h",
            color="Profils", color_continuous_scale=["#d1fae5","#009966","#003F2D"],
            title="Répartition par région"
        )
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_family="Inter", title_font_size=14, showlegend=False,
                           coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 — FORMULAIRE DE COLLECTE
# ════════════════════════════════════════════════════════════════════════════

elif "Soumettre" in page:

    st.markdown("""
    <div class="hero">
        <div class="badge">📝 FORMULAIRE DE COLLECTE</div>
        <h1>Mon Profil Professionnel</h1>
        <p>Renseignez votre parcours pour contribuer à l'étude nationale sur l'insertion des diplômés</p>
    </div>
    """, unsafe_allow_html=True)

    REGIONS = {
        "Centre":       ["Yaoundé I","Yaoundé II","Yaoundé III","Mbalmayo","Obala","Soa"],
        "Littoral":     ["Douala I","Douala II","Douala III","Nkongsamba","Edéa","Mbanga"],
        "Ouest":        ["Bafoussam","Dschang","Mbouda","Foumban","Baham"],
        "Nord":         ["Garoua","Guider","Figuil","Poli"],
        "Adamaoua":     ["Ngaoundéré","Meiganga","Tibati","Banyo"],
        "Est":          ["Bertoua","Batouri","Abong-Mbang","Yokadouma"],
        "Sud":          ["Ebolowa","Kribi","Sangmélima","Ambam"],
        "Nord-Ouest":   ["Bamenda","Kumbo","Wum","Ndop"],
        "Sud-Ouest":    ["Buea","Limbé","Kumba","Mamfe","Mundemba"],
        "Extrême-Nord": ["Maroua","Mora","Kousseri","Yagoua","Mokolo"],
    }

    NIVEAUX     = ["BTS/DUT","Licence (Bac+3)","Master (Bac+5)","Diplôme d'Ingénieur","Doctorat"]
    FILIERES    = sorted(["Informatique & Réseaux","Économie & Gestion","Droit","Médecine & Santé",
                  "Génie Civil & BTP","Sciences de l'Éducation","Agriculture & Agronomie",
                  "Comptabilité & Audit","Marketing & Commerce","Journalisme & Communication",
                  "Électronique & Télécoms","Chimie & Biochimie","Lettres & Sciences Humaines",
                  "Mathématiques & Physique","Sciences Politiques","Autre"])
    ETABLISSEMENTS = sorted(["Université de Yaoundé I","Université de Yaoundé II",
                    "Université de Douala","Université de Dschang","Université de Ngaoundéré",
                    "Université de Buea","Université de Bamenda","Université de Maroua",
                    "École Polytechnique de Yaoundé","ESSEC Douala","IUC","SUP'PTIC",
                    "ISTDI","ENSET Douala","ENAM","IRIC","Autre"])
    SECTEURS    = sorted(["Informatique & Télécoms","Finance & Banque","Santé & Pharmaceutique",
                  "Éducation & Formation","BTP & Immobilier","Agriculture & Agroalimentaire",
                  "Commerce & Distribution","Administration publique","Médias & Communication",
                  "ONG & Développement","Énergie & Mines","Transport & Logistique","Autre"])
    METHODES    = ["Candidatures en ligne (job boards)","Réseau personnel & familial",
                   "Agences d'emploi (FNE, ONEFOP)","Réseaux sociaux (LinkedIn, Facebook)",
                   "Recommandation d'un proche","Salon de l'emploi / Forum","Autre"]

    with st.form("form_profil", clear_on_submit=True):

        # ── SECTION 1 : IDENTITÉ ──
        st.markdown('<div class="form-section"><h3>👤 Identité</h3>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            nom    = st.text_input("Nom *", placeholder="Ex : Mbarga")
            age    = st.number_input("Âge *", min_value=18, max_value=45, value=25)
            region = st.selectbox("Région *", list(REGIONS.keys()))
        with c2:
            prenom = st.text_input("Prénom *", placeholder="Ex : Jean-Paul")
            sexe   = st.selectbox("Sexe *", ["Masculin","Féminin","Préfère ne pas répondre"])
            ville  = st.selectbox("Ville / District *", REGIONS[region])
        st.markdown("</div>", unsafe_allow_html=True)

        # ── SECTION 2 : FORMATION ──
        st.markdown('<div class="form-section"><h3>🎓 Formation académique</h3>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            niveau_etude   = st.selectbox("Niveau d'étude *", NIVEAUX)
            etablissement  = st.selectbox("Établissement *", ETABLISSEMENTS)
        with c2:
            filiere        = st.selectbox("Filière / Spécialité *", FILIERES)
            annee_diplome  = st.selectbox("Année d'obtention du diplôme *", list(range(2010, date.today().year + 1))[::-1])
        st.markdown("</div>", unsafe_allow_html=True)

        # ── SECTION 3 : RECHERCHE D'EMPLOI ──
        st.markdown('<div class="form-section"><h3>🔍 Recherche d\'emploi</h3>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            duree_recherche  = st.selectbox("Durée de recherche d'emploi *",
                ["Moins de 6 mois","6 à 12 mois","1 à 2 ans","Plus de 2 ans","Pas encore commencé"])
            nb_candidatures  = st.number_input("Nombre de candidatures envoyées", min_value=0, max_value=500, value=0)
        with c2:
            secteur_vise     = st.selectbox("Secteur d'activité visé *", SECTEURS)
            methodes_recherche = st.selectbox("Principale méthode de recherche *", METHODES)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── SECTION 4 : SITUATION ACTUELLE ──
        st.markdown('<div class="form-section"><h3>💼 Situation actuelle</h3>', unsafe_allow_html=True)
        statut_actuel = st.selectbox("Statut actuel *",
            ["En recherche d'emploi","Employé(e)","Auto-entrepreneur(e)","En stage","En formation complémentaire"])

        c1, c2, c3 = st.columns(3)
        with c1:
            type_contrat = st.selectbox("Type de contrat",
                ["—","CDI","CDD","Stage rémunéré","Freelance / Consultant","Temps partiel"],
                disabled=(statut_actuel != "Employé(e)"))
        with c2:
            salaire_fourchette = st.selectbox("Salaire mensuel estimé",
                ["Non applicable","Moins de 100 000 FCFA","100 000 – 200 000 FCFA",
                 "200 000 – 400 000 FCFA","400 000 – 700 000 FCFA","Plus de 700 000 FCFA"],
                disabled=(statut_actuel != "Employé(e)"))
        with c3:
            adequation = st.selectbox("Adéquation emploi / formation",
                ["—","Très bonne adéquation","Bonne adéquation","Adéquation partielle","Aucune adéquation"],
                disabled=(statut_actuel not in ["Employé(e)","Auto-entrepreneur(e)"]))
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("✅ Soumettre mon profil", use_container_width=True, type="primary")

    if submitted:
        errors = []
        if not nom.strip():   errors.append("Le nom est obligatoire.")
        if not prenom.strip(): errors.append("Le prénom est obligatoire.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            insert_profil({
                "nom": nom.strip(), "prenom": prenom.strip(),
                "age": age, "sexe": sexe, "region": region, "ville": ville,
                "niveau_etude": niveau_etude, "filiere": filiere,
                "etablissement": etablissement, "annee_diplome": annee_diplome,
                "duree_recherche": duree_recherche, "secteur_vise": secteur_vise,
                "methodes_recherche": methodes_recherche, "nb_candidatures": nb_candidatures,
                "statut_actuel": statut_actuel, "type_contrat": type_contrat,
                "salaire_fourchette": salaire_fourchette, "adequation": adequation,
            })
            st.markdown(f"""
            <div class="success-box">
                ✅ <strong>Merci {prenom} !</strong> Votre profil a été enregistré avec succès.
                Vos données contribuent à l'étude nationale sur l'insertion professionnelle des jeunes diplômés camerounais.
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 — ANALYSE DESCRIPTIVE
# ════════════════════════════════════════════════════════════════════════════

elif "Analyse" in page:

    st.markdown("""
    <div class="hero">
        <div class="badge">📊 STATISTIQUES & GRAPHIQUES</div>
        <h1>Analyse Descriptive</h1>
        <p>Visualisation et interprétation des données collectées sur l'insertion des diplômés</p>
    </div>
    """, unsafe_allow_html=True)

    df = get_all_profils()
    if df.empty:
        st.info("Aucune donnée à analyser pour le moment.")
        st.stop()

    # ── FILTRES ──
    with st.expander("🔽 Filtres", expanded=False):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            f_region  = st.multiselect("Région", sorted(df["region"].unique()), default=list(df["region"].unique()))
        with fc2:
            f_niveau  = st.multiselect("Niveau d'étude", sorted(df["niveau_etude"].unique()), default=list(df["niveau_etude"].unique()))
        with fc3:
            f_statut  = st.multiselect("Statut actuel", sorted(df["statut_actuel"].unique()), default=list(df["statut_actuel"].unique()))

    dff = df[df["region"].isin(f_region) & df["niveau_etude"].isin(f_niveau) & df["statut_actuel"].isin(f_statut)]
    st.caption(f"**{len(dff)}** profil(s) sélectionné(s)")

    # ── ROW 1 ──
    st.markdown('<div class="section-title">📌 Formation & Filières</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        niv = dff["niveau_etude"].value_counts().reset_index()
        niv.columns = ["Niveau","Effectif"]
        fig = px.bar(niv, x="Niveau", y="Effectif", color="Effectif",
                     color_continuous_scale=["#d1fae5","#009966","#003F2D"],
                     title="Distribution par niveau d'étude")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                          coloraxis_showscale=False, font_family="Inter", title_font_size=14)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_fil = dff["filiere"].value_counts().head(8).reset_index()
        top_fil.columns = ["Filière","Effectif"]
        fig2 = px.bar(top_fil, x="Effectif", y="Filière", orientation="h",
                      color="Effectif", color_continuous_scale=["#fef3c7","#FCD116","#b45309"],
                      title="Top 8 filières des répondants")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                           coloraxis_showscale=False, font_family="Inter", title_font_size=14)
        st.plotly_chart(fig2, use_container_width=True)

    # ── ROW 2 ──
    st.markdown('<div class="section-title">💼 Situation & Emploi</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        dur = dff["duree_recherche"].value_counts().reset_index()
        dur.columns = ["Durée","Effectif"]
        ORDER = ["Moins de 6 mois","6 à 12 mois","1 à 2 ans","Plus de 2 ans","Pas encore commencé"]
        dur["Durée"] = pd.Categorical(dur["Durée"], categories=ORDER, ordered=True)
        dur = dur.sort_values("Durée")
        fig3 = px.funnel(dur, x="Effectif", y="Durée",
                         color_discrete_sequence=["#CE1126"],
                         title="Durée de recherche d'emploi")
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter", title_font_size=14)
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        fig4 = px.histogram(dff, x="age", nbins=12, color="sexe",
                            color_discrete_map={"Masculin":"#009966","Féminin":"#FCD116",
                                                "Préfère ne pas répondre":"#6b7280"},
                            barmode="overlay", opacity=0.8,
                            title="Distribution des âges par sexe",
                            labels={"age":"Âge","count":"Effectif"})
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter", title_font_size=14)
        st.plotly_chart(fig4, use_container_width=True)

    # ── ROW 3 ──
    st.markdown('<div class="section-title">🌍 Géographie & Secteurs</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        sect = dff["secteur_vise"].value_counts().reset_index()
        sect.columns = ["Secteur","Effectif"]
        fig5 = px.pie(sect.head(7), names="Secteur", values="Effectif", hole=0.45,
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      title="Secteurs d'activité visés")
        fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_family="Inter", title_font_size=14)
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        taux_reg = (dff.groupby("region")
                    .apply(lambda x: round((x["statut_actuel"]=="Employé(e)").sum() / len(x) * 100, 1))
                    .reset_index(name="Taux d'emploi (%)"))
        fig6 = px.bar(taux_reg.sort_values("Taux d'emploi (%)"),
                      x="Taux d'emploi (%)", y="region", orientation="h",
                      color="Taux d'emploi (%)", color_continuous_scale=["#fecaca","#CE1126","#7f1d1d"],
                      title="Taux d'emploi par région (%)",
                      labels={"region":"Région"})
        fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                           coloraxis_showscale=False, font_family="Inter", title_font_size=14)
        st.plotly_chart(fig6, use_container_width=True)

    # ── STATS RÉSUMÉ ──
    st.markdown('<div class="section-title">📋 Statistiques descriptives — Âge & Candidatures</div>', unsafe_allow_html=True)
    stats = dff[["age","nb_candidatures"]].describe().round(2)
    stats.index = ["Effectif","Moyenne","Écart-type","Min","Q1 (25%)","Médiane (50%)","Q3 (75%)","Max"]
    st.dataframe(stats, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 — DONNÉES COLLECTÉES
# ════════════════════════════════════════════════════════════════════════════

elif "Données" in page:

    st.markdown("""
    <div class="hero">
        <div class="badge">🗂️ BASE DE DONNÉES</div>
        <h1>Données Collectées</h1>
        <p>Consultation de l'ensemble des profils enregistrés dans le système</p>
    </div>
    """, unsafe_allow_html=True)

    df = get_all_profils()

    if df.empty:
        st.info("Aucune donnée disponible.")
    else:
        st.caption(f"**{len(df)}** profil(s) enregistré(s)")

        search = st.text_input("🔍 Rechercher (nom, prénom, région, filière...)", "")
        if search:
            mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
            df   = df[mask]
            st.caption(f"**{len(df)}** résultat(s) pour « {search} »")

        cols_display = ["nom","prenom","age","sexe","region","ville","niveau_etude",
                        "filiere","statut_actuel","duree_recherche","secteur_vise","created_at"]
        st.dataframe(df[cols_display].rename(columns={
            "nom":"Nom","prenom":"Prénom","age":"Âge","sexe":"Sexe",
            "region":"Région","ville":"Ville","niveau_etude":"Niveau",
            "filiere":"Filière","statut_actuel":"Statut","duree_recherche":"Durée rech.",
            "secteur_vise":"Secteur visé","created_at":"Enregistré le"
        }), use_container_width=True, height=420)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 5 — EXPORT
# ════════════════════════════════════════════════════════════════════════════

elif "Exporter" in page:

    st.markdown("""
    <div class="hero">
        <div class="badge">📤 EXPORT DES DONNÉES</div>
        <h1>Télécharger les Données</h1>
        <p>Exportez l'ensemble des profils collectés pour analyse externe</p>
    </div>
    """, unsafe_allow_html=True)

    df = get_all_profils()

    if df.empty:
        st.info("Aucune donnée à exporter.")
    else:
        st.success(f"**{len(df)}** profil(s) prêt(s) à l'export.")

        c1, c2 = st.columns(2)

        with c1:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger en CSV",
                data=csv,
                file_name=f"insertcam_données_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with c2:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Profils")
                summary = df["statut_actuel"].value_counts().reset_index()
                summary.columns = ["Statut","Effectif"]
                summary.to_excel(writer, index=False, sheet_name="Résumé statuts")
            st.download_button(
                label="📥 Télécharger en Excel (.xlsx)",
                data=buffer.getvalue(),
                file_name=f"insertcam_données_{date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        st.markdown("---")
        st.markdown("**Aperçu des données :**")
        st.dataframe(df.head(10), use_container_width=True)
