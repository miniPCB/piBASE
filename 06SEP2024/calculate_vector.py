import math

def calculate_flux_field(sensor1, sensor2, sensor3, sensor4):
    """
    Calculate the 2D flux field vector (Fx, Fy) from four orthogonal sensor readings.
    
    Args:
    sensor1 (float): Reading from the sensor aligned with +X axis.
    sensor2 (float): Reading from the sensor aligned with +Y axis.
    sensor3 (float): Reading from the sensor aligned with -X axis.
    sensor4 (float): Reading from the sensor aligned with -Y axis.
    
    Returns:
    tuple: A tuple representing the flux field vector (Fx, Fy).
    """
    
    # Calculate the X and Y components of the flux field
    Fx = (sensor1 - sensor3) / 2
    Fy = (sensor2 - sensor4) / 2
    
    # Calculate the magnitude of the flux field
    magnitude = math.sqrt(Fx**2 + Fy**2)
    
    # Calculate the direction (angle) of the flux field in radians
    angle = math.atan2(Fy, Fx)
    
    return Fx, Fy, magnitude, angle

# Example sensor readings
sensor1 = 5.0  # +X direction
sensor2 = 3.0  # +Y direction
sensor3 = 1.0  # -X direction
sensor4 = 2.0  # -Y direction

# Calculate the flux field
Fx, Fy, magnitude, angle = calculate_flux_field(sensor1, sensor2, sensor3, sensor4)

print(f"Flux field vector: Fx = {Fx}, Fy = {Fy}")
print(f"Flux field magnitude: {magnitude}")
print(f"Flux field angle (radians): {angle}")
print(f"Flux field angle (degrees): {math.degrees(angle)}")
