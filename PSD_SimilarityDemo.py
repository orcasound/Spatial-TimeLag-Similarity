import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, correlate, correlation_lags

'''
  Demonstration of using cross power lags to find similarity between spectrograms
  by determining the time shifts needed to try to match PSD's between two spectrograms
'''
####################################################################

def insertSignal(i1, i2, amp, psd):
    for i in range(i1,i2):
        psd[i] += amp  # makes a 'signsl' between indices i1 and i2 in a psd already filled with random values ranging 0 -> 1

def calcCorrAry(psdAry1, psdAry2):
    Nf = psdAry1.shape[0]
    Nt = psdAry1.shape[1]
    corrAry = np.zeros([Nf, 2*Nt-1])
    lagList = np.zeros([2*Nt-1])
    maxCorrList = np.zeros([2*Nt-1])
    for i in range(Nf):
        psd1 = psdAry1[i,:]
        psd2 = psdAry2[i,:]
        correlation = correlate(psd1, psd2, mode="full")
        lags = correlation_lags(psd1.size, psd2.size, mode="full")
        maxCorrList[i] = np.max(correlation)
        predictedLag = lags[np.argmax(correlation)]
        if i >= 100 and i <= 105:
            plt.plot(lags, correlation)
            plt.title("i = {}, amp = {:0.2f} predicted Lag {}".format(i, np.max(psd1), predictedLag))
            plt.show()
        lagList[i] = predictedLag
        corrAry[i,:] = correlation
    return corrAry, lagList, maxCorrList

def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x - mean) / 4 / stddev)**2)

###################################################################
np.random.seed(0)  # set seed so random number generator repeast for each run

Nt = 256

i1 = Nt//2
i2 = i1 + 50
lag = 40
amp = 1

# 1-D correlation example, finding the lag between two signals
#  Create two psd arrays, one shifted by 'lag' bins in the time axis of a spectrogram
psd1 = np.random.rand(Nt)
insertSignal(i1, i2, amp, psd1)

psd2 = np.random.rand(Nt)
insertSignal(i1-lag, i2-lag, amp, psd2)   # Here the same 'signal' is input with a specified lag

plt.plot(psd1)
plt.plot(psd2)
plt.title("amp is {:0.2f}  lag is {}".format(amp, lag))
plt.show()

correlation = correlate(psd1, psd2, mode="full")
lags = correlation_lags(psd1.size, psd2.size, mode="full")
lagCorr = lags[np.argmax(correlation)]
predictedLag = lags[np.argmax(correlation)]
print("Lag of highest correlation {}  Highest correlation {:0.2f}  Index of highest correlation {}  Predicted lag {}".\
      format(lagCorr, np.max(correlation), np.argmax(correlation), predictedLag))

plt.plot(lags, correlation)
plt.title("predicted lag at max correlation = {:0.2f}, actual lag {:0.2f}".format(predictedLag, lag))
plt.show()

#  2-D correlation matrix

Nf = 256
psdAry1 = np.random.rand(Nt, Nf)
psdAry2 = np.random.rand(Nt, Nf)
for i in range(Nf):
    psd = np.random.rand(Nt)
    thisAmp = 2*amp*np.random.rand()
    insertSignal(lag + 25+i//3, lag + 25+i//3+25, thisAmp, psd)
    psdAry1[i,:] = psd
    psd = np.random.rand(Nt)
    insertSignal(25+i//3, 25+i//3+25, thisAmp, psd)
    psdAry2[i,:] = psd

fig, axs = plt.subplots(2)
fig.suptitle("amp is random up to {} and lag is {}".format(amp, lag))
axs[0].imshow(psdAry1)
axs[1].imshow(psdAry2)
plt.show()

corrAry, lagList, maxCorrList   = calcCorrAry(psdAry1, psdAry2)
plt.scatter(lagList, maxCorrList)
plt.title("Lags vs Maximum Correlation for each PSD band\nActual Lag {}".format(lag))
plt.xlabel("Optimum Lag between PSDs at each PSD level")
plt.ylabel("Maximum Correlation for each PSD pair")
plt.show()
# lagHist, bin_edges = np.histogram(lagList, bins = 50)
# plt.plot(bin_edges[:-1], lagHist)
# plt.show()
# peaks, properties = find_peaks(lagHist, height=np.max(lagHist) / 20, width=1)
# plt.scatter(lagList, maxCorrList)
# plt.title("Max Corr at each psd band vs predicted lag")
# plt.show()
#
# lagList, maxCorrList = zip(*sorted(zip(lagList,maxCorrList)))
# plt.plot(lagList)
# plt.show()
# plt.plot(maxCorrList)
# plt.show()
#
#
#
# x = lagList[400:]
# y = maxCorrList[400:]
# plt.hist(x, bins=25, density=False)
# plt.show()
# plt.plot(x,y)
# plt.show()
# popt, parms = optimize.curve_fit(gaussian, x, y)
# plt.plot(x, y)
# # plt.plot(x, gaussian(x, *popt))
#
#
# plt.hist(lagList, bins=25, density=False)
# plt.title("Lags histogram")
# plt.show()
# plt.hist(maxCorrList, bins=25, density=False)
# plt.title("Max correlation histogram")
# plt.show()
#
# corrAryThreshold = corrAry
# for i in range(Nf):
#     if maxCorrList[i] < 100:
#         corrAryThreshold[i,:] = 0
#
# plt.imshow(corrAryThreshold[:,250:350], aspect='auto')
# plt.title("This shows where 'good' correlations are found vs frequency\n Not Very Illuminating")
# plt.show()
#
#
