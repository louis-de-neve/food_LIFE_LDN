import sys
sys.path.append("model")
import model._consumption_provenance
import model._get_impacts
import model._process_dat
import model.global_commodity_impacts

import pandas as pd
import os
from multiprocessing import Pool
from tqdm import tqdm
import logging
from functools import partial

MULTIPROCESSING = True
NUM_PROCESSES = 20
OVERWRITE = True
BD_PATH = "/maps/tsb42/bd_opp_cost/v4_GOMP/agri_intersect/outputs/country_opp_cost_v6_GOMP.csv"
RESULTS_PATH = "../results"

def process_country(coi_iso, results_path="results", 
                    dat_path = "model", 
                    bd_path = os.path.join("model", "dat", "country_opp_cost_v6.csv")):
    
    coi_iso = coi_iso.upper()
    cdat = pd.read_excel(os.path.join("model", "dat", "nocsDataExport_20220822-151738.xlsx"))
    coi_code = cdat[cdat["ISO3"]==coi_iso]["FAOSTAT"].values.squeeze()
    
    scenPath = os.path.join(results_path, coi_iso) # where the results of this run 
                                            # are to be saved

    if not os.path.isdir(scenPath):
        os.makedirs(scenPath)

    years = [2017,2018,2019,2020,2021]
    sua = pd.read_csv(os.path.join(dat_path, "dat",
                        "SUA_Crops_Livestock_E_All_Data_(Normalized).csv"),
                        encoding = "latin-1")

    fs = sua[(sua["Area Code"]==coi_code)&(sua["Element Code"]==5141)&(sua.Year.isin(years))]

    hprov_path = os.path.join(scenPath, "human_provenance.csv")
    fprov_path = os.path.join(scenPath, "feed.csv")
    
    try:
       
        if OVERWRITE or not os.path.isfile(hprov_path) or not os.path.isfile(fprov_path):
            model._consumption_provenance.main(fs, coi_iso, scenPath, dat_path)

        feedimp_path = os.path.join(scenPath, "feed_impacts_wErr.csv")
        if OVERWRITE or not os.path.isfile(feedimp_path):
            fprov = pd.read_csv(fprov_path, index_col = 0)
            model._get_impacts.get_impacts(fprov, 2019, coi_iso, scenPath, dat_path, bd_path).to_csv(feedimp_path)

        humanimp_path = os.path.join(scenPath, "human_consumed_impacts_wErr.csv")
        if OVERWRITE or not os.path.isfile(humanimp_path):
            hprov = pd.read_csv(os.path.join(scenPath, "human_consumed.csv"), index_col = 0)
            model._get_impacts.get_impacts(hprov, 2019, coi_iso, scenPath, dat_path, bd_path).to_csv(humanimp_path)

        if OVERWRITE or not os.path.isfile(os.path.join(scenPath, "xdf.csv")):
            model._process_dat.main(dat_path, scenPath, bd_path, coi_code)

    except Exception as e:
        logger.error(f"Error processing country {coi_iso}: {e}")
        return
    
if __name__ == '__main__':

    cpath = os.path.join("model", "dat", "nocsDataExport_20220822-151738.xlsx")
    cdat = pd.read_excel(cpath)
    countries = [_ for _ in cdat["ISO3"].unique().tolist() if isinstance(_, str)]

    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='errors.log', encoding='utf-8', level=logging.DEBUG)

    if MULTIPROCESSING:
        
        process_country_partial = partial(process_country, bd_path=BD_PATH, results_path=RESULTS_PATH)

        with Pool(processes=NUM_PROCESSES) as pool:

            results = list(tqdm(pool.imap(process_country_partial, countries), total=len(countries)))

    else:
        for coi_iso in countries:
            process_country(coi_iso, bd_path=BD_PATH, results_path=RESULTS_PATH)

    model.global_commodity_impacts.main(OVERWRITE, BD_PATH, RESULTS_PATH)





