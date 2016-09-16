
"""
Plot masses as a function of metallicity.
"""

from astropy.table import Table, join

teff_solar, numax_solar, Dnu_solar = (5777, 3140, 135.0)


# Hekker + APOGEE + TGAS
hekker = Table.read("../tgas-hekker-apogee.fits")

# Calculate masses from scaling relations.
for i in range(1, 7):
    Dnu, numax = ("Dnu{:.0f}".format(i), "nu{:.0f}".format(i))

    mass = (hekker[numax]/numax_solar)**3 \
         * (hekker[Dnu]/Dnu_solar)**(-4) \
         * (hekker["TEFF"]/teff_solar)**(3.0/2.0)


    hekker["mass_{:.0f}".format(i)] = mass



# Pinnsonault + TGAS
pinnsonault = Table.read("../tgas-pinnsonault.fits")



# Show links of stars?
# TODO:




fig, ax = plt.subplots()

# Plot Pinnsonault first
p_ok = np.ones(len(pinnsonault), dtype=bool)
# Note __M_H_2 is calibrated ASPCAP metallicity
ax.scatter(
    pinnsonault["__M_H_2"][p_ok],
    pinnsonault["M1"][p_ok],
    facecolor="#e67e22", s=50)


# Plot Hekker 1
h_ok = np.ones(len(hekker), dtype=bool)
ax.scatter(
    hekker["PARAM_M_H"][h_ok],
    hekker["mass_1"][h_ok],
    facecolor="#3498db", s=50)


epstein = Table.read("../tgas-epstein.fits")

ax.scatter(
    epstein["__M_H_2"],
    epstein["SR_MASS"],
    facecolor="#27ae60", s=50)


ax.set_xlabel(r"$[{\rm Fe/H}]$")
ax.set_ylabel(r"$\mathcal{M}$ $[\mathcal{M}_\odot]$")

fig.savefig("mass-scaling-relations.pdf", dpi=300)


# Join Sanders and Hekker
sanders = Table.read("../apogee_distances.csv")


fig, ax = plt.subplots()

sanders_pinnsonault = join(sanders, pinnsonault, keys=("APOGEE_ID", ))
mass_diff = sanders_pinnsonault["MASS_BaSTI"] - sanders_pinnsonault["M1"]
ax.scatter(sanders_pinnsonault["__M_H_2"], mass_diff, facecolor="#e67e22", s=50)


sanders_hekker = join(sanders, hekker, keys=("APOGEE_ID", ))
for i in range(1, 7):

    mass_diff = sanders_hekker["MASS_BaSTI"] - sanders_hekker["mass_{}".format(i)]
    ax.scatter(sanders_hekker["PARAM_M_H_2"], mass_diff, facecolor="#3498db", s=50)


sanders_epstein = join(sanders, epstein, keys=("APOGEE_ID", ))
mass_diff = sanders_epstein["MASS_BaSTI"] - sanders_epstein["SR_MASS"]
ax.scatter(
    sanders_epstein["__M_H_2"],
    mass_diff,
    facecolor="#27ae60", s=50)


ax.set_xlabel(r"$[{\rm Fe/H}]$")
ax.set_ylabel(r"$\Delta\mathcal{M}$ $[\mathcal{M}_\odot]$")

fig.savefig("mass-difference.pdf", dpi=300)


