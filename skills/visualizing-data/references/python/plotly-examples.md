# Plotly Python Examples

Complete examples for data visualization using Plotly in Python.

## Installation

```bash
pip install plotly pandas
```

## Bar Chart

```python
import plotly.graph_objects as go
import plotly.express as px

# Using Plotly Express (simpler)
def create_bar_chart_simple():
    data = {
        'Category': ['Product A', 'Product B', 'Product C', 'Product D'],
        'Revenue': [4000, 3000, 2000, 2780],
        'Expenses': [2400, 1398, 9800, 3908]
    }

    fig = px.bar(
        data,
        x='Category',
        y=['Revenue', 'Expenses'],
        title='Revenue vs Expenses by Product',
        barmode='group',
        color_discrete_sequence=['#3B82F6', '#EF4444']  # Blue, Red
    )

    fig.update_layout(
        xaxis_title='Product Category',
        yaxis_title='Amount ($)',
        legend_title='Metric',
        hovermode='x unified'
    )

    return fig

# Using Graph Objects (more control)
def create_bar_chart_advanced():
    categories = ['Product A', 'Product B', 'Product C', 'Product D']
    revenue = [4000, 3000, 2000, 2780]
    expenses = [2400, 1398, 9800, 3908]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Revenue',
        x=categories,
        y=revenue,
        marker_color='#3B82F6',
        text=revenue,
        textposition='outside'
    ))

    fig.add_trace(go.Bar(
        name='Expenses',
        x=categories,
        y=expenses,
        marker_color='#EF4444',
        text=expenses,
        textposition='outside'
    ))

    fig.update_layout(
        title='Revenue vs Expenses by Product',
        xaxis_title='Product Category',
        yaxis_title='Amount ($)',
        barmode='group',
        hovermode='x unified'
    )

    return fig

# Usage
fig = create_bar_chart_simple()
fig.show()  # Interactive HTML
# fig.write_html('chart.html')  # Save to file
# fig.write_image('chart.png')  # Requires kaleido: pip install kaleido
```

---

## Line Chart

```python
import plotly.graph_objects as go
import pandas as pd

def create_line_chart():
    # Sample data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    actual_sales = [4000, 3000, 5000, 4500, 6000, 5500]
    target_sales = [3500, 3500, 4000, 4000, 4500, 4500]

    fig = go.Figure()

    # Actual sales line
    fig.add_trace(go.Scatter(
        x=months,
        y=actual_sales,
        mode='lines+markers',
        name='Actual Sales',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=8, color='#3B82F6')
    ))

    # Target line
    fig.add_trace(go.Scatter(
        x=months,
        y=target_sales,
        mode='lines+markers',
        name='Target',
        line=dict(color='#10B981', width=2, dash='dash'),
        marker=dict(size=6, color='#10B981')
    ))

    fig.update_layout(
        title='Monthly Sales Trends (Jan-Jun 2024)',
        xaxis_title='Month',
        yaxis_title='Sales ($)',
        hovermode='x unified',
        template='plotly_white'
    )

    return fig

fig = create_line_chart()
fig.show()
```

---

## Scatter Plot

```python
import plotly.express as px

def create_scatter_plot():
    data = {
        'marketing_spend': [100, 120, 170, 140, 150, 180, 160, 190, 200, 210],
        'revenue': [200, 100, 300, 250, 400, 350, 380, 420, 450, 480],
        'product': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    }

    fig = px.scatter(
        data,
        x='marketing_spend',
        y='revenue',
        text='product',
        title='Marketing Spend vs Revenue',
        color_discrete_sequence=['#3B82F6'],
        trendline='ols'  # Add trend line
    )

    fig.update_traces(
        textposition='top center',
        marker=dict(size=12, opacity=0.7)
    )

    fig.update_layout(
        xaxis_title='Marketing Spend ($K)',
        yaxis_title='Revenue ($K)',
        hovermode='closest'
    )

    return fig

fig = create_scatter_plot()
fig.show()
```

---

## Pie Chart

```python
import plotly.graph_objects as go

def create_pie_chart():
    labels = ['Desktop', 'Mobile', 'Tablet']
    values = [400, 300, 200]
    colors = ['#3B82F6', '#10B981', '#F59E0B']  # Blue, Green, Orange

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value} users<br>%{percent}<extra></extra>'
    )])

    fig.update_layout(
        title='Device Distribution',
        showlegend=True
    )

    return fig

fig = create_pie_chart()
fig.show()
```

---

## Violin Plot

```python
import plotly.graph_objects as go
import numpy as np

def create_violin_plot():
    # Generate sample data for different groups
    np.random.seed(42)

    groups = ['Group A', 'Group B', 'Group C', 'Group D']
    fig = go.Figure()

    for group in groups:
        fig.add_trace(go.Violin(
            y=np.random.randn(100) * 10 + 50,
            name=group,
            box_visible=True,
            meanline_visible=True,
            fillcolor='#3B82F6',
            opacity=0.6
        ))

    fig.update_layout(
        title='Distribution Comparison Across Groups',
        yaxis_title='Value',
        xaxis_title='Group',
        violinmode='group'
    )

    return fig

fig = create_violin_plot()
fig.show()
```

---

## Heatmap

```python
import plotly.graph_objects as go
import numpy as np

def create_heatmap():
    # Sample correlation matrix
    variables = ['Price', 'Sales', 'Marketing', 'Reviews', 'Quality']
    correlation_matrix = np.random.rand(5, 5)
    correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2  # Make symmetric
    np.fill_diagonal(correlation_matrix, 1)  # Diagonal = 1

    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=variables,
        y=variables,
        colorscale='RdBu',
        zmid=0,
        text=np.round(correlation_matrix, 2),
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(title='Correlation')
    ))

    fig.update_layout(
        title='Variable Correlation Matrix',
        xaxis_title='Variable',
        yaxis_title='Variable'
    )

    return fig

fig = create_heatmap()
fig.show()
```

---

## 3D Surface Plot

```python
import plotly.graph_objects as go
import numpy as np

def create_surface_plot():
    # Generate sample 3D data
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    fig = go.Figure(data=[go.Surface(
        x=x,
        y=y,
        z=Z,
        colorscale='Viridis'
    )])

    fig.update_layout(
        title='3D Surface Plot: z = sin(√(x² + y²))',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        width=700,
        height=700
    )

    return fig

fig = create_surface_plot()
fig.show()
```

---

## Accessibility in Plotly (Python)

```python
import plotly.graph_objects as go

def create_accessible_chart():
    data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
        'Sales': [4000, 3000, 5000, 4500]
    }

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=data['Month'],
        y=data['Sales'],
        marker_color='#3B82F6',
        text=data['Sales'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title='Monthly Sales 2024',
        xaxis_title='Month',
        yaxis_title='Sales ($)',

        # Accessibility improvements
        font=dict(size=14),  # Readable text
        hovermode='x unified',

        # Add description for screen readers
        # Note: Plotly HTML output can include aria-label via custom HTML wrapper
    )

    return fig

# When saving to HTML, wrap with accessibility attributes
def save_accessible_html(fig, filename='chart.html'):
    html_string = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Accessible Chart</title>
    </head>
    <body>
        <figure role="img" aria-label="Monthly sales from January to April 2024. Sales ranged from $3K to $5K, with peak in March.">
            <figcaption style="font-size: 18px; font-weight: bold; margin-bottom: 16px;">
                Monthly Sales Trend
            </figcaption>
            {fig.to_html(include_plotlyjs='cdn', div_id='chart')}

            <!-- Data table alternative -->
            <details style="margin-top: 16px;">
                <summary style="cursor: pointer; font-weight: 500;">View as Data Table</summary>
                <table style="margin-top: 8px; border-collapse: collapse;">
                    <caption>Monthly Sales Data</caption>
                    <thead>
                        <tr style="background-color: #F3F4F6;">
                            <th style="padding: 12px; border: 1px solid #D1D5DB;">Month</th>
                            <th style="padding: 12px; border: 1px solid #D1D5DB;">Sales ($)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td style="padding: 12px; border: 1px solid #D1D5DB;">Jan</td><td style="padding: 12px; border: 1px solid #D1D5DB;">$4,000</td></tr>
                        <tr><td style="padding: 12px; border: 1px solid #D1D5DB;">Feb</td><td style="padding: 12px; border: 1px solid #D1D5DB;">$3,000</td></tr>
                        <tr><td style="padding: 12px; border: 1px solid #D1D5DB;">Mar</td><td style="padding: 12px; border: 1px solid #D1D5DB;">$5,000</td></tr>
                        <tr><td style="padding: 12px; border: 1px solid #D1D5DB;">Apr</td><td style="padding: 12px; border: 1px solid #D1D5DB;">$4,500</td></tr>
                    </tbody>
                </table>
            </details>
        </figure>
    </body>
    </html>
    '''

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_string)

fig = create_accessible_chart()
save_accessible_html(fig, 'accessible-chart.html')
```

---

## Colorblind-Safe Colors in Plotly

```python
import plotly.graph_objects as go

# IBM colorblind-safe palette
IBM_COLORBLIND_SAFE = ['#648FFF', '#785EF0', '#DC267F', '#FE6100', '#FFB000']

# Paul Tol palette
PAUL_TOL = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB']

def create_colorblind_safe_chart(data, palette=IBM_COLORBLIND_SAFE):
    fig = go.Figure()

    for i, (category, values) in enumerate(data.items()):
        fig.add_trace(go.Scatter(
            x=values['x'],
            y=values['y'],
            mode='lines+markers',
            name=category,
            line=dict(color=palette[i % len(palette)], width=2),
            marker=dict(size=8, color=palette[i % len(palette)])
        ))

    return fig
```

---

**For Matplotlib examples, see `matplotlib-examples.md`**
**For Seaborn statistical plots, see `seaborn-examples.md`**
