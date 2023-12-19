## Essential checklist for your repository
- [ ] Update the environment.yml file in include the required libraries/packages
- [ ] Your analysis code/notebooks!

## Extreme Indices in CESM
These notebooks form the basis of Tye's workflow to extract and analyse extreme precipitation and temperature indices in CESM under climate change, and in response to climate interventions (e.g. Stratospheric Aerosol Injection).  
They are not necessarily the most efficient scripts! They are also submitted as is, with possible errors. If you find a glaring error, please let me know :)

The extreme indices were defined by the WCRP Extreme Task force for Climate Change Detection and are described in full by Zhang et al. 2011 (10.1002/wcc.147) among others.  

## Contents
Two function files leverage functions created by bgroenks96 https://github.com/bgroenks96
* precex_func
* tempex_func

Three notebooks to extract data from campaign storage, calculate indices, calculate anomalies from a base climate and the significance of changes. A notebook for plotting results.

## Indices
### Temperature
Annual frost days (FD, daily minimum <0C)  
Annual tropical nights (TR, daily minimum >25C)  
Annual icing days (ID, daily maximum <0C)  
Annual summer days (SU)   
Annual max daily max temp (TXx)  
Annual min daily max temp (TXn)  
Annual max daily min temp (TNx)  
Annual min daily min temp (TNx)  
Annual Warm Days (TX90, daily maximum >90th Percentile)  
Annual Warm Nights (TX90, daily maximum >90th percentile)  
Annual Cool Days (TN90, daily minimum <10th percentile)  
Annual Cool Nights (TN90, daily minimum <10th percentile)  

### Precipitation

Annual maximum 1-day precipitation (Rx1day)  
Annual maximum 5-day precip (Rx5day)  
Annual frequency of days >10mm precip (R10mm)  
Annual frequency of day >20mm precip (R20mm)  
Annual frequency of days >n mm precip (Rnmm)  
Annual total precipitation (PRCPTOT)  
Annual Simple daily intensity index (SDII, ratio of total precipitation on wet days)  
Annual longest dry spell (CDD, consecutive days <1mm)  
Annual longest wet spell (CWD, consecutive days >1mm)  
Annual total rain from days above a threshold (e.g. >95th percent of wet day precipitation)  
Annual frequency of days above a threshold  

   
