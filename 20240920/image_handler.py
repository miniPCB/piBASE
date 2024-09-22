from PIL import Image, ImageTk

def load_and_resize_image(image_path, max_width, max_height):
    """Load an image and resize it to fit within the max width and height."""
    try:
        img = Image.open(image_path)
        img.thumbnail((max_width, max_height))  # Resize while maintaining aspect ratio
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Failed to load image: {e}")
        return None
