#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grupo: NAN
Integrantes: Rozas Chavez, Antuanette Carolina
             Madril, Joaquin Leandro
             Fernández Fazio, Adrián Patricio
             
Este archivo incluye todo el código para recolectar los datos desde los censos,
limpiarlos, y responder a los requerimientos de la consigna.

"""

import pandas as pd

#%% Carga los archivos

censo_2010 = 'censo2010.xlsX'
censo_2010_df = pd.read_excel(censo_2010)

censo_2022 = 'censo2022.xlsX'
censo_2022_df = pd.read_excel(censo_2022)


#%% Separa la columna edad de la de provincia
censo_2010_df['edad'] = censo_2010_df['Unnamed: 2']
censo_2022_df['edad'] = censo_2022_df['Unnamed: 2']

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
#%% Elimina todas las tuplas con totales
def elimina_totales(censo):
    i = 0
    
    while i < len(censo):
        if 'Total' in str(censo.loc[i,'Unnamed: 1']):# Castea a str por Nan
            i+=1
            while 'AREA' not in str(censo.loc[i,'Unnamed: 1']):# Castea a str por Nan
                censo = censo.drop([i], axis = 0)
                i+=1
        i+=1
    return censo

censo_2010_df = elimina_totales(censo_2010_df)
censo_2022_df = elimina_totales(censo_2022_df)

censo_2010_df = censo_2010_df[censo_2010_df['Unnamed: 1'] != 'Total']
censo_2022_df = censo_2022_df[censo_2022_df['Unnamed: 1'] != 'Total']

censo_2010_df = censo_2010_df[censo_2010_df['Unnamed: 2'] != ' Total']
censo_2022_df = censo_2022_df[censo_2022_df['Unnamed: 2'] != ' Total']

censo_2010_df = censo_2010_df.reset_index(drop=True)
censo_2022_df = censo_2022_df.reset_index(drop=True)

#%% Asigna los nombres de las provincias a cada tupla
def asigna_provincias(censo):
    i = 0
    provincia = ''
    cantidad_de_elementos = len(censo)
    while i < cantidad_de_elementos:
        
        if 'AREA' in str(censo.loc[i,'Unnamed: 1']):# Castea a str por Nan
            provincia = censo.loc[i, 'Unnamed: 2']
            i+=1
        censo.loc[i, 'Unnamed: 2'] = provincia
        i+=1

asigna_provincias(censo_2010_df)
asigna_provincias(censo_2022_df)


#%% Asigna los que no tienen cobertura 
def asigna_cobertura(censo):
    i = 0
    cantidad_de_elementos = len(censo)
    while i < cantidad_de_elementos:
        if 'No tiene obra social' in str(censo.loc[i,'Unnamed: 1']):
            i+=1
            while 'AREA' not in str(censo.loc[i,'Unnamed: 1']):
                censo.loc[i,'Unnamed: 1'] = False
                i+=1
                if i == cantidad_de_elementos:
                    break
        i+=1

asigna_cobertura(censo_2010_df)
asigna_cobertura(censo_2022_df)
#%% Renombramos las columnas
censo_2010_df.rename(columns={"Unnamed: 1": "cobertura", 
                             "Unnamed: 2": "provincia",
                             "Unnamed: 3": "varon",
                             "Unnamed: 4": "mujer"                          
                      }, inplace=True)
#mujer y varon estan al reves en los dos censos
censo_2022_df.rename(columns={"Unnamed: 1": "cobertura", 
                             "Unnamed: 2": "provincia",
                             "Unnamed: 3": "mujer",
                             "Unnamed: 4": "varon"
                      }, inplace=True)
#%%
censo_2022_df = censo_2022_df[['cobertura', 'provincia', 'varon', 'mujer', 'edad']]

#%% Borramos los encabezados de referencia
def elimina_encabezados(censo):
    i = 0
    while i < len(censo):
        if 'AREA' in str(censo.loc[i,'cobertura']):# Castea a str por Nan
            for j in range(4):
                censo = censo.drop([i + j], axis = 0)
            i += 4
        i+=1
    return censo

censo_2010_df = elimina_encabezados(censo_2010_df)
censo_2022_df = elimina_encabezados(censo_2022_df)

censo_2010_df = censo_2010_df.dropna(subset='edad')
censo_2022_df = censo_2022_df.dropna(subset='edad')

censo_2010_df = censo_2010_df.reset_index(drop=True)
censo_2022_df = censo_2022_df.reset_index(drop=True)
#%% Todos los nan de cobertura a TRUE
censo_2010_df['cobertura'] = censo_2010_df['cobertura'].fillna(True)
censo_2022_df['cobertura'] = censo_2022_df['cobertura'].fillna(True)
#%% Cambiamos el nombre en el Censo 2010 a CABA
censo_2010_df['provincia'] = censo_2010_df['provincia'].replace('Ciudad Autónoma de Buenos Aires', 'Caba')
#%%
censo_2022_df.replace(to_replace='-', value=0, inplace=True)
censo_2010_df.replace(to_replace='-', value=0, inplace=True)

#%%
def agrupar_edades(censo):
    censo['rango'] = pd.cut(
        censo['edad'],
        bins=[0, 15, 35, 55, 75, 150],
        right=False,
        labels = ['0 a 14', '15 a 34', '35 a 54', '55 a 74', '75 y mas'],
        include_lowest=True
        )
    
agrupar_edades(censo_2010_df)
agrupar_edades(censo_2022_df)
#%%
def separar_sexo(censo):
    censo_mujeres = censo.loc[:,['provincia', 'rango', 'mujer', 'cobertura']]
    censo_varones = censo.loc[:,['provincia', 'rango', 'varon', 'cobertura']]
    censo_mujeres['sexo'] = 'mujer'
    censo_varones['sexo'] = 'varon'
    censo_mujeres.rename(columns={'mujer':'cantidad'}, inplace=True)
    censo_varones.rename(columns={'varon':'cantidad'}, inplace=True)
    return pd.concat([censo_mujeres, censo_varones], axis=0, ignore_index=True)

censo_2010_df = separar_sexo(censo_2010_df)
censo_2022_df = separar_sexo(censo_2022_df)
#%%
clave_censo = ['provincia', 'rango', 'sexo', 'cobertura']
censo_2010_df = censo_2010_df.groupby(clave_censo).sum().reset_index()
censo_2022_df = censo_2022_df.groupby(clave_censo).sum().reset_index()

#%% Guardamos ambos dataframes como csv
censo_2010_df.to_csv('censo_2010_limpio.csv')
censo_2022_df.to_csv('censo_2022_limpio.csv')
