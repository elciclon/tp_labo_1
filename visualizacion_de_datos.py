#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grupo: NAN
Integrantes: Rozas Chavez, Antuanette Carolina
             Madril, Joaquin Leandro
             Fernández Fazio, Adrián Patricio
             
Este archivo incluye todo el código para crear las visualizaciones de datos
a partir de nuestras tablas

"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#%% importamos las tablas

provincia = pd.read_csv('provincia.csv')
defuncion = pd.read_csv('defuncion.csv')
grupoPoblacional = pd.read_csv('grupoPoblacional.csv')
departamento = pd.read_csv('departamento.csv')
establecimiento = pd.read_csv('establecimiento.csv')

#%%
habitan_prov_2010 = grupoPoblacional[grupoPoblacional['año'] == 2010].loc[
    :, ['id_provincia', 'cantidad']
    ].groupby('id_provincia').sum().reset_index()

habitan_prov_2022 = grupoPoblacional[grupoPoblacional['año'] == 2022].loc[
    :, ['id_provincia', 'cantidad']
    ].groupby('id_provincia').sum().reset_index()

#%% grafico de cantidad de habitantes por provincia

fig, ax = plt.subplots()

ax.bar(
       habitan_prov_2010['id_provincia'], 
       habitan_prov_2010['cantidad'],
       width = 3
       )

ax.set_title('habitantes por provincia')




plt.show()

#%% grafico de defunciones por categoria en el tiempo

fig, ax = plt.subplots()

def_por_causa = (defuncion
                 .loc[:,['causa', 'año', 'cantidad']]
                 .groupby(['causa','año'])
                 .sum().reset_index())

for causa in defuncion['causa'].drop_duplicates():    
    ax.plot('año', 'cantidad', 
            data = def_por_causa[(def_por_causa['causa']==causa)],
            #linewidth=0.5,
            label=causa
        
        )

#%% grafico de tasa de mortalidad pro provincia en 2022


#%%cantidad de defunciones por grupo etario y sexo en 2022

sns.histplot( x = grupo_etario,
             y = cant_def_normalizadas,
             data = defunciones
             hue=sexo,
             order=['0 a 14', '15 a 34', '35 a 54', '55 a 74', '75 y mas']
             
    )

#%%

sns.boxplot(x = provincia,
            y = cant_establecimientos,
            data = 
    )

ax.set_title('instituciones de salud por departamento')
ax.set_xlabel('provincia')
ax.set_ylabel('cantidad de instituciones por departamento')

provincias = []
ax.set_xticks(range(len(provincias)), labels=provincias)



