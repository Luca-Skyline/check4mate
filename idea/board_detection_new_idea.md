# New and Improved Design for Board Detection: Recursion and Assumption

After some initial imperfection to detect every line on the board without accidentally using other lines, here is my new and improved strategy.

## Some things we can assume to be true:
- Lines that are "correct" will be almost exactly parallel or perpendicular to other lines that are "correct".
- Lines that are "correct" and psuedo-parallel will be spaced out equally (by distance X) or by exact whole multiples of X.
  - (X * 8), the size of the board, should be a significant percentage of the screen in both directions.
- The math for line detection may occasionally miss a border between checkered squares (from the Gaussian blur, canny image)
  - There will be some lines of the board missing
  - under the assumption the setting is turned up high enough to ignore smaller extraneous lines in the background and on pieces
- There will be extraneous lines, even some (such as the edge of a mat) that are parallel but have the wrong spacing
  
Strategy:
1. Select a line that hasn't been selected yet
2. Iterate through all other lines, selecting those that have a slope within a certain threshold of parallel and perpendicular (in two different lists)
3. Iterate through all sets of two parallel lines, looking for a common theme of an X value (distance between lines) that repeats within a certain threshold.
4. For the lines that are showing consistint accuracy to X (and multiples of X) from the lines around it, mark it as "accurate".
5. Ensure that the number of "accurate" parallel lines is at least at a certain threshold (probably 5 or 6 out of the 9 possible)
6. Remove the lines that are not "accurate"
7. Repeat 3-6 for the perpendiclar lines
8. Add implied lines that might be missing based on X spacing.
  - If there are 8 lines that are "accurate" and evenly spaced, we must decide which side to add the 9th line on... (I'll figure something out)
9. Ensure that the lines take up a significant amount of the screen 
10. Identitify an accuracy and size of our array
More to come!
