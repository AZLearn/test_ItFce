# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 08:44:12 2020

@author: vanPC2015
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import time

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt




def lect_plot():
    ###### lecture 2 fichiers .csv
    url_root = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'
    fname_G_orig = "time_series_covid19_confirmed_global.csv"
    fname_D_orig = "time_series_covid19_deaths_global.csv" 
    df_G = pd.read_csv(url_root + '/' + fname_G_orig)
    df_D = pd.read_csv(url_root + '/' + fname_D_orig)
        
    temps = len(df_G.columns) - 4
    x_temps = np.arange(temps)
    #print("nb de jours depuis aujourd'hui = ", temps )
    
    #France métrop
    df_France = df_G[df_G['Country/Region'] == 'France']
    df_Fmetrop = df_France[df_France['Province/State'].isna() == True]
    df_D_France = df_D[df_D['Country/Region'] == 'France']
    df_D_Fmetrop= df_D_France[df_D_France['Province/State'].isna() == True]

    nbcas_Fr = df_Fmetrop.iloc[:, 4: ]
    y_nbcas_Fr = np.array(nbcas_Fr)
    nbcas_D_Fr = df_D_Fmetrop.iloc[:, 4: ]
    y_nbcas_D_Fr = np.array(nbcas_D_Fr)

    maxi_nbcas_Fr = int(y_nbcas_Fr[0][-1])
    maxi_D_Fr = int(y_nbcas_D_Fr[0][-1])
    #print("France hors DOM : nb cas= {} ; nb morts = {}".format(maxi_nbcas_Fr, maxi_D_Fr))

    #France+DOM
    nbcas_FrAvecDOM = df_G[df_G['Country/Region'] == 'France'].iloc[:, 4:].sum()
    y_nbcas_FrAvecDOM = np.array(nbcas_FrAvecDOM)
    maxi_nbcas_FrAvecDOM = int(y_nbcas_FrAvecDOM[-1])
    nbcas_D_FrAvecDOM = df_D[df_D['Country/Region'] == 'France'].iloc[:, 4:].sum()
    y_nbcas_D_FrAvecDOM = np.array(nbcas_D_FrAvecDOM)
    maxi_D_FrAvecDOM = int(y_nbcas_D_FrAvecDOM[-1])
    #print("France+DOM : nb cas={} ; nb morts={}".format(maxi_nbcas_FrAvecDOM, maxi_D_FrAvecDOM))


    #Italy
    df_Italy = df_G[df_G['Country/Region'] == 'Italy']
    df_D_Italy = df_D[df_D['Country/Region'] == 'Italy']
    nbcas_It = df_Italy.iloc[:, 4: ]
    y_nbcas_It = np.array(nbcas_It)
    maxi_nbcas_It = int(y_nbcas_It[0][-1])
    nbcas_D_It = df_D_Italy.iloc[:, 4: ]
    y_nbcas_D_It = np.array(nbcas_D_It)
    maxi_D_It = int(y_nbcas_D_It[0][-1])
    #print("Italie : nb cas={} ; nb morts={}".format(maxi_nbcas_It, maxi_D_It))

    
    #Spain
    df_Spain = df_G[df_G['Country/Region'] == 'Spain']
    df_D_Spain = df_D[df_D['Country/Region'] == 'Spain']
    nbcas_Sp = df_Spain.iloc[:, 4: ]
    y_nbcas_Sp = np.array(nbcas_Sp)
    maxi_nbcas_Sp = int(y_nbcas_Sp[0][-1])
    nbcas_D_Sp = df_D_Spain.iloc[:, 4: ]
    y_nbcas_D_Sp = np.array(nbcas_D_Sp)
    maxi_D_Sp = int(y_nbcas_D_Sp[0][-1])
    #print("Espagne : nb cas={} ; nb morts={}".format(maxi_nbcas_It, maxi_D_It))

    
    #### plots
    #%matplotlib inline
    plt.scatter(x_temps,y_nbcas_It,color="red", label='Italie: ' + str(maxi_nbcas_It) + ' cas')
    plt.scatter(x_temps,y_nbcas_Sp,color="limegreen", label='Espagne: ' + str(maxi_nbcas_Sp) + ' cas')
    plt.scatter(x_temps,y_nbcas_FrAvecDOM,color="blue", label='France: ' + str(maxi_nbcas_FrAvecDOM) + ' cas')
    plt.title("Nombre de cas" + '\n' + datetime.today().strftime('%Y-%m-%d' ))
    plt.legend()
    #plt.show()
    st.pyplot()
    
    #%matplotlib inline
    plt.scatter(x_temps,y_nbcas_D_It,color="red", marker= 'x', label='Italie: ' + str(maxi_D_It) + ' morts')
    plt.scatter(x_temps,y_nbcas_D_Sp,color="limegreen", marker= 'x', label='Espagne: ' + str(maxi_D_Sp) + ' morts')
    plt.scatter(x_temps,y_nbcas_D_FrAvecDOM,color="blue", marker= 'x', label='France+DOM: ' 
                + str(maxi_D_Fr)
                + '+' + str(maxi_D_FrAvecDOM - maxi_D_Fr)
                + ' morts')

    plt.title('Nombre de morts' + '\n' + datetime.today().strftime('%Y-%m-%d' ))
    plt.legend()
    #plt.show()
    st.pyplot()


    #Décalage Italie de X jours
    #%matplotlib inline
    st.markdown('## Comparaison évolutions en France et Italie avec un décalage de 10 jours')
    st.markdown('### Nombre de cas')

    DECALAGE = 10
    y_decal_D = np.roll(y_nbcas_D_It, DECALAGE)
    y_decal = np.roll(y_nbcas_It, DECALAGE)
    
    for i in range(DECALAGE):
        y_decal_D[0, i] = y_nbcas_D_It[0, 0]
        y_decal[0, i] = y_nbcas_It[0, 0]

    plt.scatter(x_temps,y_decal,color="red", label='Italie décalé')
    plt.scatter(x_temps,y_nbcas_FrAvecDOM,color="blue", label='France')
    
    plt.title(datetime.today().strftime('%Y-%m-%d' ) + '\n' 
              + 'Nb cas/ Décalage de ' + str(DECALAGE) +' jours')  
    plt.legend()
    #plt.show()
    st.pyplot()
    
    st.markdown('### Nombre de morts')

    plt.scatter(x_temps,y_decal_D,color="red", marker='+', label='Italie décalé')
    plt.scatter(x_temps,y_nbcas_D_FrAvecDOM,color="blue", marker='x', label='France')

    plt.title(datetime.today().strftime('%Y-%m-%d' ) + '\n' 
              + 'Nb morts/ Décalage de ' + str(DECALAGE) +' jours')
    plt.legend()
    #plt.show()
    st.pyplot()

    

st.title('COVID19 : Italie-Espagne-France')
#st.title('France-Italie-Espagne')
st.header('Evolution depuis le 22/01/2020')
st.markdown('Chiffres cohérents avec ceux affichés sur :  https://www.eficiens.com/covid-19-statistics/')

lect_plot()
st.markdown('Données source : https://github.com/CSSEGISandData/COVID-19')
