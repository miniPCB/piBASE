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

# Reference voltage (depends on PGA setting)
V_REF = 4.096  # Reference voltage based on PGA setting ±4.096V

# Function to read a single channel
def read_channel(channel):
    # Configuration settings
    # Start with OS bit [15] set to 1 to start a single conversion
    config = 0x8000

    # MUX bits [14:12]: Set to the desired channel
    if channel == 0:
        config |= 0x4000  # MUX[14:12] = 100 (AIN0)
    elif channel == 1:
        config |= 0x5000  # MUX[14:12] = 101 (AIN1)
    elif channel == 2:
        config |= 0x6000  # MUX[14:12] = 110 (AIN2)
    elif channel == 3:
        config |= 0x7000  # MUX[14:12] = 111 (AIN3)
    else:
        raise ValueError("Invalid channel: must be 0-3")

    config |= 0x0200  # PGA[11:9] = 001 (FSR ±4.096V)
    config |= 0x0100  # MODE[8] = 1 (Single-shot mode)
    config |= 0x0080  # DR[7:5] = 100 (1600 SPS)
    config |= 0x0003  # Comparator disabled

    # Swap bytes because SMBus uses little endian, but TLA2024 uses big endian
    config_swapped = ((config >> 8) & 0xFF) | ((config & 0xFF) << 8)

    # Debug: Print the configuration being written
    print(f"Writing config to channel {channel}: 0x{config:04X}")

    # Write configuration to the CONFIG register
    bus.write_word_data(DEVICE_ADDR, REG_CONFIG, config_swapped)

    # Wait for conversion to complete
    conversion_time = 1.0 / 1600 + 0.001  # Add a small delay to ensure completion
    time.sleep(conversion_time)

    # Read data from the Conversion register
    raw_data = bus.read_word_data(DEVICE_ADDR, REG_CONVERSION)
    # Swap bytes to match the TLA2024's big-endian format
    raw_data_swapped = ((raw_data << 8) & 0xFF00) | (raw_data >> 8)

    # Debug: Print the raw data read from the ADC
    print(f"Raw ADC Data (Channel {channel}): 0x{raw_data_swapped:04X}")

    # The TLA2024 outputs 16 bits, but only 12 bits are significant
    # The data is left-justified; shift right by 4 bits
    adc_code = raw_data_swapped >> 4

    # Convert to signed 12-bit integer (two's complement)
    if adc_code & 0x800:
        adc_code -= 1 << 12

    # Calculate voltage from ADC code
    voltage = (adc_code * V_REF) / (1 << 11)  # (1 << 11) = 2048

    return voltage


print("Starting ADC readings from all channels with debug. Press Ctrl+C to stop.")

try:
    while True:
        # Read voltages from all four channels
        voltages = []
        for ch in range(4):
            voltage = read_channel(ch)
            voltages.append(voltage)
        # Display the readings
        print(f"CH1: {voltages[0]:.4f} V, CH2: {voltages[1]:.4f} V, CH3: {voltages[2]:.4f} V, CH4: {voltages[3]:.4f} V")
        time.sleep(1)  # Increase delay to observe debug output
except KeyboardInterrupt:
    print("\nADC reading stopped.")
finally:
    bus.close()
