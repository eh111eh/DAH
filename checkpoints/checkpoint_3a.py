# Checkpoint 3.1

"""
- Reads from MCP3208.
- Samples data for 1 second at ~100 Hz.
- Plots the samples.
- Overlays a theoretical 10 Hz sine wave for comparison.

Requirements: spidev, pylab, and MCP3208 circuit connected properly to SPI on the Pi.

This code is based on https://github.com/bwynneHEP/DAH/blob/master/CodeExamples/3-ExampleListCode.py
"""

# Checkpoint 3.1 (Fixed for MCP3208)

"""
- Reads from MCP3208.
- Samples data for 1 second at ~100 Hz.
- Plots the samples.
- Overlays a theoretical 10 Hz sine wave for comparison.

Requirements: spidev, pylab, and MCP3208 circuit connected properly to SPI on the Pi.
"""

import spidev
import time
import pylab as pl
import math

# ================================
# Function to read MCP3208 channel
# ================================
def read_adc(channel):
    if not (0 <= channel <= 7):
        raise ValueError("Channel must be 0–7")

    # MCP3208 command format:
    # Start bit (1), Single/Diff (1), D2, D1, D0, then 4 dummy bits
    start_bit = 0x06  # 00000110 (start + single-ended)
    command = start_bit | ((channel & 0x04) >> 2)
    msb = (channel & 0x03) << 6

    # Perform SPI transaction
    adc = spi.xfer2([command, msb, 0x00])

    # Assemble 12-bit result
    result = ((adc[1] & 0x0F) << 8) | adc[2]
    return result

# ================================
# Init SPI
# ================================
spi = spidev.SpiDev()
spi.open(0, 0)           # Open bus 0, device 0 (CE0)
spi.max_speed_hz = 1000000  # Try lowering if unstable, e.g. 50000

# ================================
# Sampling Parameters
# ================================
channel = 0              # ADC channel to read
vref = 3.3               # Reference voltage
duration = 1.0           # Sampling duration in seconds
sample_rate = 100        # Hz
num_samples = int(duration * sample_rate)

xvals = []               # Time values
yvals = []               # ADC readings converted to voltage

start_time = time.time()
for i in range(num_samples):
    adc_val = read_adc(channel)
    voltage = adc_val * vref / 4095.0  # 12-bit resolution
    current_time = time.time() - start_time
    xvals.append(current_time)
    yvals.append(voltage)
    time.sleep(1.0 / sample_rate)

# ================================
# Generate Theoretical 10 Hz Sine Wave
# ================================
ytheory = []
for t in xvals:
    # Sine wave from 0 to 3.3V, centered at 1.65V
    y = 1.65 + 1.65 * math.sin(2 * math.pi * 10 * t)
    ytheory.append(y)

# ================================
# Plotting
# ================================
pl.plot(xvals, yvals, 'yo', label='Measured (ADC)', markersize=5)
pl.plot(xvals, ytheory, 'r-', label='Theoretical Sine', linewidth=1)
pl.xlabel('Time (s)')
pl.ylabel('Voltage (V)')
pl.title('MCP3208 ADC Sampling of 10 Hz Sine Wave')
pl.grid(True)
pl.legend()
pl.show()

# ==============
# Import required libraries
import time
import matplotlib.pyplot as plt
from collections import deque
from DAH import MCP3208

def main():
    # Define ADC as SPI chip 0 (CE0/GPIO8)
    ADC0 = MCP3208(chip=0)

    # ADC input channel
    channel = 0  # Change to your connected channel

    # Prepare plotting
    plt.ion()  # Interactive mode ON
    fig, ax = plt.subplots()
    window_size = 200  # Number of points to display
    voltages = deque([0]*window_size, maxlen=window_size)
    times = deque([0]*window_size, maxlen=window_size)
    line, = ax.plot(times, voltages, label="ADC Voltage (V)")
    ax.set_ylim(0, 3.3)  # ADC voltage range
    ax.set_xlabel("Sample")
    ax.set_ylabel("Voltage (V)")
    ax.set_title(f"Real-time ADC readings (Channel {channel})")
    ax.legend()

    print("Reading ADC and plotting... Press Ctrl+C to stop.")

    try:
        sample_count = 0
        while True:
            # Read voltage from ADC
            voltage = ADC0.analogReadVolt(channel)
            voltages.append(voltage)
            times.append(sample_count)
            sample_count += 1

            # Update plot
            line.set_ydata(voltages)
            line.set_xdata(times)
            ax.set_xlim(max(0, sample_count-window_size), sample_count)
            fig.canvas.draw()
            fig.canvas.flush_events()

            time.sleep(0.01)  # Adjust for faster/slower updates

    except KeyboardInterrupt:
        print("\nStopped by user.")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    main()
