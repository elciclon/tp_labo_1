#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grupo: NAN
Integrantes: Rozas Chavez, Antuanette Carolina
             Madril, Joaquin Leandro
             Fernández Fazio, Adrián Patricio
             
Este archivo incluye todo el código para recolectar los datos desde las defunciones,
limpiarlos, y responder a los requerimientos de la consigna.

"""
#%% cargamos archivos
import pandas as pd

defunciones = pd.read_csv('defunciones.csv')
categorias = pd.read_csv('categoriasDefunciones.csv')
#%% Métricas para GQM
jurisdiccion_residencia_nombre_NaN = int(defunciones['jurisdicion_residencia_nombre'].isna().sum())
cie10_clasificacion_NaN = int(defunciones['cie10_clasificacion'].isna().sum())
cantidad_defunciones = len(defunciones)

#%% Crea un diccionario con las categorías agrupadas por letra
categorias_dict ={}
for e in categorias.itertuples():
    if e.codigo_def not in categorias_dict.keys():
        categorias_dict[str(e.codigo_def).lower()] = e.categorias
# Agregamos categorias faltantes
categoria_por_inicial ={}
for categoria in categorias_dict:
    letra = categoria[0]
    if letra not in categoria_por_inicial:
        if letra == 'd':
            continue
        categoria_por_inicial[letra] = categorias_dict[categoria]

for clave, valor in categoria_por_inicial.items():
    for i in range(10):
        for j in range(10):
            codigo = clave + str(i) + str(j)
            if  codigo not in categorias_dict.keys():
                categorias_dict[codigo] = valor


#%% eliminamos columnas innecesarias

defunciones = defunciones.drop([ 
                 'sexo_id', 
                 'muerte_materna_id',
                 'muerte_materna_clasificacion'], axis=1)
#%% Simplificamos las categorías
defunciones['cie10_clasificacion'] = defunciones['cie10_causa_id'].astype(str).str.lower().map(categorias_dict)    

# Elimina columna innecesario 'cie10_causa_id'
defunciones = defunciones.drop('cie10_causa_id', axis=1)

#%%
for col in ['anio', 'jurisdicion_residencia_nombre', 'grupo_edad', 'Sexo', 'cantidad']:
    print(defunciones[col].value_counts(dropna=False))
#%%
print(defunciones[['jurisdiccion_de_residencia_id', 'jurisdicion_residencia_nombre']].value_counts(dropna=False))
#%%
defunciones.drop('jurisdicion_residencia_nombre', axis=1, inplace=True)

# 'jurisdicion_residencia_nombre' tiene 9358 valores 'Sin Información'
# y 4996 valores NaN

#'grupo_edad' tiene 8811 valores 'Sin especificar'

#Sexo tiene 5220 valores 'desconocido' y 221 'indeterminado'

#9358 + 4996 + 8811 + 5220 + 221 = 28606, si ninguno tuviera null en mas de un campo
#como hay datos con Null en varios campos este valor es menor todavia
# 28606/825814 (Null / total de registros) < 3,5%
#%%
defunciones = defunciones[
    ( ~defunciones['jurisdiccion_de_residencia_id'].isin([98, 99])) &
    (defunciones['Sexo'].isin(['masculino', 'femenino'])) &
    (defunciones['grupo_edad'] != '06.Sin especificar')
    ]


#%%
todas_menos_cantidad = [
    'anio',
    'jurisdiccion_de_residencia_id', 
    'cie10_clasificacion',
    'Sexo', 
    'grupo_edad'
    ]

defunciones = defunciones.groupby(todas_menos_cantidad).sum().reset_index()
#%% reordeno columnas
defunciones = defunciones[[
    'jurisdiccion_de_residencia_id',
    'cie10_clasificacion',
    'grupo_edad',
    'Sexo',
    'anio',
    'cantidad'
    ]]

defunciones.columns = ['id_provincia', 'causa', 'rango', 'sexo', 'año', 'cantidad']
#%% Hay provincias con dos Ids
defunciones.loc[defunciones['id_provincia'] == 86, 'id_provincia'] = 22
defunciones.loc[defunciones['id_provincia'] == 62, 'id_provincia'] = 26
defunciones.loc[defunciones['id_provincia'] == 66, 'id_provincia'] = 14
defunciones.loc[defunciones['id_provincia'] == 50, 'id_provincia'] = 75

#%% Guarda los archivos

defunciones.to_csv('defunciones_limpio.csv', index=False)
