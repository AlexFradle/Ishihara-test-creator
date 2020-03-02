# Ishihara-test-creator

## Dependencies
`python 3.6+`, `pygame`
 
## Instructions
* Open colourblind_gui.py and change Dots args to edit the pattern created
* Run colourblind_gui.py
## Example

Made using: `Dots(800, 10, 5, 3)`

![](dots_3.gif)


## Using Dots class
The image that is read from should look like:
![](read_img.bmp)

And should be:
* Uncompressed to ensure all pixels are a definite colour
* Anything to be output with different colour should be black `(0, 0, 0)`

When not using the gui:
* Specify the radius
* Specify graph function
* Specify radius
  * Needs to be image width / 2
```python
dots = Dots(2000, 7, 2, 1, lambda x1, y1: 350 < x1 + y1 < 1000)
```
