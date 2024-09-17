import smbus2
import time

# Constants for TLA2024
DEVICE_BUS = 1
DEVICE_ADDR = 0x48  # I2C address of the TLA2024

# TLA2024 Register Addresses
REG_CONVERSION = 0x00
REG_CONFIG = 0x01

# Initialize I2C bus
bus = smbus2.SMBus(DEVICE_BUS)

# Configuration settings
# - PGA: ±4.096 V
# - Continuous conversion mode
# - Data rate: 1600 samples per second
# - Single-ended input on AIN0
# - No comparator
# Build the 16-bit configuration register value
config = 0x0000
config |= 0x0000  # OS[15] = 0 (No effect in continuous mode)
config |= 0x4000  # MUX[14:12] = 100 (AIN0 single-ended)
config |= 0x0200  # DR[7:5] = 100 (1600 SPS)
config |= 0x0000  # MODE[8] = 0 (Continuous conversion)
config |= 0x0100  # PGA[11:9] = 001 (FSR ±4.096V)
config |= 0x0003  # COMP_MODE[4] to COMP_QUE[0] = 00011 (Comparator disabled)

# Swap bytes because SMBus uses big endian format
config_swapped = ((config & 0xFF) << 8) | (config >> 8)

# Write configuration to the CONFIG register
bus.write_word_data(DEVICE_ADDR, REG_CONFIG, config_swapped)

# Reference voltage (depends on PGA setting)
V_REF = 4.096

print("Starting ADC reading. Press Ctrl+C to stop.")

try:
    while True:
        # Read data from the Conversion register
        data = bus.read_i2c_block_data(DEVICE_ADDR, REG_CONVERSION, 2)
        # Combine the two bytes and shift to get the 12-bit result
        raw_adc = (data[0] << 8) | data[1]
        
        # Convert to 12-bit signed integer (two's complement)
        if raw_adc > 0x7FFF:
            raw_adc -= 0x10000

        # The TLA2024 outputs 16 bits, but only 12 bits are significant
        # Shift right by 4 bits to get the actual 12-bit value
        adc_value = raw_adc >> 4

        # Calculate voltage from ADC value
        voltage = (adc_value * V_REF) / (2**12 - 1)

        print(f"ADC Value: {adc_value}, Voltage: {voltage:.4f} V")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nADC reading stopped.")
finally:
    bus.close()
