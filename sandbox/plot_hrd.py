

"""
Plot H-R diagram in a nice way.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from astropy.table import Table
from matplotlib.colors import LogNorm, PowerNorm
from matplotlib.ticker import MaxNLocator

RAVE_TGAS_FILE = "/data/gaia-eso/arc/tgas/tgas-rave.fits"


data = Table.read(RAVE_TGAS_FILE)

# Calculate absolute magnitude
data["gaia_abs_G"] = data["phot_g_mean_mag"] - 5 * np.log10(1000./data["parallax"]) + 5

Nbins = 75
xlims = (8000, 3000)
ylims = (8, -4)

cmap = "cool"


snr = 10
alpha = 0.1
parallax_error_fractions = (1, 2, 3, 4, 5, 7.5, 10, 12.5, 15, 17.5, 20)

data.sort("FE_H")

for i, parallax_error_fraction in enumerate(parallax_error_fractions):


    OK  = data["QC"] \
        * (data["parallax"] > 0) \
        * (data["FE_H"] < 0.15) \
        * (data["SNR"] > snr) \
        * ((data["parallax_error"]/data["parallax"]) <= (parallax_error_fraction/100.)) \
        * np.isfinite(data["FE_H"])


    fig, ax = plt.subplots(2, figsize=(5.1, 8.85))
    ax[0].text(0.09, 0.92, r"$<{:.1f}\%$ ${{\rm and}}$ ${{\rm S/N}} > {:.0f}$".format(parallax_error_fraction, snr),
        transform=ax[0].transAxes, horizontalalignment="left")
    ax[0].text(0.10, 0.84, r"${:.0f}$ ${{\rm stars}}$".format(sum(OK)),
        transform=ax[0].transAxes)
    


    scat = ax[0].scatter(
        data["TEFF"][OK], data["gaia_abs_G"][OK], c=data["FE_H"][OK],
        vmin=-0.5, 
        vmax=0.15, cmap=cmap, alpha=alpha, edgecolor="none", s=50)


    ax[0].set_xlim(xlims)
    ax[0].set_ylim(ylims)

    ax[1].hist2d(data["TEFF"][OK], data["gaia_abs_G"][OK],
        bins=(np.linspace(min(xlims), max(xlims), Nbins), np.linspace(min(ylims), max(ylims), Nbins)),
        norm=LogNorm(), cmap="Greys")

    ax[1].set_xlim(xlims)
    ax[1].set_ylim(ylims)

    for ax_ in ax:
        ax_.xaxis.set_major_locator(MaxNLocator(6))
        ax_.yaxis.set_major_locator(MaxNLocator(6))
        
    ax[0].set_xticklabels([])

    ax[1].set_xlabel(r"${\rm Effective}$ ${\rm temperature}$ $(RAVE$-$on),$  $T_{\rm eff}$ $[{\rm K}]$")
    ax[1].set_ylabel(r"${\rm Absolute}$ ${\rm Gaia}$ ${\rm magnitude},$ $G$ $[{\rm mags}]$")
    ax[0].set_ylabel(r"${\rm Absolute}$ ${\rm Gaia}$ ${\rm magnitude},$ $G$ $[{\rm mags}]$")

    fig.tight_layout()

    fig.savefig("screen-{}.png".format(len(parallax_error_fractions) - i), dpi=150)


os.system("convert -delay 50 -loop 10000 screen-*.png output.gif")

