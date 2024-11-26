from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    """
    Design a Butterworth band-pass filter.

    This function computes the coefficients for a Butterworth band-pass filter
    based on the specified low cut-off frequency, high cut-off frequency, 
    sampling frequency, and filter order.

    Parameters:
        lowcut (float): The lower cut-off frequency of the filter in Hz.
        highcut (float): The upper cut-off frequency of the filter in Hz.
        fs (float): The sampling frequency of the data in Hz.
        order (int, optional): The order of the filter (default is 5).

    Returns:
        Tuple: The filter coefficients (b, a) for the filter.
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Function to apply the band-pass filter
def bandpass_filter(data, lowcut, highcut, fs, order=5):
    """
    Apply a Butterworth band-pass filter to the input data.

    This function applies a band-pass filter to the provided data using
    the coefficients obtained from the butter_bandpass function.

    Parameters:
        data (np.ndarray): The input data to be filtered.
        lowcut (float): The lower cut-off frequency of the filter in Hz.
        highcut (float): The upper cut-off frequency of the filter in Hz.
        fs (float): The sampling frequency of the data in Hz.
        order (int, optional): The order of the filter (default is 5).

    Returns:
        np.ndarray: The filtered data after applying the band-pass filter.
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y