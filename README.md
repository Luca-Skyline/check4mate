# check4mate
In-Development computer vision and machine learning project, hopefully to be a "Chess Vision" chess analysis app for iOs and Android.

Roboflow Dataset I created, used for "Chess Vision" (identifying pieces). <br>
<a href="https://universe.roboflow.com/luca-dalcanto-lrlwg/chess-piece-detector-sv3nm"> <img src="https://app.roboflow.com/images/download-dataset-badge.svg"></img> </a> <br>
(images credit Daylen Yang under Open Data Commons Attribution License: http://opendatacommons.org/licenses/by/1.0/.).

Here's the Google Colab I'm using to train that CNN using YOLOv5: <br>
<a href="https://colab.research.google.com/drive/1VTXvUZuEtzxaH9c7gS56IFbabWYz_5A6#scrollTo=8t23YMrPsDKw"> <img src="https://colab.research.google.com/assets/colab-badge.svg"> </a> <br>

## Strategy:
- Run edge detection on the image and binarize it (convert every pixel into 2 values: 0 or 1, black or white)
- Run line detection to find straight edges
- Remove duplicates and find the 9 parallel lines most likely to be the vertical edges of the 8 columns. Repeat the process to find 9 parallel lines for the rows.
  - Lines within a close threshold should be averaged and deleted
  - Find the average distance between all parallel lines
  - Remove one of the 2 lines with the most extreme outward values (presumably there won't be stray lines inside the board, only on the oustide). Of the 2, remove the one that's average distance to its nearest "neighbor" is farthest from the average distance between all the lines. Recalculate the average (assuming we accurately predicted which line was more wrong, it will now be more accurate) and repeat this until we only have 9 left.
- For every combination of a horizontal and parallel line, find the 2D mean between its four points. This should get 81 points, all the corners of squares.
- Segment the each quadrilateral into its own image, perspective warped into a square.
- Run image classification to determine which piece the square most represents
- Ensure that the pieces identified match the fundemental rules of chess, and adjust predictions accordingly. For instance, if two white kings were detected, the one with the lower confidence should be assigned its second-highest prediction.
- Based on the original positions of each image, assemble a file representing the current position of the entire board.
- Assemble a UI display of the board, feed the file into a stockfish engine, or export it for use in  engines such as Chess.com or liChess!

## To-do:
- Piece image classification model
- Split chess board into squares and run that model on each one
- Incorporate stockfish so we can get a live analysis through the phone camera
- GUI/nav of app itself
- Export to chess.com, lichess, etc.
- Chess game note scanner using handwriting detection (and more edge/line detection 🫠)
- more to come...

## Resources:
Image dataset - [Daylen Yang](https://github.com/daylen/chess-id)

ML/CV model training and fitting - [Roboflow?](https://universe.roboflow.com/luca-dalcanto-lrlwg/chess-piece-detector-sv3nm)

Free, open source chess analysis engine - [Stockfish](https://github.com/official-stockfish/Stockfish)

Handwriting detection with python - [handprint](https://pypi.org/project/handprint/)

App UI Framework (compatible with both Android and iOS) - [kivy](https://github.com/kivy/kivy)

more to come!!!!
