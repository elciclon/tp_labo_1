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

instituciones = 'instituciones_de_salud.xlsX'
instituciones_df = pd.read_excel(instituciones)

defunciones = 'defunciones.csv'
defunciones_df = pd.read_csv(defunciones)