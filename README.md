# DeweyDecimalGenerator
Takes in the name of a book and generates the Dewey Decimal Classification(DDC) code needed by the Library of the book

# File structure
-`DDC.pickle` and `imageread.py` - The DDC data is avaiable as a scanned book only. This image needs to be converted to text.
For this task, `Tesseract`, an OCR library was used. `imageread.py` contains the code to do this. The images are too large
to be hosted here, however, they can easily be obtained online. `DDC.pickle` contains the output of this, which is a list of
book name and the book's code

-`classifier_binary` and `classifier_multi` - Contain prototyping code for making a simple text classifier using `NLTK`

-`book_classifier.py` - Can work in training or inference mode. -In training mode, it reads `DDC.pickle` and builds the
multiple levels of NaiveBayesClassifiers needed for generating the DDC Code and saves to disk. See `Explanation.MD` for
details on how it works. Training can take an hour. n inferenceing mode, it reads the saved classifiers and outputs the 
code

-`Explanation.MD`- Contains a summary of this work and how the system is designed
