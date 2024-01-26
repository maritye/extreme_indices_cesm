#!/usr/bin/env python

import xarray as xr
import numpy as np
import pandas as pd

from importlib import reload

import config

"""
These functions are adapted from B Groenks 
temperature extreme indices as defined by the ETCCDI
"""

# Functions for calculating extreme indices
def warmest_night(ds, variable='TREFHTMN'):
    """
    Compute warmest night.
    Args:
        ds: Dataset.
        variable: parameter of choice. Defaults to CESM TREFHTMN
    Returns:
        Dataset of TNX
    """
    ds = xr.DataArray(ds[variable].groupby('time.year').max('time'), name='TNX')
#    ds = ds.rename({'TREFHTMN':'TNX'})
#    ds.attrs["unit"], ds.attrs["longname"] = "deg C", "Maximum Annual Daily Minimum Temperature"  
    return ds

def coolest_night(ds, variable='TREFHTMN'):
    """
    Compute coolest night.
    Args:
        ds: Dataset.
        variable: parameter of choice. Defaults to CESM TREFHTMN
    Returns:
        Dataset of TNN.
    """
    ds = xr.DataArray(ds[variable].groupby("time.year").min("time"), name='TNN')
    ds.attrs["unit"], ds.attrs["longname"] = "deg C", "Minimum Annual Daily Minimum Temperature"  
    return ds

def frost_days(ds, variable='TREFHTMN'):
    """
    Compute frost days.
    Args:
        ds: Dataset.
        variable: parameter of choice. Defaults to CESM TREFHTMN
    Returns:
        Dataset of FD
    """
    ds = xr.where(ds['TREFHTMN']<0,1,0).groupby('time.year').sum('time')
    ds.name = 'FD'
    ds.attrs["unit"], ds.attrs["longname"] = "days", "Frost Days; Tn less than 0C" 
    return ds


def tropical_nights(ds, variable='TREFHTMN'):
    """
    Compute tropical nights.
    Args:
        ds: Dataset.
        variable: parameter of choice. Defaults to CESM TREFHTMN
    Returns:
        Dataset of TR
    """
    ds = xr.where(ds['TREFHTMN']>20,1,0).groupby('time.year').sum('time')
    ds.name = 'TR'
    ds.attrs["unit"], ds.attrs["longname"] = "days", "Tropical Nights; Tn greater than 20C"
    return ds

def warmest_day(ds, variable='TREFHTMX'):
    """
    Compute maximum value of daily maximum temperature.
    Args:
        ds: Dataset.
        variable: parameter of choice. Defaults to CESM TREFHTMX
    Returns:
        Dataset of TXX
    """
    ds = xr.DataArray(ds[variable].groupby("time.year").max("time"),name='TXX')
    ds.attrs["unit"], ds.attrs["longname"] = "deg C", "Maximum Annual Daily Maximum Temperature"  
    return ds


def coolest_day(ds, variable='TREFHTMX'):
    """
    Compute minimum value of daily maximum temperature.
    Args:
        ds: Dataset.
        variable: parameter of choice. Defaults to CESM TREFHTMX
    Returns:
        Dataset of TXN
    """
    ds = xr.DataArray(ds[variable].groupby("time.year").min("time"), name='TXN')
    ds.attrs["unit"], ds.attrs["longname"] = "deg C", "Minimum Annual Daily Maximum Temperature"  
    return ds

def ice_days(ds, variable='TREFHTMX'):
    """
    Compute number of days below freezing.
    Args:
        ds: Dataset.
        variable: parameter of choice. Defaults to CESM TREFHTMX
    Returns:
        Dataset of ID
    """
    ds = xr.where(ds['TREFHTMX']<0,1,0).groupby('time.year').sum('time')
    ds.name = 'ID'
    ds.attrs["unit"], ds.attrs["longname"] = "days", "Ice Days; Tx less than 0C" 
    return ds

def summer_days(ds, variable='TREFHTMX'):
    """
    Compute days when Tx >25C
    Args:
        ds: Dataset.
        variable: parameter of choice. Defaults to CESM TREFHTMX
    Returns:
        Dataset of SU
    """
    ds = xr.where(ds['TREFHTMX']>25,1,0).groupby('time.year').sum('time')
    ds.name = 'SU'
    ds.attrs["unit"], ds.attrs["longname"] = "days", "Summer Days; Tx greater than 25C"
    return ds


def big_swings(ds, mask = None):
    """
    Compute the largest diurnal temperature range in any year.
    Args:
        ds: Dataset
        variable: parameter of choice. Defaults to CESM TREFHTMN
    Returns
        Dataset of annual maximum diurnal temperature range
        DTRX
        Dataarray if masked.
    """
    ds = ds.groupby('time.year').max('time')
    if not mask:
        ds = ds.rename({'TREFHTDTR':'DTRX'})
    if mask:
        ds = xr.DataArray(xr.where(mask['mask'].values==1,ds['TREFHTDTR'].values,np.NaN)).rename(
            'DTRX').rename({'dim_0':'year','dim_1':'lat','dim_2':'lon'})
    ds.attrs["unit"], ds.attrs["longname"] = "deg C", "Maximum Annual Diurnal Temperature Range"  
    return ds

def small_swings(ds, mask = None):
    """
    Compute the smallest diurnal temperature range in any year.
    Think this happens during heatwaves?
    Args:
        ds: Dataset
        variable: parameter of choice. Defaults to CESM TREFHTMN
    Returns:
        Dataset of annual minimum diurnal temperature range and date
        DTRN
        Dataarray if masked
    """
    ds = ds.groupby('time.year').min('time')
    if not mask:
        ds = ds.rename({'TREFHTDTR':'DTRN'})
    if mask:
        ds = xr.DataArray(xr.where(mask['mask'].values==1, ds['TREFHTDTR'].values, np.NaN)).rename(
            'DTRN').rename({'dim_0':'year', 'dim_1':'lat', 'dim_2':'lon'})
    ds.attrs['unit'], ds.attrs['longname'] = 'deg C', 'Minimum Annual Diurnal Temperature Range'
    return ds

def mean_dtr(ds, mask = None):
    """
    Compute the mean diurnal temperature range in any year.
    Args:
        ds: Dataset
        variable: parameter of choice. Defaults to CESM TREFHTMN
    Returns:
        Dataset of mean diurnal temperature range and date
        DTRM
        Dataarray if masked
    """
    ds = ds.groupby('time.year').mean('time')
    if not mask:
        ds = ds.rename({'TREFHTDTR':'DTRM'})
    if mask:
        ds = xr.DataArray(xr.where(mask['mask'].values==1, ds['TREFHTDTR'].values, np.NaN)).rename(
            'DTRM').rename({'dim_0':'year', 'dim_1':'lat', 'dim_2':'lon'})
    ds.attrs['unit'], ds.attrs['longname'] = 'deg C', 'Annual Mean Diurnal Temperature Range'
    return ds

def t_quant(ds, threshold=0.9, time0='1981-01-01', time1='2010-12-31', varname='TREFHTMX'):
    """
    Compute quantiles in temperature daily min and max data.
    Args:
        ds: Dataset.
        varname: TREFHTMX (assumes CESM output, daily maxima)
        threshold (float): upper quantile percent (as decimal). Defaults to 0.9
        time0 (str): First time for slice. Defaults to 1981-01-01
        time1 (str): Second time for slice. Defaults to 2010-12-31.
    Output:
        quantile for merging and use as threshold.
    """
    abx = varname[7]
    dp = ds.sel(time=slice(time0,time1)).quantile(q=[threshold],dim=['time']).squeeze().drop('quantile')
    dp.name = ('Q'+ abx + f"{str(int(float(0.9)*100))}")
    return dp

def annualnum_above_q(ds, thresh_data, threshold=0.9, varname='TREFHTMX'):
    """
    Compute number of days exceeding 90% temperature threshold per year
    Args:
        ds: Dataset
        thresh_data: Threshold dataset (computed using r_quant over all ensemble members)
        threshold: upper quantile percent as decimal, defaults to 0.95
        varname: PRECT assumes CESM output
    """
    abx = varname[7]
    ds = xr.where(ds[varname] > thresh_data,1,0).groupby('time.year').sum('time')
    #ds = ds.rename({('Q'+ abx + f"{str(int(float(threshold)*100))}"):('T'+ abx + f"{str(int(float(threshold)*100))}")})
    return ds

def annualnum_below_q(ds, thresh_data, threshold=0.1, varname='TREFHTMN'):
    """
    Compute number of days exceeding 90% temperature threshold per year
    Args:
        ds: Dataset
        thresh_data: Threshold dataset (computed using r_quant over all ensemble members)
        threshold: upper quantile percent as decimal, defaults to 0.95
        varname: PRECT assumes CESM output
    """
    abx = varname[7]
    ds = xr.where(ds[varname] < thresh_data,1,0).groupby('time.year').sum('time')
    #ds = ds.rename({('Q'+ abx + f"{str(int(float(threshold)*100))}"):('T'+ abx + f"{str(int(float(threshold)*100))}")})
    return ds
