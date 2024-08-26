# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 22:37:33 2024

@author: r.auappavou
"""

import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET

# Charger et analyser le fichier XML
file_path = 'D:\Documents de r.auappavou\Python Scripts\Quickcheck\qcw\Measdata.qcw'
tree = ET.parse(file_path)
root = tree.getroot()

# Fonction pour extraire les valeurs mesurées et analysées avec les noms des worklists
def extract_all_measured_analyzed_values_with_worklist(root):
    trend_data_list = []
    
    for trend_data in root.findall(".//TrendData"):
        trend_info = {}
        trend_info['Date'] = trend_data.attrib.get('date')
        
        # Extraction des valeurs générales
        worklist = trend_data.find('.//Worklist')
        if worklist is not None:
            treatment_unit = worklist.find(".//TreatmentUnit")
            trend_info['Treatment Unit'] = treatment_unit.text if treatment_unit is not None else None
            
            energy = worklist.find(".//Energy")
            trend_info['Energy'] = energy.text if energy is not None else None
            
            wedge = worklist.find(".//Wedge")
            trend_info['Wedge'] = wedge.text if wedge is not None else None
            
            worklist_name = worklist.find('.//Name')
            trend_info['Worklist Name'] = worklist_name.text if worklist_name is not None else None

        # Extraction de toutes les valeurs mesurées
        meas_data = trend_data.find('.//MeasData/MeasValues')
        if meas_data is not None:
            for measure in meas_data:
                value = measure.find('Value')
                if value is not None:
                    trend_info[f'Measured {measure.tag}'] = value.text
        
        # Extraction de toutes les valeurs analysées
        analyze_data = trend_data.find('.//MeasData/AnalyzeValues')
        if analyze_data is not None:
            for analyze in analyze_data:
                value = analyze.find('Value')
                if value is not None:
                    trend_info[f'Analyzed {analyze.tag}'] = value.text

        trend_data_list.append(trend_info)
    
    return trend_data_list

# Extraction des données
final_data_with_worklist = extract_all_measured_analyzed_values_with_worklist(root)

# Convertir "Energy" et "Wedge" en entiers ou décimaux simples
def adjust_energy_wedge_format(data_list):
    for item in data_list:
        if 'Energy' in item:
            item['Energy'] = int(float(item['Energy']))
        if 'Wedge' in item:
            item['Wedge'] = int(float(item['Wedge']))
    return data_list

final_adjusted_list = adjust_energy_wedge_format(final_data_with_worklist)

# Conversion des autres colonnes en format flottant avec 4 décimales
def enforce_float_conversion(data_list):
    for item in data_list:
        for key, value in item.items():
            try:
                if isinstance(value, str) and 'E' in value:
                    item[key] = f'{float(value):.4f}'
            except ValueError:
                continue
    return data_list

final_float_corrected_list = enforce_float_conversion(final_adjusted_list)

# Trier les données par Worklist Name, avec "P4 HEBDO" séparé des autres "P4"
def sort_by_worklist(data_list):
    return sorted(data_list, key=lambda x: (x['Worklist Name'] if 'P4 HEBDO' not in x['Worklist Name'] else f'AA_{x["Worklist Name"]}'))

# Appliquer le tri
sorted_results_dict = sort_by_worklist(final_float_corrected_list)

# sorted_results_dict contient maintenant les résultats triés
