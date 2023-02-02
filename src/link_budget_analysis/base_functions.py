import numpy as np

c0 = 299792458 #m

def calculateDistance(lat1, lon1, alt1, lat2, lon2, alt2):
    R0 = 6373.0 #km radius of Earth
    eccentricity = 0.01671 #eccentricity of the Earth
    lat1 = np.radians(lat1) #deg(lat1) ---> radians(lat1)
    lon1 = np.radians(lon1) #deg(lon1) ---> radians(lon1)
    lat2 = np.radians(lat2) #deg(lat2) ---> radians(lat2)
    lon2 = np.radians(lon2) #deg(lon2) ---> radians(lon2)
    R_corrected = R0 * np.sqrt(1 - (eccentricity * np.sin(lat1)^2)) #the radius accounted for the Earth being ellipsoid aka "the fat earth"
    
    # next, the lattitudes and longitudes is being transferred from an lla coordinate (ellipsoid shape) to rectangular coordinate system in terms of x, y, z. 
    # so, basically R1_xyz = [x1, y1, z1] 
    # lat1, lon1, alt1 to x1, y1, z1
    x1 = (R_corrected + alt1) * np.cos(lat1) * np.cos(lon1)
    y1 = (R_corrected + alt1) * np.cos(lat1) * np.sin(lon1)
    z1 = R_corrected * ((1 - eccentricity ^ 2) + alt1) * np.sin(lat1)
    R1_xyz = [x1, y1, z1]
    # lat2, lon2, alt2 to x2, y2, z2
    x2 = (R_corrected + alt2) * np.cos(lat2) * np.cos(lon2)
    y2 = (R_corrected + alt2) * np.cos(lat2) * np.cos(lon2)
    z2 = R_corrected * ((1 - eccentricity ^ 2) + alt2) * np.sin(lat2)
    R2_xyz = [x2, y2, z2]

    # now calculate the distance
    n_hat = R1_xyz / np.linalg.norm(R1_xyz) # unit vector normal to xy plane
    d = R2_xyz - R1_xyz 
    n = np.dot(R1_xyz,R2_xyz)
    distance = np.linalg.norm(d) #horizontal distance (km)

    # now calculate look angle
    d_outofplane = np.dot(d, n)
    d_inplane = d - n_hat * d_outofplane
    lookAngle = np.arctan2((d_outofplane)/(d_inplane)) # if result is negative, the position of object 2 is below horizon

    # now calculate the horizontal distance using haversine formula
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    horizontalDistance = R0 * c

    return distance, lookAngle, horizontalDistance

def calculateEIRP (transmitPowerTx, antennaGainTx, lineLossTx, splitterLossTx):
    transmitPowerTxdB = 10 * np.log10(transmitPowerTx)
    totalLossesTx = lineLossTx + splitterLossTx
    EIRP = transmitPowerTxdB + antennaGainTx + totalLossesTx
    return EIRP


def calculateFSPL(slantRange, frequency):
    FSPL = - (20 * np.log10(slantRange * 1e3) + 20 * np.log10(frequency * 1e6) + 20 * np.log10(4 * np.pi / c0))
    return FSPL

def calculatePropagationLosses(frequency, angleRadians):
    #Propagation loss calculations are not accurate. Please verify the equations used in this function.
    specificAtmosphericAbsorptionOxygen = 0.001*(0.00719+6.09/((frequency*1e6/1000000000)**2+0.227)+4.81/((frequency*1e6/1000000000-57)**2+1.5))*(frequency*1e6/1000000000)** 2
    specificAtmosphericAbsorptionWater = 0.0001*(0.05+0.021*7.5+3.6/((frequency*1e6/1000000000-22.2) ** 2+8.5)+10.6/((frequency*1e6/1000000000-183.3) ** 2+9)+8.9/((frequency*1e6/1000000000-325.4) ** 2+26.3))*(frequency*1e6/1000000000)**2*7.5
    atmosphericAbsorptionLosses = -(specificAtmosphericAbsorptionOxygen + specificAtmosphericAbsorptionWater) * 3 * np.exp(-0.002/3) / np.sin(angleRadians)
    ionosphericLosses = - 2
    PropagationLosses = atmosphericAbsorptionLosses + ionosphericLosses
    return PropagationLosses

def calculatesignalAtGS(EIRP, FSPL, atmosphericLosses, polarizationLoss):
    calculatesignalAtGS = EIRP + FSPL + atmosphericLosses + polarizationLoss
    return calculatesignalAtGS

def calculateReflectorBeamwidth(antennaGain):
    antennaBeamwidth = 10 ** ((44.3 - antennaGain) / 20)
    return antennaBeamwidth
def calculateAntennaPointingLoss(pointingOffset, antennaBeamwidth):
    pointingOffset = pointingOffset
    antennaPointingLoss = - 12 * (pointingOffset / antennaBeamwidth) ** 2
    return antennaPointingLoss

def calculateSystemNoiseTemp(antennaTemp, waveguideGain, ambientTemp, LNATemp, receiverTemp, LNAGain):
    waveguideGainFactor = 10**(waveguideGain/10)
    LNAGainFactor = 10**(LNAGain/10)
    eqNoiseTempTowardsAntenna = (antennaTemp + (waveguideGainFactor - 1) * ambientTemp ) / waveguideGainFactor
    eqNoiseTempLookingForwardReceiver = LNATemp + (receiverTemp / LNAGainFactor)
    systemNoiseTemp = eqNoiseTempTowardsAntenna + eqNoiseTempLookingForwardReceiver
    return systemNoiseTemp

def noiseFigure2noiseTemp(noiseFig, ambientTemp):
    noiseTemp = ambientTemp * (10**(noiseFig/10) - 1)
    return noiseTemp

def calculateGT(antennaGainRx, antennaRadomeLossRx, waveguideGain, systemNoiseTemp):
    receiverGT = antennaGainRx + antennaRadomeLossRx + waveguideGain - 10 * np.log10(systemNoiseTemp)
    return receiverGT