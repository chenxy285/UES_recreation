This repository contains the codes, data, and output of the analysis of green space accessibility in Singapore. It is 
to answer the question of to what extent the neighbourhood green space meet the recreational needs of residents.

## 1. Data processing: clean the questionnaire data
   (1) **Input:** the csv file of the questionnaire data about the visit frequency and visit duration of 1000 respondents to 
         the neighbourhood green spaces \(NGS\) and further green spaces \(GS\). This data is confidential and not 
uploaded.  
   (2) **Output:** two csv files of NGS and GS visits respectively. Each file contains three columns:
MSNO \(respondent ID\), total_dur \(total visit duration for this respondent in last year\), and
PostalCode \(the postal code of the respondent's residential address). The two output files are named: `ngs_clean.csv`
and `park_clean.csv`.  
   (3) **Commands:** `python codes/data_processing.py`


## 2. Geocoding: convert the postal codes to geo-coordinates for each respondent
   (1) **Input:** `ngs_clean.csv` and `park_clean.csv`  
   (2) **Output:** two csv files containing geo-coordinates of the residential address of each respondent. The files are
named `ngs_coords.csv` and `park_coords.csv`. The geocoding is conducted using OneMap API. An account need to be
registered and a token need to be retrieved from [OneMap API](https://www.onemap.gov.sg/apidocs/).  
   (3) **Commands:** `python codes/geocoding.py`
 

## 3. Ratio calculation: aggregate the respondents by HDB towns, subzones amd planning areas and calculate the 
near-to-far visit ratio
   (1) **Input:** spatial data of planning unit boundaries at three different level \(stored in [here](data/boundaries) \)
and `ngs_coords.csv`, `park_coords.csv`.  
   (2) **Output:** three geojson files of three planning unit boundaries attached with the median ratio of all respondents
in each unit, named `ratio_town.geojson`, `ratio_PA.geojson`, `ratio_subzone.geojson`.  
   (3) **Commands:** `python codes/near_to_far_ratio.py`.  
   (4) How do we calculate the ratio? Total duration spent on NGS / total duration spent on GS, first aggregated by each
respondent using median, next aggregated by three different levels of planning units using median too. \(We used median
as the data is highly skewed.)

## 4. Plotting: generate the maps and histograms to present the results.
   (1) **Input:** `ratio_town.geojson`, `ratio_PA.geojson`, `ratio_subzone.geojson`, `park_clean.csv`, and `ngs_clean.csv`  
   (2) **Output:** distribution maps of the ratios and histograms at the overall level and three planning unit levels.  
   (3) **Commands:** `python codes/plotting.py` and `python codes/histogram.py`  
