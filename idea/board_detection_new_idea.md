# New and Improved Design for Board Detection: Recursion and Implication

After some initial struggle to detect every line on the board without accidentally using other lines, here is my new and improved strategy.

## Some things we can assume to be true:
- Lines that are "correct" will be almost exactly parallel or perpendicular to other lines that are "correct".
- Lines that are "correct" and psuedo-parallel will be spaced out equally (by distance X) or by exact whole multiples of X.
  - (X * 8), the size of the board, should be a significant percentage of the screen in both directions.
- The math for line detection may occasionally miss a border between checkered squares (from the Gaussian blur, canny image)
  - There will be some lines of the board missing
  - under the assumption the setting is turned up high enough to ignore smaller extraneous lines in the background and on pieces
- There will be extraneous lines, even some (such as the edge of a mat) that are parallel but have the wrong spacing
  
