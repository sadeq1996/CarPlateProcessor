import cv2
import pytesseract

# Load image
img = cv2.imread(r"plate8.jpg")

#* pytessract
pytesseract.pytesseract.tesseract_cmd =\
                                      r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Convert to grayscale

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply a Gaussian blur with a kernel size of 5
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection with a lower threshold of 50 and an upper threshold of 150
edges = cv2.Canny(blur, 50, 150)

# Find contours in the image
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw the contours on the original image
cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

resized_img = cv2.resize(img, (200, 200))
# Iterate through contours and filter for rectangular shapes
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
    if len(approx) == 4:
        #calculate x, y , w, h
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w)/h
        if aspect_ratio >= 1.5 and aspect_ratio <= 4.0:
            # Draw bounding box around plate
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            # Extract plate image and apply OCR
            # plate_img = img[y:y+h, x:x+w]
            # plate_text = pytesseract.image_to_string(plate_img, config='--psm 11')
            # # Print recognized plate text
            # print(plate_text)
            
#*++++++++++++++++++++++++++++crop image
largest_contour = None
max_area = 0
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.04*cv2.arcLength(contour, True), True)
    if len(approx) == 4 and cv2.contourArea(contour) > max_area:
        largest_contour = approx
        max_area = cv2.contourArea(contour)
        
x, y, w, h = cv2.boundingRect(largest_contour)

plate = img[y:y+h, x:x+w]


            
#*-----------------------------------
config = r"C:\Program Files\Tesseract-OCR\tessdata"


text = pytesseract.image_to_string(plate,lang="eng", config=config)

print(text)

with open(r"result.txt", "w", encoding="utf-8") as f:
    f.write(text)

# Show image with bounding boxes around plates
cv2.imshow('Car Plates', plate)
cv2.waitKey(0)
cv2.destroyAllWindows()
#==============
