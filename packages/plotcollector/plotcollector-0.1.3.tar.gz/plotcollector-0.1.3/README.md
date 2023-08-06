# Plotcollector

Plotcollector is a Python module that provides a simple GUI to collect all matplotlib figures into a single interactive window and save them in a PowerPoint Presentation or PDF file by the simple press of a button. 

plotcollector is most useful when dealing with many plots where the sheer amount of individual windows is unmanageable and yet interactivity is needed.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install plotcollector.

```bash
pip install plotcollector
```

## Usage
```python
import plotcollector as plc

#this goes after all figures have been created
#Note the rest of the script won't continue until the
#plotcollector window is closed
plc.view()
```
## Using the Spyder IDE

Running PyQt apps in spyder currently results in incorrect sys exit behaviour when the IPython Console Graphics Backend is not set as "Inline".
To make sure plotcollector operates correctly in spyder be sure to change the graphics backend as:
```
Tools -> Preferences --> IPython Console -> Graphics --> Graphics Backend as Inline
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT License]
