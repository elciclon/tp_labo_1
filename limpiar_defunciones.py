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

defunciones = defunciones.drop(['jurisdiccion_de_residencia_id', 
                 'sexo_id', 
                 'muerte_materna_id',
                 'muerte_materna_clasificacion'], axis=1)
#%% Simplificamos las categorías
defunciones['cie10_clasificacion'] = defunciones['cie10_causa_id'].astype(str).str.lower().map(categorias_dict)    

# Elimina columna innecesario 'cie10_causa_id'
defunciones = defunciones.drop('cie10_causa_id', axis=1)

#%% Guarda los archivos

defunciones.to_csv('defunciones_limpio.csv')
