'''
Higher level functions for calling lower-level functions in submodules
'''
import numpy as np
from base_functions import calculateEIRP, calculateFSPL, calculatePropagationLosses, calculateAntennaPointingLoss, \
    calculateSystemNoiseTemp, calculateGT, noiseFigure2noiseTemp, calculatesignalAtGS, calculateReflectorBeamwidth, \
    calculateDistance

from link_budget_analysis.parse_cfg import (load_link_config_file)

cfg_default = load_link_config_file("default_configuration.yml")

### Design parameter ###
frequency = cfg_default["default_config"]["design_parameter"]["frequency"]
dataRate = cfg_default["default_config"]["design_parameter"]["dataRate"]
propagationPathLength = cfg_default["default_config"]["design_parameter"]["propagationPathLength"]
### Transmitter ###
transmitPower = cfg_default["default_config"]["transmitter_parameter"]["transmitPower"]
antennaGainTx =  cfg_default["default_config"]["transmitter_parameter"]["antennaGainTx"]
lineLossTx = cfg_default["default_config"]["transmitter_parameter"]["lineLossTx"]
splitterLossTx = cfg_default["default_config"]["transmitter_parameter"]["splitterLossTx"]
EIRP = calculateEIRP(transmitPower, antennaGainTx, lineLossTx, splitterLossTx)

### Propagation Path ###
FSPL = calculateFSPL(propagationPathLength, frequency)
atmosphericLosses = cfg_default["default_config"]["propagation_path_parameter"]["atmosphericLosses"]
polarizationLoss = cfg_default["default_config"]["propagation_path_parameter"]["polarizationLoss"]
signalLevelAtGroundStation = calculatesignalAtGS(EIRP, FSPL, atmosphericLosses, polarizationLoss)

### Receiver ###
antennaGainRx = cfg_default["default_config"]["receiver_parameter"]["antennaGainRx"]
antennaBeamwidthRx = calculateReflectorBeamwidth(antennaGainRx)  # degrees
pointingOffsetRx = cfg_default["default_config"]["receiver_parameter"]["pointingOffsetRx"]
antennaRadomeLossRx = cfg_default["default_config"]["receiver_parameter"]["antennaRadomeLossRx"]
lineLossRx = cfg_default["default_config"]["receiver_parameter"]["lineLossRx"]
antennaPointingLossRx = calculateAntennaPointingLoss(pointingOffsetRx, antennaBeamwidthRx)

### Noise ###
ambientTemp = cfg_default["default_config"]["receiver_parameter"]["ambientTemp"]
antennaTemp = cfg_default["default_config"]["receiver_parameter"]["antennaTemp"]
waveguideGain = cfg_default["default_config"]["receiver_parameter"]["waveguideGain"]
waveguideTemp = cfg_default["default_config"]["receiver_parameter"]["waveguideTemp"]
LNAGain = cfg_default["default_config"]["receiver_parameter"]["LNAGain"]
LNANoiseFig = cfg_default["default_config"]["receiver_parameter"]["LNANoiseFig"]
receiverNoiseFig = cfg_default["default_config"]["receiver_parameter"]["receiverNoiseFig"]

LNATemp = noiseFigure2noiseTemp(LNANoiseFig, ambientTemp)
receiverNoiseTemp = noiseFigure2noiseTemp(receiverNoiseFig, ambientTemp)
systemNoiseTemp = calculateSystemNoiseTemp(antennaTemp, waveguideGain, ambientTemp, LNATemp, receiverNoiseTemp, LNAGain)
receiverGT = 1 # unit = dB, min=-5, max=6 
    # (1.8m: 30dB <G/T> 6.0dB) (1.5m: 26dB <G/T> 3dB) (0.6m: 21dB <G/T> -0.5dB) [combination of JDA and quasonix]
    # if preceise calculation required, use following equation
    #receiverGT = calculateGT(antennaGainRx, antennaRadomeLossRx, waveguideGain, systemNoiseTemp)

### Eb/No Method ###
dataRate = dataRate * 1e06  # Mbps
implementationLoss = cfg_default["default_config"]["receiver_parameter"]["implementationLoss"]
combinerGain = cfg_default["default_config"]["receiver_parameter"]["combinerGain"]
systemSNo = signalLevelAtGroundStation + receiverGT + antennaPointingLossRx + 228.6
systemEbNo = systemSNo - 10 * np.log10(dataRate)
requiredEbNo = cfg_default["default_config"]["design_parameter"]["requiredEbNo"]
EbNoSystemLinkMargin = implementationLoss + systemEbNo - requiredEbNo + combinerGain


## Results

print("Transmitter EIRP at rocket:  {} dB".format(round(EIRP, 2)))
print("Free-space path loss:  {} dB".format(round(FSPL, 2)))
print("Signal Level at Ground Station:  {} dB".format(round(signalLevelAtGroundStation, 2)))
print("System Noise Temperature:    {} K".format(round(systemNoiseTemp, 2)))
print("Ground Station G/T:          {} dB".format(round(receiverGT, 2)))
print("Link margin (EbNo Method):   {} dB".format(round(EbNoSystemLinkMargin, 2)))
   
