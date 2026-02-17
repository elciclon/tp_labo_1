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
habitan_por_prov = (grupoPoblacional
                     .loc[ :, ['id_provincia','año', 'cantidad']]
                     .groupby(['id_provincia', 'año'])
                     .sum()
                     .reset_index()
                     )

#%% grafico de cantidad de habitantes por provincia

ax = sns.barplot(
       data= habitan_por_prov,
       y = 'id_provincia',
       x = 'cantidad',
       orient = 'y',
       hue = 'año'
       )

ax.set_title('habitantes por provincia')
ax.set_xscale('log')


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

#%% grafico de tasa de mortalidad por provincia en 2022

sns.barplot(
    x = provincia,
    y = tasa_de_mortalidad,
    hue=''
    
    )


#%%cantidad de defunciones por grupo etario y sexo en 2022

sns.histplot( x = grupo_etario,
             y = cant_def_normalizadas,
             data = defunciones
             hue=sexo,
             order=['0 a 14', '15 a 34', '35 a 54', '55 a 74', '75 y mas']
             
    )

#%%

salud_por_depto = (establecimiento
                   .loc[:, ['id_provincia', 'id_departamento','id_establecimiento']]
                   .groupby(['id_provincia', 'id_departamento'])
                   .count()
                   .reset_index()
                   .rename(columns={'id_establecimiento':'cantidad'})
                   )

ax = sns.boxplot(x = 'id_provincia',
            y = 'cantidad',
            data = salud_por_depto,
            log_scale=True
    )
#%%
#??????????
ax.set_title('instituciones de salud por departamento')
ax.set_xlabel('provincia')
ax.set_ylabel('cantidad de instituciones por departamento')

provincias = []
ax.set_xticks(range(len(provincias)), labels=provincias)



