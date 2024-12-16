import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Optional
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches

@dataclass
class VariableConfig:
    name: str
    min_value: float
    max_value: float

def create_radar_plot(df: pd.DataFrame, variable_configs: List[VariableConfig], 
                      title: str = "", figsize: Tuple[int, int] = (10, 10),
                      show_legend: bool = True, show_title: bool = True) -> None:
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection='polar'))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    n_variables = len(variable_configs)
    theta = np.linspace(0, 2 * np.pi, n_variables, endpoint=False)

    labels = [config.name for config in variable_configs]

    # Add the variable names as labels
    ax.set_xticks(theta)
    ax.set_xticklabels(labels, fontsize=24)

    # Move labels outward
    ax.tick_params(pad=18)

    # Generate colors for generated signals
    generated_colors = generate_colors(len(df) - 1)  # Generate one less color

    # Plot each data series
    for i, row in df.iterrows():
        values = []
        for config in variable_configs:
            value = row[config.name]
            normalized_value = (value - config.min_value) / (config.max_value - config.min_value)
            values.append(normalized_value)
        
        values = np.array(values)
        values = np.concatenate((values, [values[0]]))  # repeat first value to close the polygon

        if i == 0:
            label = 'Original Signal'
            color = 'black'
            alpha = 0.1  # You might want to adjust this for visibility
        else:
            label = f'Generated Signal {i}'
            color = generated_colors[i-1]  # Use generated colors for other signals
            alpha = 0.2

        ax.plot(np.concatenate((theta, [theta[0]])), values, color=color, linewidth=2, 
                label=label)
        ax.fill(np.concatenate((theta, [theta[0]])), values, color=color, alpha=alpha)
        
        # Add points at the nodes
        ax.scatter(theta, values[:-1], color=color, s=30, zorder=10)

    # Set the limits of the plot
    ax.set_ylim(0, 1)
    
    # Add concentric circles for the grid at 25% intervals
    ax.set_rgrids([0.25, 0.5, 0.75], angle=0, fontsize=20)
    ax.set_yticklabels([])

    # Add title if show_title is True
    if show_title:
        ax.set_title(title, pad=20)

    # Add legend if show_legend is True
    if show_legend:
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=24)
    
    # Adjust the outermost ring to match inner rings
    ax.spines['polar'].set_color('gray')  # Set color to match inner rings
    ax.spines['polar'].set_linewidth(0.5)  # Set line width to match inner rings
    ax.spines['polar'].set_alpha(0.2)  # Set transparency to match inner rings
    plt.tight_layout()
    plt.show()


def create_origami_plot(df: pd.DataFrame, variable_configs: List[VariableConfig], 
                        title: str = "", figsize: Tuple[int, int] = (10, 10),
                        show_legend: bool = True) -> None:
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, pad=20)

    n_variables = len(variable_configs)
    theta = np.linspace(0, 2 * np.pi, n_variables, endpoint=False)
    theta = np.roll(theta, -1)  # Ensure the first variable is at the top
    
    x_coordinates = np.cos(theta)
    y_coordinates = np.sin(theta)

    # Draw main axes
    for x, y, config in zip(x_coordinates, y_coordinates, variable_configs):
        ax.plot([0, x], [0, y], color='gray', alpha=0.3, linewidth=1, linestyle='-')
        # Add labels
        label_x, label_y = x * 1.2, y * 1.2
        ha = 'left' if x > 0 else 'right' if x < 0 else 'center'
        va = 'bottom' if y > 0 else 'top' if y < 0 else 'center'
        ax.text(label_x, label_y, config.name, ha=ha, va=va, fontsize=8)

    # Draw grid
    for i in range(1, 5):
        circle = plt.Circle((0, 0), i / 4, fill=False, linestyle=':', linewidth=0.5, color='black')
        ax.add_artist(circle)
        ax.text(-0.05, i / 4, f'{i / 4:.2f}', ha='right', va='center', color='gray')

    # Generate colors for each data series
    colors = generate_colors(len(df))

    # Plot each data series
    for i, row in df.iterrows():
        opacity = 1 if i == 0 else 0.5  # Full opacity for first series, half for others
        plot_data_series(ax, row, variable_configs, colors[i], opacity, x_coordinates, y_coordinates)

    # Add legend if show_legend is True
    if show_legend:
        legend_elements = [
            plt.Line2D([0], [0], color=colors[0], lw=2, label=f'Patient {df.iloc[0, 0]} (outline)')
        ]
        if len(df) > 1:
            legend_elements.extend([
                plt.Line2D([0], [0], color=colors[1], lw=2, alpha=0.5, label=f'Patient {df.iloc[1, 0]} (outline)')
            ])
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.3, 1))

    plt.tight_layout()
    plt.show()

def plot_data_series(ax, data, variable_configs, color, opacity, x_coordinates, y_coordinates):
    n_variables = len(variable_configs)
    
    max_values = np.array([config.max_value for config in variable_configs])
    min_values = np.array([config.min_value for config in variable_configs])
    data_values = np.array([data[config.name] for config in variable_configs])
    
    scale = (data_values - min_values) / (max_values - min_values)
    
    main_x = x_coordinates * scale
    main_y = y_coordinates * scale
    
    # Calculate auxiliary points
    aux_theta = np.linspace(0, 2 * np.pi, n_variables, endpoint=False) + (np.pi / n_variables)
    aux_theta = np.roll(aux_theta, -1)  # Ensure auxiliary points align with main points
    aux_x = np.cos(aux_theta) * 0.1
    aux_y = np.sin(aux_theta) * 0.1

    # Create a list of points for the polygon
    polygon_points = []
    for i in range(n_variables):
        polygon_points.append((main_x[i], main_y[i]))
        polygon_points.append((aux_x[i], aux_y[i]))
    
    # Create and add the polygon patch
    polygon = patches.Polygon(polygon_points, closed=True, fill=True, 
                              facecolor=color, edgecolor=color, 
                              alpha=opacity * 0.2)  # Adjust alpha for fill opacity
    ax.add_patch(polygon)

    # Draw lines and points
    for i in range(n_variables):
        next_i = (i + 1) % n_variables
        ax.plot([main_x[i], aux_x[i], main_x[next_i]], 
                [main_y[i], aux_y[i], main_y[next_i]], 
                color=color, alpha=opacity, linewidth=2)

    # Plot main points
    ax.scatter(main_x, main_y, color=color, alpha=opacity, s=30)
    
    # Plot auxiliary points
    ax.scatter(aux_x, aux_y, color=color, alpha=opacity * 0.5, s=15)

def generate_colors(n):
    # Create a custom colormap
    cmap = LinearSegmentedColormap.from_list("custom", ["#4B0082", "#9400D3", "#00CED1", "#20B2AA"])
    return [cmap(i) for i in np.linspace(0, 1, n)]