# This repository contains code and data to accompany the manuscript "Quantifying the impact of food we eat on species extinctions".
# Thomas S Ball,  10/04/2025

All code contained in this repository is written in Python, and thus require a working Python environment to work, but aside from some minor modification of file paths should not require any modification.

The scripts rely on the Python standard library, alongside pandas, numpy, and openpyxl, alongside matplotlib for the plotting scripts. These are found in the 'reqs' file, and can be installed by running 'pip install -r reqs'.

The code requires extra data sources to run correctly:
	 - Supply utilisation accounts from FAOSTAT, obtained from here: https://www.fao.org/faostat/en/#data/SCL. Navigate to this page, and on the right handside under 'Bulk downloads' selected 'All Data'. This file should be placed in the 'dat' folder, and named "SUA_Crops_Livestock_E_All_Data_(Normalized).csv".

	 - Production data from FAOSTAT, obtained from: https://www.fao.org/faostat/en/#data/QCL. On the righthand side, again select 'All Data'. This file should be placed in the 'dat' folder and named "Production_Crops_Livestock_E_All_Data_(Normalized).csv".

	 -"TradeMatrixFeed_import_dry_matter_2013.csv" is unfortuantely too large to be included in a github.com repository, and so has to be obtained by running the code accompanying Schwarzmueller (2022, zenodo.org/records/5751294). Run the code from Schwarzmueller following the instructions contained therein, and place the resulting file into the 'dat' folder. Note that other files from Schwarzmueller are already included to minimise the number of files the user is required to procure.

 With all the data in place, running the code requires you to execute 'run_head.py' as a python script, modifying the script itself to select the country-of-interest and corresponding output folder. Output files are not named in a country specific way, so you must create a seperate output folder for each country (for example: results/GBR, results/USA etc).

