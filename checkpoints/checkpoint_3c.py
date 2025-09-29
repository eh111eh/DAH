# Checkpoint 3.4

"""
1. Reads 100 ADC samples while square wave is applied
2. Separates high vs low using midpoint threshold
3. Averages each set
4. Prompts you to enter oscilloscope high/low values
5. Repeats after you reduce the square wave amplitude
6. Plots a calibration curve (measured vs oscilloscope)
7. Saves plot as adc_calibration_plot.pdf
"""

import spidev
import time
import pylab as pl
import statistics

#==========================================================
# SPI ADC reader for MCP3208
#==========================================================
def read_adc(channel):
    if not 0 <= channel <= 7:
        raise ValueError("Channel must be between 0 and 7")
    
    # MCP3208 protocol
    cmd = 0b00000110 | ((channel & 0x04) >> 2)
    msb = ((channel & 0x03) << 6)
    response = spi.xfer2([cmd, msb, 0])
    result = ((response[1] & 0x0F) << 8) | response[2]
    return result

#==========================================================
# Setup SPI
#==========================================================
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

#==========================================================
# Function to take 100 samples and separate high/low
#==========================================================
def get_adc_high_low(channel, vref=3.3):
    samples = []
    for _ in range(100):
        adc_val = read_adc(channel)
        voltage = adc_val * vref / 4095.0
        samples.append(voltage)
        time.sleep(0.005)  # ~5 ms delay (200 Hz sampling rate)

    # Heuristic: use midpoint to separate high/low
    v_mid = (max(samples) + min(samples)) / 2
    high_vals = [v for v in samples if v > v_mid]
    low_vals  = [v for v in samples if v <= v_mid]

    avg_high = statistics.mean(high_vals) if high_vals else 0
    avg_low  = statistics.mean(low_vals) if low_vals else 0

    return avg_high, avg_low, samples

#==========================================================
# Collect calibration points
#==========================================================
print("=== Square Wave Calibration ===")
print("1. Connect FULL amplitude square wave to ADC input.")
input("Press Enter when ready to sample...")

full_high, full_low, _ = get_adc_high_low(channel=0)
print(f"ADC High Voltage (Full): {full_high:.3f} V")
print(f"ADC Low Voltage  (Full): {full_low:.3f} V")

v_high_full_scope = float(input("Enter Oscilloscope HIGH voltage (Full amp): "))
v_low_full_scope  = float(input("Enter Oscilloscope LOW voltage (Full amp): "))

print("\n2. Reduce the amplitude by approx 2x.")
input("Press Enter when ready to sample again...")

half_high, half_low, _ = get_adc_high_low(channel=0)
print(f"ADC High Voltage (Half): {half_high:.3f} V")
print(f"ADC Low Voltage  (Half): {half_low:.3f} V")

v_high_half_scope = float(input("Enter Oscilloscope HIGH voltage (Half amp): "))
v_low_half_scope  = float(input("Enter Oscilloscope LOW voltage (Half amp): "))

#==========================================================
# Prepare data for plotting
#==========================================================
oscilloscope_vals = [
    v_low_full_scope,
    v_high_full_scope,
    v_low_half_scope,
    v_high_half_scope
]

adc_measured_vals = [
    full_low,
    full_high,
    half_low,
    half_high
]

#==========================================================
# Plot Calibration Curve
#==========================================================
pl.figure(figsize=(6, 4))
pl.plot(oscilloscope_vals, adc_measured_vals, 'bo-')  # Blue dots + lines
pl.xlabel("Oscilloscope Voltage (V)")
pl.ylabel("ADC Measured Voltage (V)")
pl.title("ADC Calibration Plot (Square Wave)")
pl.grid(True)
pl.tight_layout()
pl.savefig("adc_calibration_plot.pdf")
pl.show()

print("Calibration plot saved as 'adc_calibration_plot.pdf'")
