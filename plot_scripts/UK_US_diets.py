# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:34:30 2024

@author: Thomas Ball
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# odPath = "E:\\OneDrive\\OneDrive - University of Cambridge"
odPath = "C:\\Users\\Thomas Ball\\OneDrive - University of Cambridge"
resultsPath = os.path.join(odPath, "Work\\FOODv0\\results")
figPath = "figs"
datPath = os.path.join(odPath, "Work", "FOODv0", "git", "food_v0", "model", "dat")

global_dat = pd.read_csv(os.path.join(resultsPath, "odf_commodities.csv"),index_col=0)
crop_db = pd.read_csv(os.path.join(datPath, "..", "crop_db.csv"))

GROUPING = "group_name_v6"
groups = crop_db[GROUPING].unique()
country_db_file = "nocsDataExport_20220822-151738.xlsx"
country_db = pd.read_excel(os.path.join(datPath,country_db_file))
pop_dat = pd.read_csv(os.path.join(datPath,"FAOSTAT_data_en_3-12-2024_population.csv"))
pop_dat = pop_dat[pop_dat.Year == 2021]
cal_dat = pd.read_csv(os.path.join(datPath,"FAOSTAT_data_en_3-12-2024_calories.csv"))


# %%
# diets = pd.read_csv(os.path.join(odPath, "Work", "FOODv0", "diets5_UK.csv"), index_col = 0, encoding = "latin-1")

diets = pd.read_csv(os.path.join(odPath, "Work", "FOODv0", "diets5_US.csv"), index_col = 0, encoding = "latin-1")
# 
diets = diets.loc[:, ~(diets.columns == "No-ruminant")]

coi = {
        
        # "DEU" : "", 
        "USA" : {"marker" : ">", "color" : "#EDF97A"},
        # "GBR" : {"marker": "v", "color" : "#FFB000"}, 
        # "JPN" : {"marker": ".", "color" : "#FE6100"},
        # "BRA" : {"marker": "x", "color" : "#DC267F"},
        # "IND" : {"marker": "o", "color" : "#785EF0"},
        # "TZA" : {}, 
        # "UGA" : {"marker" : "^", "color" : "#648FFF"},
        # "LKA" : {}
        # "UKR" : {}
        }

colourdict = {"group_name_v6" : {'Ruminant meat' : "#C90D75",
                                    'Pig meat'       : "#D64A98",
                                    'Poultry meat'   : "#D880B1",
                                    'Dairy'          : "#F7BDDD",
                                    'Eggs'           : "#FFEDF7",
                                    
                                    'Grains'             : "#D55E00",
                                    "Rice"               : "#D88E53",
                                    "Soybeans"           : "#DCBA9E",
                                    
                                    'Roots and tubers'   : "#0072B2",
                                    'Vegetables'         : "#4F98C1",
                                    'Legumes and pulses' : "#9EBFD2",
                                    
                                    'Bananas'           : "#FFED00",
                                    'Tropical fruit'    : "#FFF357",
                                    'Temperate fruit'   : "#FDF8B9",
                                    'Tropical nuts'     : "#27E2FF",
                                    'Temperate nuts'    : "#7DEEFF",
                                    
                                    'Sugar beet'    : "#FFC000",
                                    'Sugar cane'    : "#F7C93B",
                                    'Spices'        : "#009E73",
                                    'Coffee'        : "#33CCA2",
                                    'Cocoa'         : "#62DEBC",
                                    "Tea and maté"  : "#A2F5DE",
                                    
                                    "Oilcrops" : "#000000",
                                    "Other" : "#A2A2A2"},
              
               # "group_name_v7": {'Grains, roots, starchy carbohydrates' : "#e9f354",
               #                  'Legumes, beans, nuts' : "#54f3f1",
               #                  'Fruit and vegetables' : "#6ef354",
               #                  'Stimulants and spices' : "#7f54f3",
               #                  'Ruminant meat' : "#e0254a", 
               #                  'Dairy and eggs' : "#F7BDDD",
               #                  'Poultry and pig meat' : "#ff61cf", 
               #                  'Total' : "#000000"
               #                  }
               "group_name_v7": {'Grains, roots, starchy carbohydrates' : "#E69F00",
                                'Legumes, beans, nuts' : "#F0E442",
                                'Fruit and vegetables' : "#009E73",
                                'Stimulants and spices' : "#56B4E9",
                                'Ruminant meat' : "#D55E00", 
                                'Dairy and eggs' : "#0072B2",
                                'Poultry and pig meat' : "#CC79A7", 
                                'Total' : "#000000"
                                }
               }

gmap = {
    'Ruminant meat' : "Ruminant meat",
    'Pig meat'       : "Poultry and pig meat",
    'Poultry meat'   : "Poultry and pig meat",
    'Dairy'          : "Dairy and eggs",
    'Eggs'           : "Dairy and eggs",
    
    'Grains'             : "Grains, roots, starchy carbohydrates",
    "Rice"               : "Grains, roots, starchy carbohydrates",
    "Soybeans"           : "Legumes, beans, nuts",
    
    'Roots and tubers'   : "Grains, roots, starchy carbohydrates",
    'Vegetables'         : "Fruit and vegetables",
    'Legumes and pulses' : "Legumes, beans, nuts",
    
    'Bananas'           : "Fruit and vegetables",
    'Tropical fruit'    : "Fruit and vegetables",
    'Temperate fruit'   : "Fruit and vegetables",
    'Tropical nuts'     : "Legumes, beans, nuts",
    'Temperate nuts'    : "Legumes, beans, nuts",
    
    'Sugar beet'    : "#FFC000",
    'Sugar cane'    : "#F7C93B",
    'Spices'        : "Stimulants and spices",
    'Coffee'        : "Stimulants and spices",
    'Cocoa'         : "Stimulants and spices",
    "Tea and maté"  : "Stimulants and spices",
    
    "Oilcrops" : "#000000",
    "Other" : "#A2A2A2"}

colours = colourdict[GROUPING]

data_df = pd.DataFrame()
odf = pd.DataFrame()


diets_list = diets.columns

#%%
def invert_color(hex_color):
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')
    
    # Convert hex to RGB
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)
    
    # Invert RGB
    inverted_red = 255 - red
    inverted_green = 255 - green
    inverted_blue = 255 - blue
    
    # Convert back to hex
    inverted_hex = '#{0:02x}{1:02x}{2:02x}'.format(inverted_red, inverted_green, inverted_blue)
    
    return inverted_hex
def w_mean(df, col, cons_col):
    w_mean = (df[col] * df[cons_col]).sum() / (df[cons_col].sum())**2
    if type(w_mean) != float:
        w_mean = w_mean.squeeze()
    return w_mean / 1000
    
#%%
groups = np.concatenate([groups, ["Total"]])

for c in coi.keys():
    
    ccode = country_db[country_db.ISO3==c].M49
    cpop = (pop_dat[pop_dat["Area Code (M49)"]==ccode.squeeze()].Value * 1000).squeeze()
    
    try:
        kdf = pd.read_csv(os.path.join(resultsPath, c.lower(), "kdf.csv"),index_col=0)
        xdf = pd.read_csv(os.path.join(resultsPath, c.lower(), "xdf.csv"),index_col=0)
    except FileNotFoundError:
        resultsPath_ext = "D:\\Food_v0\\all_results"
        kdf = pd.read_csv(os.path.join(resultsPath_ext, c.lower(), "kdf.csv"),index_col=0)
        xdf = pd.read_csv(os.path.join(resultsPath_ext, c.lower(), "xdf.csv"),index_col=0)
    
    xdf["Consumer"] = c
    data_df = pd.concat([data_df, xdf])
    
    for g, group in enumerate(groups):
        
        print(group)
        
        if group == "Total":
            items = crop_db.Item
        else:
            items = crop_db[crop_db[GROUPING] == group].Item
        
        kdf_groupdat = kdf[kdf.Item.isin(items)]
        total_cap = kdf_groupdat.bd_opp_total.sum() / (cpop * 365)
        feed_cap = kdf_groupdat.bd_opp_feed.sum() / (cpop * 365)
        food_cap = kdf_groupdat.bd_opp_food.sum() / (cpop * 365)
        
        # food
        xdfg = xdf[xdf.Item.isin(items)]
        prov = xdfg.provenance.sum()
        domestic = xdfg[xdfg.Country_ISO == c]
        offshore = xdfg[xdfg.Country_ISO != c]
        dom_oc_food = domestic.bd_opp_cost_calc.sum()
        os_oc_food = offshore.bd_opp_cost_calc.sum()
        w_mean_food_domestic = w_mean(domestic, "bd_opp_cost_calc", "provenance")
        w_mean_food_offshore = w_mean(offshore, "bd_opp_cost_calc", "provenance")
        
        # feed
        xdfg = xdf[xdf.Animal_Product.isin(items)]
        domestic = xdfg[xdfg.Country_ISO == c]
        offshore = xdfg[xdfg.Country_ISO != c]
        if len(xdfg) > 0:
            w_mean_feed_domestic = w_mean(domestic, "bd_opp_cost_calc", "provenance")
            w_mean_feed_offshore= w_mean(offshore, "bd_opp_cost_calc", "provenance")
            dom_oc_feed = domestic.bd_opp_cost_calc.sum()
            os_oc_feed = offshore.bd_opp_cost_calc.sum()
        else:
            w_mean_feed_domestic = 0
            w_mean_feed_offshore = 0
            dom_oc_feed = 0
            os_oc_feed = 0
        
        tdom = np.nansum([w_mean_food_domestic, w_mean_feed_domestic])
        toff = np.nansum([w_mean_food_offshore, w_mean_feed_offshore])
        
        if (np.array([tdom,toff]) == 0).any():
            ratio = 0
        else:
            ratio = toff / tdom
        
        perc_dom = np.nansum([dom_oc_food, dom_oc_feed]) / np.nansum([os_oc_food, os_oc_feed, dom_oc_food, dom_oc_feed])
        perc_os = 1-perc_dom
        odf = pd.concat([odf, pd.DataFrame({
                        "a":c,
                        "g":group,
                        "total_cap": total_cap,
                        "feed_cap": feed_cap,
                        "food_cap": food_cap,
                        # "dom_kg" : tdom,
                        # "os_kg" : toff,
                        "ratio" : ratio,
                        "perc_os" : perc_os,
                        "cons" : prov,
                        "pop" : cpop},
            
                     index = [0])
                         ])
  
odf["cons_pc"] = odf.cons / odf["pop"]

odf.to_csv(os.path.join(resultsPath, f"odf_countries_{c}.csv"))
           
odf = odf[~(odf.g.isna())]
odf = odf[~odf.g.str.contains("sug",case=False)]
groups = odf.g.unique()
areas = odf.a.unique()


#%%
fig, ax = plt.subplots()
alpha = 0.8
figsize = (8, 7)
country_m49s = [country_db[country_db.ISO3==c].M49.squeeze() for c in areas]
mean_cals = cal_dat[cal_dat["Area Code (M49)"].isin(country_m49s)].Value.mean()

xgroups = groups[:-1]
xgroups = [k for k in colours.keys() if "Sugar" not in k]
exc_groups = ["Sugar beet", "Sugar cane", "Other", "Oilcrops"]
# exc_groups = ["Other", "Oilcrops"]
xgroups = groups[:-1]
xgroups = [k for k in colours.keys() if k not in exc_groups]

xgroups =['Ruminant meat',
          
             'Pig meat',
             'Poultry meat',
             
             'Dairy',
             'Eggs',
             
             'Grains',
             'Rice',
             'Roots and tubers',
             
             'Bananas',
             'Tropical fruit',
             'Temperate fruit',
             'Vegetables',
             
             'Soybeans',
             'Legumes and pulses',
             'Tropical nuts',
             'Temperate nuts',
             
             'Spices',
             'Coffee',
             'Cocoa',
             'Tea and maté']

area = list(coi.keys())[0]
    
ccode = country_db[country_db.ISO3==c].M49
cdat = odf[odf.a==area]
ccals = cal_dat[cal_dat["Area Code (M49)"]==ccode.squeeze()].Value.squeeze()

for d, diet in enumerate(diets):
    
    ctotal = 0
    
    cal_scalar = mean_cals / ccals
    
    mp = []
    
    for g, group in enumerate(xgroups):
        
        # color = colours[group]
        mapped_group = gmap[group]
        color = colourdict["group_name_v7"][mapped_group]
        
        val = cdat[cdat.g==group].total_cap.squeeze()

        if group in ["Tea and maté", "Coffee", "Cocoa", "Oilcrops", "Other", "Spices"]:
            scalar = 1
            ascale = 1
            # hatch = "//"
            hatch = None
            hcolor = invert_color(color)
            hcolor = color
            linewidth = 0
            
        else:
            scalar = diets["Baseline"].Cals / diets[diet].Cals
            ascale = 1
            hatch, hcolor = None, None 
            val = val * (diets[diet][group]/diets["Baseline"][group]) * scalar
            linewidth = 0
            
        if d == 0:
            label = mapped_group
            if label in mp:
                label = None
            else:
                mp.append(label)

            ax.bar(d, val, bottom = ctotal, 
                   color = color,
                   alpha = alpha *ascale,
                   # label = group,
                   label = label,
                   hatch = hatch,
                   edgecolor = hcolor,
                   linewidth = 0)
        else:
            ax.bar(d, val, bottom = ctotal, color = color,
                   alpha = alpha *ascale,
                   hatch = hatch,
                   edgecolor = hcolor,
                   linewidth = 0)
            
        ctotal = np.nansum([ctotal,val])
    
ax.legend(ncol = 2)
ax.set_xticks(np.arange(0, len(diets.columns),1), labels = diets.columns)
ax.set_ylabel(u"Extinction opportunity cost ($10^{-10}\Delta$E per-capita)")

fig = plt.gcf()
fig.set_size_inches(figsize)
fig.tight_layout()
