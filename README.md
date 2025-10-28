# MOM6-src-2024
MOM6 source code for Hogikyan and Jansen
including u_evap variable

The following files are different from August 1 version of MOM6-examples to implement u_ev, v_ev:
 - atmos_null/atmos_model.F90
 - coupler/atm_land_ice_flux_exchange.F90
 - coupler/surface_flux.F90

you must add "u_ev", "v_ev" to your data_table and specify files
