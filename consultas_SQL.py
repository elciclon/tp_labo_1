#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grupo: NAN
Integrantes: Rozas Chavez, Antuanette Carolina
             Madril, Joaquin Leandro
             Fernández Fazio, Adrián Patricio
             
Este archivo incluye todo el código para crear las tablas a partir de los 
documentos provistos ya saneados, y responder a los requerimientos de la 
consigna.

"""
#%% Cargamos las tablas

import pandas as pd
import duckdb as dd

provincia = pd.read_csv('provincia.csv')
defuncion = pd.read_csv('defuncion.csv')
grupoPoblacional = pd.read_csv('grupoPoblacional.csv')
departamento = pd.read_csv('departamento.csv')
establecimiento = pd.read_csv('establecimiento.csv')

#%% EJERCICIO I

cantidadConCobertura2010 = """

                            SELECT p.nombre, gp.rango, SUM(gp.cantidad) AS cantidad
                            FROM provincia AS p JOIN grupoPoblacional AS gp
                            ON p.id_provincia = gp.id_provincia
                            WHERE gp.año = 2010 AND gp.tiene_cobertura = True
                            GROUP BY p.nombre, gp.rango

                            """
              
cantidadConCobertura2010 = dd.sql(cantidadConCobertura2010).df()

cantidadSinCobertura2010 = """

                            SELECT p.nombre, gp.rango, SUM(gp.cantidad) AS cantidad
                            FROM provincia AS p JOIN grupoPoblacional AS gp
                            ON p.id_provincia = gp.id_provincia
                            WHERE gp.año = 2010 AND gp.tiene_cobertura = False
                            GROUP BY p.nombre, gp.rango

                            """
              
cantidadSinCobertura2010 = dd.sql(cantidadSinCobertura2010).df()

cantidadConCobertura2022 = """

                            SELECT p.nombre, gp.rango, SUM(gp.cantidad) AS cantidad
                            FROM provincia AS p JOIN grupoPoblacional AS gp
                            ON p.id_provincia = gp.id_provincia
                            WHERE gp.año = 2022 AND gp.tiene_cobertura = True
                            GROUP BY p.nombre, gp.rango

                            """
              
cantidadConCobertura2022 = dd.sql(cantidadConCobertura2022).df()

cantidadSinCobertura2022 = """

                            SELECT p.nombre, gp.rango, SUM(gp.cantidad) AS cantidad
                            FROM provincia AS p JOIN grupoPoblacional AS gp
                            ON p.id_provincia = gp.id_provincia
                            WHERE gp.año = 2022 AND gp.tiene_cobertura = False
                            GROUP BY p.nombre, gp.rango

                            """
              
cantidadSinCobertura2022 = dd.sql(cantidadSinCobertura2022).df()

coberturaDeSalud = """

                    SELECT DISTINCT c1.nombre AS Provincia, c1.rango AS 'Grupo etario',
                    c1.cantidad AS 'Habitantes con Cobertura en 2010',
                    s1.cantidad AS 'Habitantes sin Cobertura en 2010',
                    c2.cantidad AS 'Habitantes con Cobertura en 2022',
                    s2.cantidad AS 'Habitantes sin Cobertura en 2022'
                    FROM cantidadConCobertura2010 AS c1 JOIN cantidadSinCobertura2010 AS s1
                    ON c1.nombre = s1.nombre AND c1.rango = s1.rango
                    JOIN cantidadConCobertura2022 AS c2 
                    ON c1.nombre = c2.nombre AND c1.rango = c2.rango
                    JOIN cantidadSinCobertura2022 AS s2
                    ON c1.nombre = s2.nombre AND c1.rango = s2.rango

                    """
                    
coberturaDeSalud = dd.sql(coberturaDeSalud).df()