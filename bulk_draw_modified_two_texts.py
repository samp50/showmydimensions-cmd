
import cv2
import os

def calculate_font_scale(image, target_point_size):
    # Assuming 300 DPI for the image, which is a common print resolution
    dpi = 300

    # Convert point size to pixels. 1 point = 1/72 inches
    point_size_in_pixels = (target_point_size / 72) * dpi

    # Use the height of the image to calculate the scale
    image_height = image.shape[0]
    font_scale = point_size_in_pixels / image_height

    return font_scale

def draw_bounding_box_lines(image_path, output_path):
    target_point_size = 22  # Desired text point size

    # Load the image
    image = cv2.imread(image_path)

    # Calculate font scale based on the image and target point size
    font_scale = calculate_font_scale(image, target_point_size)
    font_thickness = 2

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to get a binary image
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Get the largest contour, assuming it is the object
        cnt = max(contours, key=cv2.contourArea)

        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(cnt)

        # Check if the bounding box is close to the edge
        if is_close_to_edge(x, y, w, h, image.shape[1], image.shape[0]):
            border_width = w // 3
            border_height = h // 3
            image = cv2.copyMakeBorder(image, border_height, border_height, border_width, border_width, cv2.BORDER_CONSTANT, value=[255, 255, 255])

        # Draw the bounding box
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Put text 1
        cv2.putText(image, 'Object', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), font_thickness)
        
        # Put text 2 (example)
        cv2.putText(image, 'Another Text', (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), font_thickness)

    # Save the image
    cv2.imwrite(output_path, image)

def is_close_to_edge(x, y, w, h, image_width, image_height, threshold=10):
    return x < threshold or y < threshold or (x + w) > (image_width - threshold) or (y + h) > (image_height - threshold)

# Example usage
draw_bounding_box_lines('test/lamp.jpg', 'output_image.jpg')