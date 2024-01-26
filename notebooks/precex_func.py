#!/usr/bin/env python

import xarray as xr
import numpy as np
import pandas as pd
import utils

from importlib import reload

import config

"""
These functions are adapted from climdex (in R) and xclim to extract
precipitation extreme indices as defined by the ETCCDI

Annual maximum 1 and 5day totals, quantile of wet day precipitation, contribution of quantile to annual total
number of days above threshold
"""

def yearly_rx1day(ds, varname = 'PRECT'):
    """
    Compute the annual maximum 24h precipitation total
    Args:
        ds: Dataset
        varname: assumes 'PRECT' 
    """
    ds = xr.DataArray(ds[varname].groupby('time.year').max('time'), name='RX1D')

    return ds
    
def yearly_rx5day(ds, varname = 'PRECT'):
    """
    Compute the annual maximum 5 day precipitation total
    Args:
        ds: Dataset
        varname: assumes 'PRECT'
    """
    ds = xr.DataArray(ds[varname].rolling(time=5).sum().groupby('time.year').max('time'), name='RX5D')

    return ds

def r_quant(ds, threshold=0.95, time0='1981-01-01', time1='2010-12-31', varname='PRECT'):
    """
    Compute quantiles in rainfall data. Calculates for days with >=1mm.
    Args:
        ds: Dataset.
        varname: PRECT (assumes CESM output)
        threshold (float): Lower quantile percent (as decimal). Defaults to 0.95
        time0 (str): First time for slice. Defaults to 1981-01-01
        time1 (str): Second time for slice. Defaults to 2010-12-31.
    """
    dp = ds.sel(time=slice(time0,time1)).where(ds[varname] > 1).quantile(q=[threshold],dim=['time']).squeeze().drop('quantile')
    dp = dp.to_array(name=(f"Q{str(int(float(threshold)*100))}"))
    return dp

def annualtot_above_q(ds, thresh_data, threshold=0.95, varname='PRECT'):
    """
    Compute total precipitation from days exceeding threshold
    Args:
        ds: Dataset.
        thresh_data: Threshold dataset (computed using r_quant over all members).
        threshold (float): Upper quantile percent (as decimal) defaults to 0.95
        varname: PRECT. assumes CESM output
    """
    ds = xr.where(ds[varname] > thresh_data,ds[varname],0).groupby('time.year').sum('time')
    ds = ds.to_array(name = (f"PR{str(int(float(threshold)*100))}")).squeeze().drop('variable')
    return ds

def annualnum_above_q(ds, thresh_data, threshold=0.95, varname='PRECT'):
    """
    Compute number of days exceeding threshold per year
    Args:
        ds: Dataset
        thresh_data: Threshold dataset (computed using r_quant over all ensemble members)
        threshold: upper quantile percent as decimal, defaults to 0.95
        varname: PRECT assumes CESM output
    """
    ds = xr.where(ds[varname] > thresh_data,1,0).groupby('time.year').sum('time')
    ds = ds.to_array(name = (f"N{str(int(float(threshold)*100))}")).squeeze().drop('variable')
    return ds

def ann_prop_above(ds, thresh_data, threshold=0.95, varname = 'PRECT'):
    """
    Compute proportion of annual total precipitation derived from days
    above a high threshold
    Args:
        ds: Dataset
        thresh_data: Threshold dataset (computed using r_quant over all ensemble members)
        threshold: upper quantile percent as decimal. defaults to 0.95
        varname: PRECT assuming CESM output
    time_dim assumes 'time'
    uses prcptot function for annual total
    """
    dtop = annualtot_above_q(ds, thresh_data, threshold, varname)
    dbot = prcptot(ds)
    return xr.DataArray(dtop/dbot, name=(f"P{str(int(float(threshold)*100))}tot"))


def nwd(ds, varname = 'PRECT'):

    """
    Annual count of wet days when precipitation exceeds 1mm.
    Args:
        ds: Dataset
        varname: variable name. Defaults to PRECT for CESM output.
    """
    ds = xr.where(ds[varname]>=1,1,0).groupby('time.year').sum('time')
    ds.name = 'NWD'
    ds.attrs["unit"], ds.attrs["longname"] = "days", "Number of wet days. Days with >1mm rain"
    return ds

"""
The following are essentially copied from B Groenks with 
Additional features that I don't understand removed. MT.
"""

def annual_rnmm(ds, nmm, varname = 'PRECT'):
    '''
    Annual count of days when precipitation exceeds n mm.
    Exactly the same as nwd function above if 1mm chosen
    '''
    def _count_rnmm(x, axis):
        return np.sum(x >= nmm, axis = axis)
    X_arr = xr.DataArray(ds[varname])
    return X_arr.groupby('time.year').reduce(_count_rnmm)

def annual_r10mm(ds, varname='PRECT'):
    """
    Annual count of heavy rain days
    When precipitation exceeds 10mm
    """
    ds = xr.where(ds[varname]>=10,1,0).groupby('time.year').sum('time')
    return xr.DataArray(ds, name = 'R10mm')

def annual_r20mm(ds, varname = 'PRECT'):
    """
    Annual count of very heavy rain days
    When precipitation exceeds 20mm
    """
    ds = xr.where(ds[varname]>=20,1,0).groupby('time.year').sum('time')
    return xr.DataArray(ds, name = 'R20mm')

def prcptot(ds, varname ='PRECT'):
    """
    Total precipitation over one year
    """
    return xr.DataArray(ds[varname].groupby('time.year').sum('time'), name ='PTOT')

def sdii(ds, varname = 'PRECT'):
    """
    Simple daily intensity index.
    Ratio of total annual precipitation to the total number of wet days
    """
    return xr.DataArray(prcptot(ds)/nwd(ds), name='SDII')

def cdd(ds, varname = 'PRECT'):
    """
    Maximum number of consecutive dry days per year
    """
    def _cdd(x, axis):
        has_no_precip = x <= (1.0)
        return utils.max_consecutive_count(has_no_precip)
    return xr.DataArray(ds[varname].groupby('time.year').reduce(_cdd, dim ='time'), name='CDD')


def cwd(ds, varname = 'PRECT'):

    """
    Maximum number of consecutive wet days per year
    """
    def _cwd(x, axis):
        has_precip = x >= (1.0)
        return utils.max_consecutive_count(has_precip)
    return xr.DataArray(ds[varname].groupby('time.year').reduce(_cwd, dim ='time'), name='CWD')
   