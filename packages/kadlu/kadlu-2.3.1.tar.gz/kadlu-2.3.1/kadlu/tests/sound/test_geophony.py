""" Unit tests for the the 'sound.geophony' module in the 'kadlu' package

    Authors: Oliver Kirsebom
    contact: oliver.kirsebom@dal.ca
    Organization: MERIDIAN-Intitute for Big Data Analytics
    Team: Acoustic data Analytics, Dalhousie University
    Project: packages/kadlu
             Project goal: Tools for underwater soundscape modeling
     
    License:

"""

import pytest
import os
import numpy as np
from kadlu.sound.geophony import geophony, transmission_loss, kewley_sl_func, source_level
from kadlu.geospatial.ocean import Ocean
from kadlu.utils import R1_IUGG, deg2rad

current_dir = os.path.dirname(os.path.realpath(__file__))
path_to_assets = os.path.join(os.path.dirname(current_dir),"assets")

def test_kewley_sl_func():
    sl1 = kewley_sl_func(freq=10, wind_uv=0)
    sl2 = kewley_sl_func(freq=40, wind_uv=2.57)
    assert sl1 == sl2
    assert sl2 == 40.0
    sl3 = kewley_sl_func(freq=40, wind_uv=5.14)
    assert sl3 == 44.0
    sl4 = kewley_sl_func(freq=100, wind_uv=5.14)
    assert sl4 == 42.5

def test_source_level():
    ok = {'load_bathymetry': 10000, 'load_wind_uv': 5.14}
    o = Ocean(**ok)
    sl = source_level(freq=10, x=0, y=0, area=1, ocean=o, sl_func=kewley_sl_func)
    assert sl == 44.0
    sl = source_level(freq=100, x=[0,100], y=[0,100], area=[1,2], ocean=o, sl_func=kewley_sl_func)
    assert sl[0] == 42.5
    assert sl[1] == sl[0] + 10*np.log10(2)

def test_geophony_flat_seafloor():
    """ Check that we can execute the geophony method for a 
        flat seafloor and uniform sound speed profile"""
    kwargs = {'load_bathymetry':10000, 'load_wind_uv':1.0, 'ssp':1480, 'angular_bin':90, 'dr':1000, 'dz':1000}
    geo = geophony(freq=100, south=44, north=46, west=-60, east=-58, depth=[100, 2000], xy_res=71, **kwargs)
    spl = geo['spl']
    x = geo['x']
    y = geo['y']
    assert x.shape[0] == 3
    assert y.shape[0] == 5
    assert spl.shape[0] == 3
    assert spl.shape[1] == 5
    assert spl.shape[2] == 2
    assert np.all(np.diff(x) == 71e3)
    assert np.all(np.diff(y) == 71e3)
    # try again, but this time for specific location
    kwargs = {'load_bathymetry':10000, 'load_wind_uv':1.0, 'ssp':1480, 'angular_bin':90, 'dr':1000, 'dz':1000, 'propagation_range':50}
    geo = geophony(freq=100, lat=45, lon=-59, depth=[100, 2000], **kwargs)

def test_geophony_in_canyon(bathy_canyon):
    """ Check that we can execute the geophony method for a 
        canyon-shaped bathymetry and uniform sound speed profile"""
    kwargs = {'load_bathymetry':bathy_canyon, 'load_wind_uv':1.0, 'ssp':1480, 'angular_bin':90, 'dr':1000, 'dz':1000}
    z = [100, 1500, 3000]
    geo = geophony(freq=10, south=43, north=46, west=60, east=62, depth=z, xy_res=71, **kwargs)
    spl = geo['spl']
    x = geo['x']
    y = geo['y']
    assert spl.shape[0] == x.shape[0]
    assert spl.shape[1] == y.shape[0]
    assert spl.shape[2] == len(z)
    assert np.all(np.diff(x) == 71e3)
    assert np.all(np.diff(y) == 71e3)    
    # check that noise is NaN below seafloor and non Nan above
    bathy = np.swapaxes(np.reshape(geo['bathy'], newshape=(y.shape[0], x.shape[0])), 0, 1)
    bathy = bathy[:,:,np.newaxis]
    xyz = np.ones(shape=bathy.shape) * z
    idx = np.nonzero(xyz >= bathy)
    assert np.all(np.isnan(spl[idx]))
    idx = np.nonzero(xyz < bathy)
    assert np.all(~np.isnan(spl[idx]))

def test_transmission_loss_real_world_env():
    """ Check that we can initialize a transmission loss object 
        for a real-world environment and obtain the expected result """

    from datetime import datetime
    bounds = dict(
               start=datetime(2015,1,1), end=datetime(2015,1,2), 
               top=0, bottom=10000
             )    
    src = dict(load_bathymetry='gebco', load_temp='hycom', load_salinity='hycom')
    sound_source = {'freq': 200, 'lat': 43.8, 'lon': -59.04, 'source_depth': 12}
    seafloor = {'sound_speed':1700,'density':1.5,'attenuation':0.5}
    transm_loss = transmission_loss(seafloor=seafloor, propagation_range=20, **src, **bounds, **sound_source, dr=100, angular_bin=45, dz=50)

    tl_h, ax_h, tl_v, ax_v = transm_loss.calc(vertical=True)

    answ_h = np.array([ [ 97.6, 117.2, 115.,  119.3, 119.7, 120.3, 121.3, 122.1, 122.9, 123.5],
                        [ 97.6, 116.5, 117.7, 117.8, 120.1, 122.1, 121.3, 123.5, 120.2, 122.7],
                        [ 97.6, 114.3, 117.2, 118.4, 120.6, 120.2, 122.2, 120.4, 125.4, 121.1],
                        [ 97.6, 117.6, 117.9, 117.8, 117.7, 121.1, 119.9, 120.7, 122.3, 123.6],
                        [ 97.6, 114.6, 117.6, 117.5, 116.9, 120.1, 121.8, 120.1, 119.8, 121.3],
                        [ 97.6, 110.4, 115.5, 119.6, 119. , 117.9, 117.7, 123.4, 120.7, 122.3],
                        [ 97.6, 110.2, 114.8, 117.8, 123.7, 120.1, 121. , 121.7, 123.8, 120.4],
                        [ 97.6, 112. , 115.7, 118.4, 119.1, 120.2, 121.2, 122. , 122.8, 123.5]])

    answ_v = np.array([ [31.9, 65.4, 68.1, 70.1, 71.3, 72.4, 73.4, 74.2, 75.0, 75.7, 76.3],
                        [53.4, 147.3, 145.0, 148.3, 148.9, 150.6, 150.9, 150.2, 150.7, 151.5, 152.2],
                        [59.5, 164.8, 161.9, 165.3, 166.0, 167.6, 167.9, 167.2, 167.6, 168.5, 169.1],
                        [63.7, 175.1, 172.2, 175.6, 176.3, 177.8, 178.2, 177.5, 177.9, 178.7, 179.4],
                        [67.6, 182.7, 179.8, 183.2, 184.0, 185.5, 185.8, 185.1, 185.6, 186.4, 187.1],
                        [71.8, 189.4, 186.5, 189.9, 190.6, 192.1, 192.5, 191.8, 192.2, 193.0, 193.7],
                        [77.9, 195.1, 193.6, 197.9, 202.1, 200.8, 201.5, 201.7, 202.4, 203.1, 203.8],
                        [98.9, 214.0, 215.1, 219.7, 224.7, 223.1, 224.0, 224.8, 225.5, 226.2, 226.8]])

    np.testing.assert_array_almost_equal(tl_h[0,0,:,::20], answ_h, decimal=1) 
    np.testing.assert_array_almost_equal(tl_v[0,1::10,::20,0], answ_v, decimal=1) 
    assert tl_h.shape == (1,1,8,200), f'tl_h.shape = {tl_h.shape}'
    assert tl_v.shape == (1,72,201,8), f'tl_v.shape = {tl_v.shape}'


def test_transmission_loss_flat_seafloor():
    """ Check that we can initialize a transmission loss object 
        for a flat seafloor and uniform sound speed profile """
    transm_loss = transmission_loss(freq=100, source_depth=75, propagation_range=0.5, load_bathymetry=2000, ssp=1480, angular_bin=10)
    tl_h, ax_h, tl_v, ax_v = transm_loss.calc(vertical=True)
    answ = np.genfromtxt(os.path.join(path_to_assets, 'lloyd_mirror_f100Hz_SD75m.csv'), delimiter=",")
    assert answ.shape == tl_v[0,:,:,0].shape
    np.testing.assert_array_almost_equal(-tl_v[0,1:,:,0], answ[1:,:], decimal=3) 

#def test_test():
#    from datetime import datetime
#    bounds = dict(
#               south=43.53, north=44.29, west=-59.84, east=-58.48,
#               start=datetime(2015,1,1), end=datetime(2015,1,2), 
#               top=0, bottom=10000
#             )    
#    src = dict(load_bathymetry='chs', load_temp='hycom', load_salinity='hycom')
#    sound_source = {'freq': 200, 'lat': 43.8, 'lon': -59.04, 'source_depth': 12}
#    o = Ocean(**src, **bounds)
#    seafloor = {'sound_speed':1700,'density':1.5,'attenuation':0.5}
#    transm_loss = transmission_loss(seafloor=seafloor, propagation_range=20, **src, **bounds, **sound_source, ssp=1480, dz=50)
#    transm_loss.calc(vertical=False)
