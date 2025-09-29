# Checkpoint 3.1

"""
- Reads from MCP3208.
- Samples data for 1 second at ~100 Hz.
- Plots the samples.
- Overlays a theoretical 10 Hz sine wave for comparison.

Requirements: spidev, pylab, and MCP3208 circuit connected properly to SPI on the Pi.

This code is based on https://github.com/bwynneHEP/DAH/blob/master/CodeExamples/3-ExampleListCode.py
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
        return -1

    # MCP3208 uses a 3-byte SPI transfer
    cmd = 0b00000110 | ((channel & 0x04) >> 2)
    msb = ((channel & 0x03) << 6)
    adc = spi.xfer2([cmd, msb, 0])
    result = ((adc[1] & 0x0F) << 8) | adc[2]
    return result

# ================================
# Init SPI
# ================================
spi = spidev.SpiDev()
spi.open(0, 0)           # Open bus 0, device 0 (CE0)
spi.max_speed_hz = 1000000

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
    voltage = adc_val * vref / 4095.0
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
