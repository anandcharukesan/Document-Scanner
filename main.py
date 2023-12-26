import cv2
import imutils
from skimage.filters import threshold_local
from transform import perspective_transform
import os
import img2pdf
import tempfile

def delete_files_in_directory(directory):
    file_list = os.listdir(directory)
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")



    




def scanner(img, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Loading and displaying the original image
    original_img = cv2.imread(img)
    copy = original_img.copy()
    cv2.waitKey(0)

    ratio = original_img.shape[0] / 500.0
    img_resize = imutils.resize(original_img, height=500)
    # cv2.imshow('Resized image', img_resize)
    # cv2.waitKey(0)

    gray_image = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(0)

    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edged_img = cv2.Canny(blurred_image, 75, 200)
    cv2.waitKey(0)

    cnts, _ = cv2.findContours(edged_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    doc = None  # Initialize the 'doc' variable

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            doc = approx
            break
    
    if doc is None:
        # Handle the case where no valid document contour is found
        print("Your files are already scanned !")
        return
    
    p = []
    for d in doc:
        tuple_point = tuple(d[0])
        cv2.circle(img_resize, tuple_point, 3, (0, 0, 255), 4)
        p.append(tuple_point)
    cv2.waitKey(0)

    warped_image = perspective_transform(copy, doc.reshape(4, 2) * ratio)
    # warped_image = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)
    # cv2.waitKey(0)

    # T = threshold_local(warped_image, 11, offset=8, method="gaussian")
    # warped = (warped_image > T).astype("uint8") * 255
    
    
    
    # Save the image with a sequential name in the output directory
    image_count = len(os.listdir(output_directory))
    output_path = os.path.join(output_directory, f"scan_{image_count}.png")
    
    
    
    
    
    cv2.imwrite(output_path, warped_image)
    print("Saved scanned image:", output_path)

    # cv2.imshow("Final Scanned image", imutils.resize(warped_image, height=650))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    
    image_folder = output_directory
    output_pdf_path = "Output path/output.pdf" 
    
    image_paths = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # convert_images_to_pdf(image_paths, output_pdf_path)
    
def convert_images_to_pdf(image_paths, output_path):
    # Create a temporary directory to store the image files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Convert each image to a temporary file
        temp_files = []
        for image_path in image_paths:
            image = cv2.imread(image_path)
            if image is not None:
                temp_file = os.path.join(temp_dir, os.path.basename(image_path))
                cv2.imwrite(temp_file, image)
                temp_files.append(temp_file)

        # Check if any valid images were found
        if not temp_files:
            print("No valid images found in the specified folder.")
            return

        # Convert temporary files to a PDF
        with open(output_path, "wb") as pdf_file:
            pdf_file.write(img2pdf.convert(temp_files))
            
            
    

    
    


