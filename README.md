# visibility
Computes CHEOPS and JWST visibility for any target during the year

Predicts visibility for targets by CHEOPS and JWST. 
Accuracy for CHEOPS targets is +/- 1 day

Only the Sun avoidance zone for the respective missions are
taken into account when evaluating visibility, not the
instantaneous orbits of the space telescopes. This means that 
e.g. the observing efficiency of CHEOPS is not estimated and
the more complex visibility checker should be used to determine
it. New: A CHEOPS visibility checker computing efficiencies is
now available: https://gitlab.unige.ch/cheops/CHEOPS_visibility_tool

Example of use:

    import visibility as vi
    
    print('Is 55 Cnc visible to JWST on 2022-11-21 ?') 
    b = vi.jwst_vis('55 Cnc', '2022-11-21') 
    print(f'Answer is {b}') # True (Yes)
    
    print('Is 55 Cnc visible to CHEOPS on 2022-11-21 ?') 
    b = vi.cheops_vis('55 Cnc', '2022-11-21') 
    print(f'Answer is {b}') # False (No)

    print('When during the year is WASP-12 visible to both CHEOPS and JWST?') 
    vi.visibility('WASP-12', telescope='BOTH')
    # Answer is "WASP-12: 0209-0225, 1031-1116", i.e.
    # February 9-25 and October 31 to November 16.

    print('When during the year is TOI-500 visible to CHEOPS?') 
    vi.visibility('TOI-500', telescope='CHEOPS')
    # Answer is "TOI-500: Not visible" (never)

@author: Alexis Brandeker (alexis@astro.su.se)
