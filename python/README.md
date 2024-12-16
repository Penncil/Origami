
# Origami Plot Library

This library provides functions to create origami plots for visualizing multi-dimensional data. Origami plots are a unique way to represent multiple variables in a single, intuitive graphic.

## Features

- Create origami plots with customizable variables and ranges.
- Support for different color schemes, including colorblind-friendly options.
- Configurable figure size for different display needs.
- Grid lines and axis labels for better readability.

## Installation

To use the Origami Plot Library, clone the repository and import the module in your Python script or Jupyter notebook.

```bash
git clone https://github.com/galsapir/origami_plot.git
```

Then, you can import the necessary functions in your Python script or Jupyter notebook:

```python
from origami_plot import create_origami_plot, VariableConfig, ColorScheme
import pandas as pd
```

## Usage

1. **Prepare your data:** Ensure your data is in a Pandas Series.
2. **Define variable configurations:** Create a list of `VariableConfig` objects specifying the name, minimum, and maximum values for each variable.
3. **Create the plot:** Use the `create_origami_plot` function to generate the plot, specifying the data, variable configurations, color scheme, and other optional parameters.

For detailed usage examples, please refer to the provided Jupyter notebook in the repository.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.
