# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 03:09:58 2022

Predicts visibility for targets by CHEOPS and JWST
Accuracy for CHEOPS targets is +/- 1 day

Only the Sun avoidance zone for the respective missions are
taken into account when evaluating visibility, not the
instantaneous orbits of the space telescopes. This means that 
e.g. the observing efficiency of CHEOPS is not estimated and
the more complex visibility checker should be used to determine
it.

@author: Alexis Brandeker (alexis@astro.su.se)
"""
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord, get_sun, get_icrs_coordinates

JWST_min_sep = 85*u.deg     # Minimum angle to sun for JWST target
JWST_max_sep = 137*u.deg    # Maximum angle to sun for JWST target
CHEOPS_min_sep = 120*u.deg  # Minimum angle to sun for CHEOPS target


def cheops_vis(target_name, date_str):
    """Checks if target_name is visible by CHEOPS
    at date_str (format 'YYYY-MM-DD'). Returns boolean.
    """
    return visible(target_name, date_str, telescope='CHEOPS')


def jwst_vis(target_name, date_str):
    """Checks if target_name is visible by JWST
    at date_str (format 'YYYY-MM-DD'). Returns boolean.
    """
    return visible(target_name, date_str, telescope='JWST')
    

def visible(target_name, date_str, telescope='CHEOPS'):
    """Checks if target_name is visible by telescope
    at date_str (format 'YYYY-MM-DD'). Returns boolean.
    """
    coo = get_icrs_coordinates(target_name)
    date = Time(date_str)
    return visible_coo(coo, date, telescope=telescope)


def visible_coo(target_coo, date, telescope='CHEOPS'):
    """Checks if coordinate target_coo [SkyCoord] is visible by
    telescope at date [Time]. telescope can be 'CHEOPS', 'JWST',
    or 'BOTH'. Returns boolean.
    """
    sun_gcrs = get_sun(date)
    sun_icrs = SkyCoord(ra=sun_gcrs.ra, dec=sun_gcrs.dec)
    sep = target_coo.separation(sun_icrs)        

    if telescope == 'JWST':
        return  (sep >= JWST_min_sep) & (sep <= JWST_max_sep)
    if telescope == 'BOTH':
        return  ((sep > CHEOPS_min_sep) & 
                 (sep >= JWST_min_sep) &
                 (sep <= JWST_max_sep))
    return  sep > CHEOPS_min_sep


def visibility(target_name, telescope='CHEOPS'):
    """Prints visibility ranges of target_name through the year.
    telescope can be 'CHEOPS', 'JWST', or 'BOTH'
    Output format is string with "mmdd-MMDD" where mm & MM are month
    numbers and dd & DD are days of month. E.g., 0209-0225 means it
    is visible 9-25 February.
    """
    coo = get_icrs_coordinates(target_name)
    new_year = Time('2001-01-01')
    stat = visible_coo(coo, new_year, telescope)
    
    vis_ranges = []
    
    for n in range(1,365):
        new_date = new_year + n*u.day
        new_stat = visible_coo(coo, new_date, telescope)
        if stat == new_stat:
            continue
        if stat:
            new_date -= 1*u.day
        monthdaystr = '{:02d}{:02d}'.format(new_date.datetime.month,
                                            new_date.datetime.day)
        if stat:
            if len(vis_ranges) == 0:
                last_vis = monthdaystr
            else:
                vis_ranges[-1][1] = monthdaystr
        else:
            vis_ranges.append([monthdaystr,None])
        stat = new_stat
    
    if len(vis_ranges) == 0:
        print('{:s}: Not visible'.format(target_name))
        return
    
    if vis_ranges[-1][1] is None:
        vis_ranges[-1][1] = last_vis

    str_range = vis_ranges[0][0]+'-'+vis_ranges[0][1]
    for n in range(1, len(vis_ranges)):
        str_range += ', '+ vis_ranges[n][0]+'-'+vis_ranges[n][1]
    print('{:s}: {:s}'.format(target_name, str_range))
        
    
def max_solar_angle(target_name):
    """Given target_name, computes the maximum angle between the target and the
    Sun. Returns maximum angle in degrees.
    """
    target_coo = get_icrs_coordinates(target_name)
    new_year = Time('2001-01-01')
    max_sep = -1*u.deg

    for n in range(1,365):
        date = new_year + n*u.day
        sun_gcrs = get_sun(date)
        sun_icrs = SkyCoord(ra=sun_gcrs.ra, dec=sun_gcrs.dec)
        sep = target_coo.separation(sun_icrs)        
        if max_sep < sep:
            max_sep = sep
    print('{:.2f}'.format(max_sep))
    return max_sep


if __name__ == '__main__': 

# Examples
    print('Is 55 Cnc visible to JWST on 2022-11-21 ?') 
    b = jwst_vis('55 Cnc', '2022-11-21') 
    print(f'Answer is {b}') # True (Yes)
    
    print('Is 55 Cnc visible to CHEOPS on 2022-11-21 ?') 
    b = cheops_vis('55 Cnc', '2022-11-21') 
    print(f'Answer is {b}') # False (No)

    print('When during the year is WASP-12 visible to both CHEOPS and JWST?') 
    visibility('WASP-12', telescope='BOTH')
    # Answer is "WASP-12: 0209-0225, 1031-1116", i.e.
    # February 9-25 and October 31 to November 16.

    print('When during the year is TOI-500 visible to CHEOPS?') 
    visibility('TOI-500', telescope='CHEOPS')
    # Answer is "TOI-500: Not visible" (never)

    print('What is the maximum angular distance between beta Pic and the Sun?')
    max_solar_angle('beta Pic')
    # Answer is 105.58 deg

    