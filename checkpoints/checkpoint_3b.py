# Checkpoint 3.2

"""
1. In Python, record the time before sampling starts.
2. Collect 100 ADC values (loop).
3. Record the time after sampling ends.
4. Compute average time between samples = (t_{end} - t_{start})/100.
5. Plot voltage vs. time using matplotlib.pyplot (or pylab).
6. Save plot as PDF.
"""

import spidev
import time
import pylab as pl

# =============================
# Read MCP3208 from given channel
# =============================
def read_adc(channel):
    if not (0 <= channel <= 7):
        raise ValueError("Channel must be 0-7")
    
    # Start bit, single-ended mode (start + SGL/DIF + D2)
    cmd = 0b00000110 | ((channel & 0x04) >> 2)
    msb = ((channel & 0x03) << 6)
    
    # Send three bytes and receive response
    response = spi.xfer2([cmd, msb, 0])
    
    # Convert response to 12-bit value
    result = ((response[1] & 0x0F) << 8) | response[2]
    return result

# =============================
# Setup SPI
# =============================
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI bus 0, device CE0
spi.max_speed_hz = 1000000  # 1 MHz

# =============================
# Sampling Configuration
# =============================
vref = 3.3              # Reference voltage
channel = 0             # ADC input channel
num_samples = 100       # Number of ADC readings

xvals = []              # Time (s)
yvals = []              # Voltage (V)

print("Starting sampling...")

start_time = time.time()
for i in range(num_samples):
    adc_val = read_adc(channel)
    voltage = adc_val * vref / 4095.0
    timestamp = time.time()
    xvals.append(timestamp)
    yvals.append(voltage)
end_time = time.time()

# Normalize time (relative to first sample)
time_zero = xvals[0]
xvals = [t - time_zero for t in xvals]

# Calculate time per sample
total_duration = end_time - start_time
avg_sample_interval = total_duration / num_samples

print(f"Total sampling time: {total_duration:.6f} s")
print(f"Average time per sample: {avg_sample_interval:.6f} s")

# =============================
# Plotting
# =============================
pl.figure(figsize=(8, 4))
pl.plot(xvals, yvals, 'bo-', markersize=4, label="ADC Samples")
pl.xlabel("Time (s)")
pl.ylabel("Voltage (V)")
pl.title("MCP3208 ADC Sampling of 10 Hz Sine Wave")
pl.grid(True)
pl.legend()

# Save to PDF
pl.savefig("adc_sampling_plot.pdf")
pl.show()

print("Plot saved as 'adc_sampling_plot.pdf'")