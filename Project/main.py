
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from pytesseract import Output
import csv
import random
from csv import writer
import os

# C:\Program Files\Tesseract-OCR
img = cv2.imread('data/letter1.jpg')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# create a function to extract text from image using pytesseract and put it into a txt file
def extract_text(img, invert):
    # convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = gray
    # apply a thrshold to get image with only b&w (binarization)
    ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # write the image into a temporary file
    cv2.imwrite("data/output/temp.png", img)
    # read the text from the image
    text = pytesseract.image_to_string(cv2.imread("data/output/temp.png"))
    # print the text
    print(text)
    # write the text into a txt file
    f = open("data/output/tester.txt", "w")
    f.close()
    return img


# Remove words-text.csv & words-boxs.csv
if os.path.exists("words-text.csv"):
    os.remove('words-text.csv')
if os.path.exists("words-boxs.csv"):
    os.remove('words-boxs.csv')

# Read in image
img1 = extract_text(img, False)

# Pytesseract
d = pytesseract.image_to_data(img1, output_type=Output.DICT)
text = pytesseract.image_to_string(img1)
words = text.split()
for i in range(len(words)):  ## make all the words into lower case for matching
    words[i] = words[i].lower()

# Creating words-text.csv ( Contains all words that are found)
k = 0
for j in words:
    tempList = list([words[k]])
    temptList = tempList
    k = k + 1
    with open('words-text.csv', 'a', newline='') as f_object:
        # Pass File object to Writer object
        writer_object = writer(f_object)
        # Append the List to next csv row
        writer_object.writerow(tempList)
        # Close the csv
        f_object.close()
    del tempList[:]

# Creating words-boxs.csv file ( Contains all Bounding Boxes )
n_boxes = len(d['level'])
for i in range(n_boxes):
    if d['text'][i] != "":
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        wList = list([x, y, w, h])
        with open('words-boxs.csv', 'a', newline='') as f_object:
            # Pass File object to Writer object
            writer_object = writer(f_object)
            # Append the List to next csv row
            writer_object.writerow(wList)
            # Close the csv
            f_object.close()
        del wList[:]

# Compare words-text.csv with bad-words-removed-blanks.csv to see if any words match
with open('data/bad.csv', 'r') as csv1, open('words-text.csv', 'r') as csv2:
    # Main = Bad Words Dataset
    # Temp = Dataset created from inputted image
    main = csv1.readlines()
    temp = csv2.readlines()

indexList = []
print('The matching words are:')
# Open the words-matched.csv File and write in any matched words
with open('words-matched.csv', 'w') as outFile:
    for line in temp:
        if line in main:
            outFile.write(line)
            print(''.join(line))
            line = line.replace("\n", "")
            index = words.index(line)
            words[index] = words[index].replace(line, line + ' ')  # needed for duplicates
            print(index)
            indexList.append(index)
print(indexList)

# Draw Rectangle on the bad words
with open('words-boxs.csv', 'r') as f:
    read = list(csv.reader(f))
    for i, value in enumerate(read):
        if i in indexList:
            (x, y, w, h) = (int(value[0]), int(value[1]), int(value[2]), int(value[3]))
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
            print(i, value)

cv2.imwrite("data/output/output.png", img)
cv2.imshow('censored.png', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
