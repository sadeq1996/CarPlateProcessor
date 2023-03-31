import cv2
import pytesseract

# Load image
img = cv2.imread(r"1.jfif")

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
b=cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

resized_img = cv2.resize(img, (200, 200))
cv2.imshow('Car Plates', resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#==============
