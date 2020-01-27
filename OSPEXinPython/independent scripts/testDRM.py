import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.modeling.models import custom_model

hdulist1 = fits.open("C:/Users/a_lesya007/Downloads/NEW/NEW/ResultFigures/Figures18112019/Scripts/hsi_spectrum_20020220_080000.fits" )
header11 = hdulist1[1].header
header13 = hdulist1[3].header
data11 = hdulist1[1].data
data12 = hdulist1[2].data
Rate = data11.RATE
Livetime = data11.LIVETIME
print('livetime', Livetime.shape)
Time = data11.TIME - 2
Time_del = data11.TIMEDEL
E_min = data12.E_MIN
E_max = data12.E_MAX
Area = header13[24]
E_mean = np.mean(E_min)
Accum_Time = np.sum(Time_del)
n = len(E_min)

deltaE = np.zeros(shape=(n))
for i in range(n):
    deltaE[i] = E_max[i] - E_min[i]

#Rate
CountRate = np.zeros(shape=(n))
for i in range(n):
    CountRate[i] = np.mean(Rate[:, i])

#Counts
Counts = np.zeros(shape=(n))
for i in range(n):
    Counts[i] = np.mean(Rate[:,i]*Accum_Time)

#Flux
Flux = np.zeros(shape=(n))
for i in range(n):
    Flux[i] = np.mean(Rate[:,i]) / (Area*deltaE[i]-2)

print('Flux: ', Flux.shape)

hdulist = fits.open("C:/Users/a_lesya007/PycharmProjects/thursday/hsi_srm_20020220_080000.fits" )
hdulist.info()

header1 = hdulist[1].header
header3 = hdulist[3].header
data1 = hdulist[1].data
data2 = hdulist[2].data
Energy_low = data1.ENERG_LO
#print('E_low: ', Energy_low)
# print("energy law shape: ", Energy_low.shape)
Energy_hi = data1.ENERG_HI
#print('E_high: ',Energy_hi)
n_grp = data1.N_GRP
#print('N_grp: ', n_grp)
f_chan = data1.F_CHAN
#print('F_chan: ', f_chan)
n_chan = data1.N_CHAN
#print('N_chan: ', n_chan)

matrix = data1.MATRIX
print('Matrix: ', matrix.shape)

edges = np.append(E_min,E_max[-1])

# the width of the channels
dE = np.diff(edges)

#Rate
PhotonRate = np.zeros(shape=(n))
for i in range(n):
    PhotonRate[i] = Rate[0, i]
dNc_dtdE = PhotonRate
# plt.plot(edges[:-1], dNc_dtdE, drawstyle = 'steps-post')
# plt.yscale('log')
# plt.xscale('log')
# plt.show()

PhotonCounts = np.zeros(shape=(n))
for i in range(n):
    PhotonCounts[i] = Rate[0, i]*Time_del[i]
dNc_dtdE2 = PhotonCounts/ dE
# plt.plot(edges[:-1], PhotonCounts, drawstyle = 'steps-post')
# plt.yscale('log')
# plt.xscale('log')
# plt.show()


PhotonFlux = np.zeros(shape=(n))
for i in range(n):
    PhotonFlux[i] = Rate[0, i]/(Area*deltaE[0]-2)
dNc_dtdE3 = PhotonFlux/ dE
# plt.plot(edges[:-1], dNc_dtdE3, drawstyle = 'steps-post')
# plt.yscale('log')
# plt.xscale('log')
# plt.show()


def power_law(energy, norm, index):

    return norm * np.power(energy/100.,index)

# for ease
def differential_flux(e):

    return power_law(e, .01, -2)

# integral of the differential flux
def integral(e1, e2):
    return (e2 - e1) / 6.0 * (differential_flux(e1) + 4 * differential_flux((e1 + e2) / 2.0)+ differential_flux(e2))

# true photon fluxes integrated over the photon bins of the response
true_fluxes = integral(Energy_low[:], Energy_hi[:])
#print(true_fluxes)
# dNp/(dt dA)
ed = np.append(Energy_low,Energy_hi[-1])
PhE = np.diff(ed)
fig, ax = plt.subplots()
PL = true_fluxes/PhE
# print('PL size: ', PL.shape)
# P = PL/np.transpose(matrix)
# plt.plot(edges[:-1],P,  drawstyle = 'steps-post')
# plt.yscale('log')
# plt.xscale('log')
# plt.show()
#
# ax.step(ed[:-1],PL,where='post')
# ax.set_xscale('log')
# ax.set_yscale('log')
# ax.set_xlabel('Photon Energy')
# ax.set_ylabel(r'$\frac{d N_p}{dt dA}$')
# folded_photons = np.dot(PL, np.diag(matrix))
# plt.plot(ed[:-1], folded_photons,  drawstyle = 'steps-post')
# # #plt.plot(edges[:-1], folded_counts, drawstyle = 'steps-post', label='modeled data')
# plt.yscale('log')
# plt.xscale('log')
# plt.show()
folded_counts = np.dot(true_fluxes, np.transpose(matrix).T)
# PhFlux = np.zeros(shape=(n))
# for i in range(n):
#     PhFlux[i] = np.sum(true_fluxes[:])
# print('PhFlux: ', PhFlux.shape)
PhFlux = np.resize(PL, len(E_min))
Photons = dNc_dtdE3*(PhFlux/folded_counts)
plt.plot(edges[:-1], Photons,  drawstyle = 'steps-post')
plt.plot(ed[:-1], PL, drawstyle = 'steps-post', label='modeled data')
plt.yscale('log')
plt.xscale('log')
plt.show()
#
plt.plot(edges[:-1], dNc_dtdE3, drawstyle = 'steps-post', label='real data')
plt.plot(edges[:-1], folded_counts, drawstyle = 'steps-post', label='modeled data')
plt.yscale('log')
plt.xscale('log')
plt.show()
#d = np.dot(dNc_dtdE3*true_fluxes)

# plt.plot(edges[:-1],folded_counts/dE, drawstyle = 'steps-post', label='modeled data')
# plt.plot(edges[:-1],PL[:77], drawstyle = 'steps-post', label='real data')
# plt.yscale('log')
# plt.xscale('log')
# plt.show()

