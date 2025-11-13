# Matplotlib Examples (Python)

Publication-quality static plots using Matplotlib.

## Installation

```bash
pip install matplotlib numpy pandas
```

## Basic Line Chart

```python
import matplotlib.pyplot as plt
import numpy as np

def create_line_chart():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    actual = [4000, 3000, 5000, 4500, 6000, 5500]
    target = [3500, 3500, 4000, 4000, 4500, 4500]

    plt.figure(figsize=(10, 6))

    # Plot lines
    plt.plot(months, actual, marker='o', linewidth=2, color='#3B82F6', label='Actual Sales')
    plt.plot(months, target, marker='s', linewidth=2, linestyle='--', color='#10B981', label='Target')

    # Formatting
    plt.title('Monthly Sales Trend (Jan-Jun 2024)', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Sales ($)', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)

    # Add value labels
    for i, (m, a) in enumerate(zip(months, actual)):
        plt.text(i, a + 200, f'${a:,}', ha='center', fontsize=9)

    plt.tight_layout()
    return plt

# Usage
plt = create_line_chart()
plt.show()
# plt.savefig('sales-trend.png', dpi=300, bbox_inches='tight')
```

---

## Bar Chart

```python
import matplotlib.pyplot as plt
import numpy as np

def create_bar_chart():
    categories = ['Electronics', 'Clothing', 'Home', 'Sports', 'Books']
    revenue = [45000, 38000, 52000, 29000, 21000]
    expenses = [28000, 22000, 31000, 18000, 12000]

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))

    # Create grouped bars
    bars1 = ax.bar(x - width/2, revenue, width, label='Revenue', color='#3B82F6')
    bars2 = ax.bar(x + width/2, expenses, width, label='Expenses', color='#EF4444')

    # Formatting
    ax.set_title('Revenue and Expenses by Category', fontsize=16, fontweight='bold')
    ax.set_xlabel('Category', fontsize=12)
    ax.set_ylabel('Amount ($)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    def autolabel(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'${height/1000:.0f}K',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=9)

    autolabel(bars1)
    autolabel(bars2)

    plt.tight_layout()
    return plt

plt = create_bar_chart()
plt.show()
```

---

## Scatter Plot with Colorblind-Safe Colors

```python
import matplotlib.pyplot as plt
import numpy as np

# IBM Colorblind-Safe Palette
IBM_COLORS = ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000']

def create_scatter_multigroup():
    np.random.seed(42)

    fig, ax = plt.subplots(figsize=(10, 8))

    groups = ['Group A', 'Group B', 'Group C']
    for i, group in enumerate(groups):
        x = np.random.randn(50) * 10 + i * 20
        y = np.random.randn(50) * 10 + i * 15

        ax.scatter(x, y, c=IBM_COLORS[i], label=group, s=80, alpha=0.7, edgecolors='white', linewidth=0.5)

    ax.set_title('Multi-Group Scatter Plot', fontsize=16, fontweight='bold')
    ax.set_xlabel('Variable X', fontsize=12)
    ax.set_ylabel('Variable Y', fontsize=12)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return plt

plt = create_scatter_multigroup()
plt.show()
```

---

## Histogram

```python
import matplotlib.pyplot as plt
import numpy as np

def create_histogram():
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)  # Mean=100, std=15, n=1000

    plt.figure(figsize=(10, 6))

    plt.hist(data, bins=30, color='#3B82F6', alpha=0.7, edgecolor='white', linewidth=0.5)

    plt.title('Distribution of Values', fontsize=16, fontweight='bold')
    plt.xlabel('Value', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(axis='y', alpha=0.3)

    # Add mean line
    mean_val = np.mean(data)
    plt.axvline(mean_val, color='#EF4444', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.1f}')
    plt.legend()

    plt.tight_layout()
    return plt

plt = create_histogram()
plt.show()
```

---

## Box Plot

```python
import matplotlib.pyplot as plt
import numpy as np

def create_box_plot():
    np.random.seed(42)

    data = [
        np.random.normal(100, 10, 100),  # Group A
        np.random.normal(90, 15, 100),   # Group B
        np.random.normal(110, 12, 100),  # Group C
        np.random.normal(95, 8, 100),    # Group D
    ]

    labels = ['Group A', 'Group B', 'Group C', 'Group D']

    fig, ax = plt.subplots(figsize=(10, 6))

    bp = ax.boxplot(data, labels=labels, patch_artist=True, notch=True)

    # Color boxes with colorblind-safe palette
    colors = ['#648FFF', '#785EF0', '#DC267F', '#FE6100']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_title('Distribution Comparison Across Groups', fontsize=16, fontweight='bold')
    ax.set_ylabel('Value', fontsize=12)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return plt

plt = create_box_plot()
plt.show()
```

---

## Saving Publication-Quality Figures

```python
# High-resolution for publications
fig.savefig('figure.png', dpi=300, bbox_inches='tight')

# Vector format for scaling
fig.savefig('figure.pdf', bbox_inches='tight')
fig.savefig('figure.svg', bbox_inches='tight')

# Transparent background
fig.savefig('figure.png', dpi=300, bbox_inches='tight', transparent=True)
```

---

**For Seaborn statistical visualizations, see `seaborn-examples.md`**
