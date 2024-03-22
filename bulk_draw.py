import cv2
import os

def draw_bounding_box_lines(image_path, output_path):
    isResized = False
    font_scale = 0.5
    font_thickness = 2
    # Load the image
    image = cv2.imread(image_path)
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
            # Update the bounding box coordinates after border addition
            x += border_width
            y += border_height
            isResized = True

        # Draw the left line with an arrow at the top
        cv2.arrowedLine(image, (x - 50, y + h), (x - 50, y), (0, 255, 0), 2, tipLength=0.05)
        cv2.putText(image, '10 cm', (x - 60, int((y + h + y) / 2)), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), font_thickness)
        cv2.circle(image, (x - 50, y + h), 5, (0, 255, 0), -1)

        # Draw the bottom line with an arrow at the right
        cv2.arrowedLine(image, (x, y + h + 50), (x + w, y + h + 50), (0, 255, 0), 2, tipLength=0.05)
        cv2.putText(image, '10 cm', (int((x + (x + w)) / 2), y + h + 60), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), font_thickness)
        cv2.circle(image, (x, y + h + 50), 5, (0, 255, 0), -1)

    # Save the result
    cv2.imwrite(output_path, image)
    return isResized

def is_close_to_edge(x, y, w, h, image_width, image_height):
    third_w, third_h = w // 3, h // 3
    return x < third_w or y < third_h or (image_width - (x + w)) < third_w or (image_height - (y + h)) < third_h

def process_images(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            draw_bounding_box_lines(input_path, output_path)

# Returns length & height arrow start/end points, isResized boolean value,
# and link to image (resized or original) for each image path as arg. Send
# 
def return_image_data(output_path):
    pass


# Process all images in 'mens_shoes' and save to 'output'
process_images('test', 'output')