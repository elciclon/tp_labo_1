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
def normalizar_defunciones(grupo:list[str])->pd.DataFrame:
    grupo_poblacion = [col for col in grupo if col != 'causa']
    hab_grupo = (grupoPoblacional [grupoPoblacional['año'] == 2022]
                     .loc[:, grupo_poblacion+['cantidad']]
                     .groupby(grupo_poblacion)
                     .sum()
                     .reset_index()
                     .rename(columns={'cantidad':'habitantes'})
                     )
    if 'id_provincia' in grupo:
        hab_grupo = hab_grupo.merge(provincia, on='id_provincia', how='left')
    def_grupo = (defuncion [defuncion['año'] == 2022]
                     .loc[:, grupo +['cantidad']]
                     .groupby(grupo)
                     .sum()
                     .reset_index()
                     .rename(columns={'cantidad':'defunciones'})
                     .merge(hab_grupo, on=grupo_poblacion, how='left')
                     )

    def_grupo['defunciones_normalizadas'] = (def_grupo['defunciones']
                                                 /def_grupo['habitantes'])*1000
    return def_grupo.copy()

#%%
habitan_por_prov = (grupoPoblacional
                     .loc[ :, ['id_provincia','año', 'cantidad']]
                     .groupby(['id_provincia', 'año'])
                     .sum()
                     .reset_index()
                     .merge( provincia, on='id_provincia', how='left' )
                     )

#%% grafico de cantidad de habitantes por provincia
habitan_por_prov['año'] = habitan_por_prov['año'].astype(str)

provincias_ordenadas =( habitan_por_prov[ habitan_por_prov['año'] == '2022'] 
                       .sort_values(by='cantidad', ascending=False)
                       )

plt.figure(figsize=(12,8))
ax = sns.barplot(
       data= habitan_por_prov,
       y = 'nombre',
       x = 'cantidad',
       orient = 'y',
       hue = 'año',
       hue_order=['2022','2010'],
       order = provincias_ordenadas['nombre']
       )


# Nombres de los ejes
ax.set_xlabel('Cantidad de habitantes (escala logarítmica)')
ax.set_ylabel('Provincia')

ax.set_title('HABITANTES POR PROVINCIA')
ax.set_xscale('log')
ax.set_xticks([100000, 1000000, 10000000])
ax.grid(axis='x')


plt.show()

#%% grafico de defunciones por categoria en el tiempo

fig, ax = plt.subplots(figsize=(10,10))
ax.set_xticks(range(2005,2022, 2))
ax.set_xlabel('año')
ax.set_ylabel('Cantidad de defunciones')
ax.set_title('Defunciones por categoría a lo largo del tiempo')
plt.grid(axis='x')

def_por_causa = (defuncion
                 .loc[:,['causa', 'año', 'cantidad']]
                 .groupby(['causa','año'])
                 .sum()
                 .reset_index())

mayores_causas = (defuncion[defuncion['año'] == 2022]
                 .loc[:,['causa', 'cantidad']]
                 .groupby(['causa'])
                 .sum()
                 .sort_values(by='cantidad', ascending=False)
                 .reset_index()['causa']
                 .tolist()
                 )

cantidad_elementos = len(mayores_causas)
i = 0
while i < cantidad_elementos:
    
    ax.plot('año', 'cantidad', 
            data = def_por_causa[(def_por_causa['causa']==mayores_causas[i])],
            #linewidth=0.5,
            label=mayores_causas[i]
        )
    i+=1
    if i%6 ==0:
        plt.legend(
            bbox_to_anchor = (0.5, -0.05),
            loc='upper center'
            
            )
        plt.show()
        if i!=18:
            fig, ax = plt.subplots(figsize=(10,10))
            ax.set_xticks(range(2005,2023, 2))
            ax.set_xlabel('año')
            ax.set_ylabel('Cantidad de defunciones')
            ax.set_title('Defunciones por categoría a lo largo del tiempo')
            plt.grid(axis='x')


#%% cantidad de defunciones por provincia en 2022
plt.figure(figsize=(12,8))



def_por_prov = normalizar_defunciones(['id_provincia'])

provincias_ordenadas= def_por_prov.sort_values(by='defunciones_normalizadas')

ax = sns.barplot( y = 'nombre',
             x = 'defunciones_normalizadas',
             data = def_por_prov,
             order = provincias_ordenadas['nombre']
    )
ax.grid(axis='x')
ax.set_title('TASA DE MORTALIDAD POR PROVINCIA 2022')
ax.set_ylabel('')
ax.set_xlabel('defunciones cada mil habitantes')

plt.show()


#%% defunciones por prov diferenciado por causa
def_por_prov = normalizar_defunciones(['id_provincia', 'causa'])

# tasa de mortalidad por causa, todas las causas
for causa in defuncion['causa'].drop_duplicates():
    plt.figure(figsize=(12,8))
    plt.xlim(0, 4)
    filtro_causa = def_por_prov ['causa'] == causa
    ax = sns.barplot( y = 'nombre',
                 x = 'defunciones_normalizadas',
                 data = def_por_prov[filtro_causa],
                 order = provincias_ordenadas['nombre']
                 
        )
    ax.grid(axis='x')
    ax.set_title(causa)
    ax.set_ylabel('')
    ax.set_xlabel('defunciones cada mil habitantes')

    plt.show()

#%% tasa de mortalidad principales causas
plt.figure(figsize=(12,8))


filtro_causa = def_por_prov ['causa'].isin(
    [#'Tumores ', 
     'Enfermedades del aparato circulatorio',
     'Enfermedades del aparato respiratorio'
     ])
ax = sns.barplot( y = 'nombre',
             x = 'defunciones_normalizadas',
             data = def_por_prov[filtro_causa],
             hue='causa',
             order = provincias_ordenadas['nombre']
             
    )
ax.grid(axis='x')
plt.xlim(0, 4)
ax.set_title('TASA DE MORTALIDAD POR PROVINCIA 2022, PRINCIPALES CAUSAS')
ax.set_ylabel('')
ax.set_xlabel('defunciones cada mil habitantes')

plt.show()


#%% tasa de mortalidad POR GRUPO ETARIO, PARA CADA PROVINCIA
def_provincia_grupo = normalizar_defunciones(['id_provincia','rango'])


for rango in defuncion['rango'].drop_duplicates():
    plt.figure(figsize=(12,8))
    #plt.xlim(0, 10)
    filtro_edad = def_provincia_grupo ['rango'] == rango
    ax = sns.barplot( y = 'nombre',
                 x = 'defunciones_normalizadas',
                 data = def_provincia_grupo[filtro_edad],
                 order = provincias_ordenadas['nombre']
                 
        )
    ax.grid(axis='x')
    ax.set_title(rango)
    ax.set_ylabel('')
    ax.set_xlabel('defunciones cada mil habitantes')

    plt.show()


#%%cantidad de defunciones por grupo etario y sexo en 2022
def_por_grupo = normalizar_defunciones(['rango', 'sexo'])

ax = sns.barplot( x = 'rango',
             y = 'defunciones_normalizadas',
             data = def_por_grupo,
             hue='sexo',
             order=['0 a 14', '15 a 34', '35 a 54', '55 a 74', '75 y mas']
             
    )
ax.set_title('DEFUNCIONES EN ARGENTINA 2022')
ax.set_ylabel('defunciones cada mil habitantes')
ax.set_xlabel('rango de edad')

plt.show()
#%%

salud_por_depto = (establecimiento
                   .loc[:, ['id_provincia', 'id_departamento','id_establecimiento']]
                   .groupby(['id_provincia', 'id_departamento'])
                   .count()
                   .reset_index()
                   .rename(columns={'id_establecimiento':'cantidad'})
                   .merge( provincia, on='id_provincia', how='left' )
                   )
provincias_ordenadas =( salud_por_depto
                       .groupby('nombre')[['cantidad']]
                       .median().reset_index()
                       .sort_values(by='cantidad', ascending=False)
                       )
plt.figure(figsize=(12,8))

ax = sns.boxplot(y = 'nombre',
            x = 'cantidad',
            data = salud_por_depto,
            log_scale=True,
            order = provincias_ordenadas['nombre']
    )
ax.set_title('ESTABLECIMIENTOS DE SALUD POR DEPARTAMENTO')
ax.set_ylabel('')
ax.set_xlabel('cantidad de instituciones por departamento')

plt.show()

#%% terapia intensiva por departamento

terapia_por_depto = (establecimiento [establecimiento['tiene_terapia']]
                   .loc[:, ['id_provincia', 'id_departamento','id_establecimiento']]
                   .groupby(['id_provincia', 'id_departamento'])
                   .count()
                   .reset_index()
                   .rename(columns={'id_establecimiento':'cantidad'})
                   .merge( provincia, on='id_provincia', how='left' )
                   )
provincias_ordenadas_terapia =( terapia_por_depto
                       .groupby('nombre')[['cantidad']]
                       .median().reset_index()
                       .sort_values(by='cantidad', ascending=False)
                       )
plt.figure(figsize=(12,8))

ax = sns.boxplot(y = 'nombre',
            x = 'cantidad',
            data = terapia_por_depto,
            log_scale=True,
            order = provincias_ordenadas_terapia['nombre']
    )
ax.set_title('ESTABLECIMIENTOS DE SALUD CON TERAPIA INTENSIVA POR DEPARTAMENTO')
ax.set_ylabel('')
ax.set_xlabel('cantidad de instituciones por departamento')

plt.show()

#%%

plt.figure(figsize=(12,8))

     
terapia_por_prov = (establecimiento
                 .loc[:, ['id_provincia', 'tiene_terapia']]
                 .groupby('id_provincia')
                 .count()
                 .reset_index()
                 .rename(columns={'tiene_terapia':'cant_terapia'})
                 .merge(habitan_por_prov[habitan_por_prov['año']=='2022'], 
                        on='id_provincia', 
                        how='left')
                 )

terapia_por_prov['cant_normalizada'] = (terapia_por_prov['cant_terapia']
                                             /terapia_por_prov['cantidad'])*1000

ax = sns.barplot( y = 'nombre',
             x = 'cant_normalizada',
             data = terapia_por_prov,
             order = provincias_ordenadas['nombre']
             
    )
ax.grid(axis='x')
ax.set_title('ESTABLECIMIENTOS CON TERAPIA INTENSIVA POR PROVINCIA')
ax.set_ylabel('')
ax.set_xlabel('Establecimientos cada mil habitantes')

plt.show()





