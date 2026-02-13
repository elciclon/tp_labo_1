#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grupo: NAN
Integrantes: Rozas Chavez, Antuanette Carolina
             Madril, Joaquin Leandro
             Fernández Fazio, Adrián Patricio
             
 Este archivo incluye todo el código para recolectar los datos desde las fuentes
 proporcionadas, limpiarlos, y responder a los requerimientos de la consigna.

"""

import pandas as pd

#%% Carga los archivos

censo_2010 = 'censo2010.xlsX'
censo_2010_df = pd.read_excel(censo_2010)

censo_2022 = 'censo2022.xlsX'
censo_2022_df = pd.read_excel(censo_2022)

instituciones = 'instituciones_de_salud.xlsx'
instituciones_df = pd.read_excel(instituciones)

defunciones = 'defunciones.csv'
defunciones_df = pd.read_csv(defunciones)

#%% Limpia encabezados y resúmenes

# Limpiar encabezados
for i in range(14):
    censo_2010_df = censo_2010_df.drop([i], axis = 0)
    censo_2022_df = censo_2022_df.drop([i], axis = 0)
    
# Limpiar resúmenes
for i in range(14930, 15608):
    censo_2010_df = censo_2010_df.drop([i], axis = 0)
    
for i in range(10541, 11001):
    censo_2022_df = censo_2022_df.drop([i], axis = 0)
    
#%% Elimina columnas innecesarias

censo_2010_df = censo_2010_df.drop(['CEPAL/CELADE Redatam+SP 01/29/2026', 
                                    'Unnamed: 5'], axis = 1)
censo_2022_df = censo_2022_df.drop(['CEPAL/CELADE Redatam+SP 01/29/2026', 
                                    'Unnamed: 5'], axis = 1)

censo_2010_df = censo_2010_df.reset_index(drop=True)
censo_2022_df = censo_2022_df.reset_index(drop=True)

#%% Asigna los nombres de las provincias a cada tupla

i = 14
provincia = ''
while i <= len(censo_2010_df):
    if 'AREA' in censo_2010_df[i]['Unnamed: 1']:
        provincia = censo_2010_df['Unnamed: 2']
    censo_2010_df['Unnamed: 2'] = provincia
