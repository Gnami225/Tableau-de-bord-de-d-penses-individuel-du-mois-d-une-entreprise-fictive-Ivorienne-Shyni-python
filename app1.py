import faicons as fa
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# chargement des données et outils
from shared import app_dir, df, df_depenses 
from shinywidgets import output_widget, render_plotly
from shiny import App, reactive, render, ui
#technique page 1
imat = df['Immatriculation'].tolist()  
imat_dict = {var: var for var in imat}

type = df['Type de camion'].tolist() 
badge = df['BADGE ASSOCIE'].tolist()
police_assurance = badge = df['POLICE ASSURANCE'].tolist()
expiration_assurance = df['EXPIRATION ASSURANCE'].tolist()
vidange = df['VIDANGE'].tolist()
Chantier = df['Chantier'].tolist()
carteg = df['CARTE GRISE'].tolist()
expiration_transport = df["EXPIRATION CARTE DE TRANSPORT"]
entete = df_depenses.columns

ICONS = {
    "user": fa.icon_svg("user", "regular",{"style": "color: orange;"}),
    "wallet": fa.icon_svg("wallet"),
    "ellipsis": fa.icon_svg("ellipsis"),
    "camion": fa.icon_svg("truck", "solid"),
    "bobo": fa.icon_svg("wrench","solid"),
    "assurance": fa.icon_svg("file-contract","solid"),
    "vidange": fa.icon_svg("oil-can","solid"),
    "stopwatch": fa.icon_svg("stopwatch", "solid"),
    "depense": fa.icon_svg("money-bill-wave", "solid"),
    "patente": fa.icon_svg("clipboard", "solid"),
    "carte_de_stationnement": fa.icon_svg("id-card", "solid"),
    "badge": fa.icon_svg("user-shield"),
    "carte_grise": fa.icon_svg("id-card"),
    "chantier_positionnement": fa.icon_svg("location-dot", "solid"),
    
}


#technique page 2

# Page 1
page1 = ui.page_sidebar(
    ui.sidebar(
        ui.input_dark_mode(),
        ui.input_select("imat","Choisissez un camion",imat_dict),
        ui.markdown("Informations chauffeur"),
        ui.output_text("chauffeur"),
        ui.output_text("contact"),

    ),
    ui.layout_column_wrap(
        ui.value_box("Type",ui.output_text("type"),showcase=ICONS["camion"]),
        ui.value_box("Position",ui.output_text("chantier"),showcase=ICONS["chantier_positionnement"]),
        
    ),
    ui.layout_columns(
        ui.value_box("Police d'assurance",ui.output_text("police"),showcase=ICONS["assurance"]),
        ui.value_box("Badge associé",ui.output_text("badge"),showcase=ICONS["badge"]),
        ui.value_box("Prochaine vidange",ui.output_text("vidange"),showcase=ICONS["vidange"]),

    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Récap des dépenses"),
            output_widget("plot_depenses_t"),
            #ui.output_plot("plot_depenses"),
            #ui.output_data_frame("ligne_depenses"),
            full_screen=True,
        ),

    ),
    ui.layout_columns(
        ui.value_box("Nombre de bobos",ui.output_text("total_nombre_bobo_relatif"),showcase=ICONS["bobo"]),
        ui.value_box("Dépenses totales relatives à l'entretien",ui.output_text("total_depenses_relative"),showcase=ICONS["depense"]),   
    ),

    ui.layout_columns(
        #ui.card(
            #ui.card_header("Nombre d'intervention par camion"),
            #ui.output_table("base_somme_depense"),
           # full_screen=True,
       # ),
        ui.card(
            ui.card_header("Histogramme des dépenses par Camions"),
            output_widget("plot_depenses_pour_tous"),
            #ui.output_plot("plot_depenses_pour_tous"),
            style= "height: 500px;" , 
            full_screen=True,
        ),
    ),
    ui.layout_columns(
        ui.value_box("N° de  carte grise",ui.output_text("carte_grise"), showcase=ICONS["carte_grise"]),
        ui.value_box("Expiration d'assurance",ui.output_text("expiration_assurance"),showcase=ICONS["stopwatch"]),
        ui.value_box("Expiration carte de tranport",ui.output_text("exppiration_transport"),showcase=ICONS["stopwatch"]),
        
    ),
    
)

# les différentes pages et titres
app_ui = ui.page_navbar(
    ui.nav_panel("Dashbord dépenses : Camions", page1),
    #ui.nav_panel("Dashbord dépenses : Engins", page2),
    #ui.nav_panel("", page3),
    title="PWC : Gestion",
     fillable=True,
)

# Server
def server(input, output, session):

#Ensselble des fonction pour page 1 : Dashbord depenses camions

   #fonction reactive

    @render.data_frame
    def base_de_donnees():
        return df
    
    @render.data_frame
    def base_de_donnees_depenses():
        return df_depenses
    
    @reactive.Calc
    def filtre_tableau_depense():
        filtre_tableau_depense =df_depenses.loc[df_depenses["Immatriculation"]==input.imat()]
        return filtre_tableau_depense
    
    @render.data_frame
    def ligne_depenses()->pd.DataFrame:
        return filtre_tableau_depense() 
        
    
    @render.image
    def logo():
        logo = {"src": r"C:\Users\jngue\Desktop\stage_PWC\dasbord_pytthon\05-basic-navigation/logopwc.png","height":"200px", "width": "200px"}
        return logo
    

    
    @reactive.Calc
    def filtre_depense():
        filtre_depense = df.loc[df["Immatriculation"]==input.imat(),["DEPENSES RELATIVES"]]
        return filtre_depense.values[0]
    @render.text
    def depense_relative():
        return filtre_depense()
    
    

    
    @reactive.Calc
    def filtre_type():
        filtre_type = df.loc[df["Immatriculation"]==input.imat(),["Type de camion"]]
        return filtre_type.values[0][0] 
    @render.text
    def type():
        return filtre_type()
    

    
    @reactive.Calc
    def filtre_badge():
        filtre_badge = df.loc[df["Immatriculation"]==input.imat(),["BADGE ASSOCIE"]]
        return filtre_badge.values[0][0] 
    @render.text
    def badge():
        return filtre_badge()
    


    @reactive.Calc
    def filtre_police():
        filtre_police = df.loc[df["Immatriculation"]==input.imat(),["POLICE ASSURANCE"]]
        return filtre_police.values[0][0] 
    @render.text
    def police():
        return filtre_police()
    

    @reactive.Calc
    def filtre_expiration_assurance():
        filtre_expiration_assurance = df.loc[df["Immatriculation"]==input.imat(),["EXPIRATION ASSURANCE"]]
        return filtre_expiration_assurance.values[0][0]
    @render.text
    def expiration_assurance():
        return filtre_expiration_assurance()
    

    @reactive.Calc
    def filtre_vidange():
        filtre_vidange = df.loc[df["Immatriculation"]==input.imat(),["VIDANGE"]]
        return f"{filtre_vidange.values[0][0]} Km"
    @render.text
    def vidange():
        return filtre_vidange()
    
    @reactive.Calc
    def filtre_chantier():
        filtre_chantier = df.loc[df["Immatriculation"]==input.imat(),["Chantier"]]
        return filtre_chantier.values[0][0] 
    @render.text
    def chantier():
        return filtre_chantier()
    


    @reactive.Calc
    def filtre_carte_grise():
        filtre_carte_grise = df.loc[df["Immatriculation"]==input.imat(),["CARTE GRISE"]]
        return filtre_carte_grise.values[0][0] 
    @render.text
    def carte_grise():
        return filtre_carte_grise()
    


    @reactive.Calc
    def filtre_expiration_transport():
        filtre_expiration_transport = df.loc[df["Immatriculation"]==input.imat(),["EXPIRATION CARTE DE TRANSPORT"]]
        return filtre_expiration_transport.values[0][0] 
    @render.text
    def exppiration_transport():
        return filtre_expiration_transport()
    

    @reactive.Calc
    def total_depenses():
         # Conserve la première colonne
        premiere_colonne = df_depenses.iloc[:, 0]  # Prend la première colonne à partir de la deuxième ligne
        # Calcule la somme des lignes à partir de la deuxième ligne et deuxième colonne
        somme_depenses = df_depenses.iloc[:, 1:].sum(axis=1)
        # Combine la première colonne avec les résultats de la somme dans un DataFrame
        resultat_final = pd.DataFrame({
        'Immatriculation': premiere_colonne,  # Colonne d'identifiants des camions
        'Total Dépenses': somme_depenses  # Somme des dépenses par ligne
    })
        total_depenses = resultat_final.loc[resultat_final["Immatriculation"]==input.imat(),["Total Dépenses"]]
        return f"{total_depenses.values[0][0]} Fcfa"
    

    @render.text
    def total_depenses_relative():
        return total_depenses()
    

    @reactive.Calc
    def filtre_chauffeur():
        filtre_chauffeur = df.loc[df["Immatriculation"]==input.imat(),["Chauffeur"]]
        return filtre_chauffeur.values[0][0] 
    @render.text
    def chauffeur():
        return filtre_chauffeur()
    

    @reactive.Calc
    def filtre_contact():
        filtre_contact = df.loc[df["Immatriculation"]==input.imat(),["Contact chauffeur"]]
        return filtre_contact.values[0][0] 
    @render.text
    def contact():
        return filtre_contact()
    
    
    #@reactive.Calc
    #def df_somme_depenses():
        # Conserve la première colonne
        #premiere_colonne = df_depenses.iloc[:, 0]  # Prend la première colonne à partir de la deuxième ligne
        # Calcule la somme des lignes à partir de la deuxième ligne et deuxième colonne
       # somme_depenses = df_depenses.iloc[:, 1:].sum(axis=1)
        # Combine la première colonne avec les résultats de la somme dans un DataFrame
        #resultat_final = pd.DataFrame({
        #'Camion': premiere_colonne,  # Colonne d'identifiants des camions
        #'Total Dépenses': somme_depenses  # Somme des dépenses par ligne
    #})
       # return resultat_final
    
    #@render.table
    #def base_somme_depense():
        #return df_somme_depenses()  
    

    @reactive.Calc
    def df_compte_depenses():
         l =[]
         n=0
         premiere_colonne = df_depenses.iloc[:,0]
         for i in range(0,df_depenses.shape[0]):
             for j in range(0,df_depenses.shape[1]):
                 if df_depenses.iloc[i,j]!=0:
                     n= n+1
             l.append(n)
             n=0 
         resultat_final = pd.DataFrame({
        'Immatriculation': premiere_colonne,  
        'Nombre de Dépenses': l  
    })
         total_bobo = resultat_final.loc[resultat_final["Immatriculation"]==input.imat(),["Nombre de Dépenses"]].copy()
         return total_bobo.values[0][0]
    
    @render.text
    def total_nombre_bobo_relatif():
        return df_compte_depenses()
    
    
    @render_plotly()
    def plot_depenses_pour_tous():
        # Conserve la première colonne
        premiere_colonne = df_depenses.iloc[:, 0]  # Prend la première colonne
        # Calcule la somme des lignes à partir de la deuxième ligne et deuxième colonne
        somme_depenses = df_depenses.iloc[:, 1:].sum(axis=1)
        # Combine la première colonne avec les résultats de la somme dans un DataFrame
        resultat_final = pd.DataFrame({
        'Immatriculation': premiere_colonne,  # Colonne d'identifiants des camions
        'Total Dépenses': somme_depenses  # Somme des dépenses par ligne
    })
        # Création du graphique avec Plotly
        fig = px.bar(
        resultat_final,
        x='Immatriculation',
        y='Total Dépenses',
        color='Total Dépenses',
        title='Dépenses totales par camions',
        labels={'Immatriculation': 'Camions', 'Total Dépenses': 'Montant'},
        template='plotly_white',  # Optionnel : pour un style plus propre
        #color_continuous_scale=px.colors.sequential.Blues,  # Dégradé de bleu
        #color_continuous_scale=['#000000', '#808080', '#FFFFFF'],  # Dégradé de gris, du noir au blanc
        #color_continuous_scale=px.colors.sequential.YlOrBr
        #color_continuous_scale=px.colors.sequential.Redor
        #color_continuous_scale=px.colors.diverging.Temps
        #color_continuous_scale=px.colors.sequential.Sunset
        #color_continuous_scale=px.colors.sequential.Oranges,
        color_continuous_scale=["#FFFF99", "#FFCC66", "#FF9933", "#FF6600"]
        
    )
        # Ajustement de la rotation des étiquettes sur l'axe des x
        fig.update_layout(xaxis_tickangle=-45)
        return fig
    

    @render_plotly()
    def plot_depenses_t():
        # Filtrer les données pour l'immatriculation spécifique
        df_bar_depenses = df_depenses.loc[df_depenses["Immatriculation"] == input.imat()]
        # Récupérer les noms des colonnes (sauf "Immatriculation")
        column_names = df_depenses.columns.drop("Immatriculation")
        # Créer un DataFrame pour le graphique
        df_plot = pd.DataFrame({
        'Variables': column_names,
        'Valeurs': df_bar_depenses.iloc[0][column_names]
    })
         # Création du graphique avec Plotly
        fig = px.bar(
        df_plot,
        x='Variables',
        y='Valeurs',
        color='Valeurs',
        title='Détails des dépenses',
        labels={'Variables': 'Catégories de dépenses', 'Valeurs': 'Montants'},
        template='plotly_white',  # Style propre
        #color_discrete_sequence=['#FFA500']  # Couleur orange pour toutes les barres
        #color_continuous_scale=px.colors.sequential.Oranges,  # Dégradé d'orange
        #color_continuous_scale=['#000000', '#808080', '#FFFFFF'],  # Dégradé de gris, du noir au blanc
        color_continuous_scale=px.colors.sequential.YlOrBr
        #color_continuous_scale=px.colors.sequential.Tropic
    )
         # Ajustement des titres des axes
        fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        xaxis_tickangle=-45  # Rotation des étiquettes sur l'axe des x
    )
        return fig
    
    
# Create and run the app
app = App(app_ui, server)
