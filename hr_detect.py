import numpy as np
import matplotlib.pyplot as plt
from ecg_gudb_database import GUDb
import ecg_filter as ECGFilter

def DetectRPeaks(frequency, detect_range):
    R_peaks = []
    location = []
    for i in np.arange(1, len(frequency)-1):
        if frequency[i] > frequency[i-1] and frequency[i] > frequency[i+1]:
            max_flag = 1
            for j in range(1, detect_range):
                if frequency[i] < frequency[i-j]:
                    max_flag = 0
                    break
                if frequency[j] > frequency[i]/2:
                    max_flag = 0
                    break
            if max_flag == 1:
                R_peaks.append(frequency[i])
                location.append(i)
    return R_peaks, location

def CalculateMomentHeartRate(location, sample_rate):
    MomentHeartRate = []
    for i in range(len(location) - 1):
        interval = location[i+1] - location[i]
        time_interval = interval/sample_rate
        heartrate = int(60/time_interval)
        MomentHeartRate.append(heartrate)

    return MomentHeartRate

if __name__ == '__main__':
    data = np.loadtxt('shortecg.dat')
    # data = data - 2048
    # data = data * 2E-3 * 500 / 1000

    plt.plot(data)
    plt.title('Org ECG')
    plt.xlabel('time/sec')
    plt.show()

    fs = 1000.0
    detect_range = 200
    sample_rate = 250
    ntaps = 500

    f1 = int(45.0 / fs * ntaps)
    f2 = int(55.0 / fs * ntaps)
    f0 = int(5 / fs * ntaps)
    f_resp = np.ones(ntaps)
    f_resp[f1:f2 + 1] = 0
    f_resp[ntaps - f2:ntaps - f1 + 1] = 0
    f_resp[0:f0 + 1] = 0
    f_resp[ntaps - f0:ntaps] = 0
    coeff_tmp = np.fft.ifft(f_resp)
    coeff_tmp = np.real(coeff_tmp)
    coeff = np.zeros(ntaps)
    coeff[0:int(ntaps / 2)] = coeff_tmp[int(ntaps / 2):ntaps]
    coeff[int(ntaps / 2):ntaps] = coeff_tmp[0:int(ntaps / 2)]

    coeff2 = coeff * np.hamming(ntaps)

    y = ECGFilter.Filter_processing(data, coeff2)


    plt.plot(y)
    plt.title('Filtered ECG')
    plt.xlabel('time/sec')
    plt.show()

    # template = y[500:3000]
    #
    # plt.plot(template)
    # plt.show()
    #
    # fir_coeff = template[::-1]
    # plt.plot(fir_coeff)
    # plt.show()

    # det = ECGFilter.Filter_processing(data, fir_coeff)

    R_peaks, location = DetectRPeaks(y, detect_range)
    plt.title('Filtered ECG')
    plt.plot(y)
    plt.xlabel('time/sec')
    plt.scatter(location, R_peaks, color="red")
    plt.legend()
    plt.show()

    moment_heartrate = CalculateMomentHeartRate(location, sample_rate)
    print(moment_heartrate)

    # subject number to load, starting at 0, our Msc number is 11
    subject_number = 11
    # print experiments
    print("Experiments:", GUDb.experiments)
    # experiment to load
    experiment = 'walking'
    # creating class which loads the experiment
    ecg_class = GUDb(subject_number, experiment)

    # getting the raw ECG data numpy arrays from class
    chest_strap_V2_V1 = ecg_class.cs_V2_V1
    einthoven_i = ecg_class.einthoven_I
    einthoven_ii = ecg_class.einthoven_II
    einthoven_iii = ecg_class.einthoven_III

    # getting filtered ECG data numpy arrays from class
    ecg_class.filter_data()
    chest_strap_V2_V1_filt = ecg_class.cs_V2_V1_filt
    einthoven_i_filt = ecg_class.einthoven_I_filt
    einthoven_ii_filt = ecg_class.einthoven_II_filt
    einthoven_iii_filt = ecg_class.einthoven_III_filt

    filtered_ecg = y
    R_peaks, location = DetectRPeaks(filtered_ecg, detect_range)
    plt.plot(einthoven_iii_filt, label="Original ECG")
    plt.plot(filtered_ecg, label="Filtered ECG")
    plt.scatter(location, R_peaks, color="red")
    plt.xlabel('Time/ses')
    plt.legend()
    plt.show()

