from sirc import Epidemie
import numpy as np

# dosis_bei_der_die_hälfte_krank_wird, dauer_der_simulation, erreger_produktion, erregerzerfall, sterberate, volumen, population
betatest = Epidemie([1400,1600], 400, 900000000, np.exp(-4.18), 0.08, 300000, 100000)

sim = betatest.simulation()

betatest.populations_plot(sim)

betatest.kontzentrations_plot(sim)