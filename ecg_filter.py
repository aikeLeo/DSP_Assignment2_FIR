import numpy as np
import matplotlib.pyplot as plt

def Filter_processing(data, coefficient):
    from fir_filter import FIR_filter

    FIR_filter = FIR_filter(coefficient)
    after_filtering_ecg = []
    for i, v in enumerate(data):
        after_filtering_ecg.append(FIR_filter.dofilter(v))
    return after_filtering_ecg


if __name__ == '__main__':

    data = np.loadtxt('shortecg.dat')
    sample_rate = 250

    freq_time = np.arange(0, len(data)) * (1.0/sample_rate)
    freq_data = abs(np.fft.fft(data))
    freqs = np.fft.fftfreq(data.size, 1/sample_rate)

    plt.plot(freqs, freq_data)
    plt.show()

    ntaps = 500
    cutoff_freq = 5

    siginal = np.ones(ntaps)
    k1 = int((cutoff_freq - 5) / sample_rate * ntaps)
    k2 = int((cutoff_freq + 5) / sample_rate * ntaps)
    siginal[k1:k2] = 0
    siginal[ntaps - k2:ntaps - k1] = 0
    init_freq = np.fft.ifft(siginal)

    len = ntaps
    impulse_response = np.zeros(len)
    impulse_response[0:int(len/2)] = init_freq[int(len/2):len]
    impulse_response[int(len/2):len] = init_freq[0:int(len/2)]
    coefficient = impulse_response * np.hamming(ntaps)

    taps = np.linspace(0, sample_rate, ntaps)
    plt.plot(taps, siginal)
    plt.title("Filter signal")
    plt.show()

    plt.plot(init_freq)
    plt.title('freq_domain signal')
    plt.show()

    plt.plot(taps, coefficient)
    plt.title('signal with window')
    plt.show()

    after_filtering_ecg = Filter_processing(data, coefficient)
    after_filtering_ecg -= np.mean(after_filtering_ecg)

    plt.plot(freq_time, data, label="Original ECG")
    plt.xlabel('Time/ses')
    plt.legend()
    plt.show()
    plt.plot(freq_time, after_filtering_ecg, label="after filtering ECG")
    plt.xlabel('Time/ses')
    plt.legend()
    plt.show()

    # np.savetxt("shortECG.dat", after_filtering_ecg)