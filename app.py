from flask import Flask, render_template_string
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# Load the Netflix data
netflix_data = pd.read_csv('/home/praveen/Documents/Webpage/netflix_titles.csv')

# Initialize the Flask application
app = Flask(__name__)

# Function to create plots
def create_plots():
    plots = []

    # Plot 1: Count of titles by type (Movie/TV Show)
    fig, ax = plt.subplots()
    sns.countplot(data=netflix_data, x='type', palette=['#E50914', '#221F1F'], ax=ax)
    ax.set_title('Count of Titles by Type')
    ax.set_xlabel('Type')
    ax.set_ylabel('Count')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.read()).decode('utf-8')
    plots.append(plot_data)
    plt.clf()

    # Plot 2: Count of titles by country
    fig, ax = plt.subplots(figsize=(12, 6))
    country_counts = netflix_data['country'].value_counts().head(10)
    sns.barplot(x=country_counts.values, y=country_counts.index, palette='Reds', ax=ax)
    ax.set_title('Top 10 Countries by Number of Titles')
    ax.set_xlabel('Count')
    ax.set_ylabel('Country')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.read()).decode('utf-8')
    plots.append(plot_data)
    plt.clf()

    # Plot 3: Distribution of release years
    fig, ax = plt.subplots()
    sns.histplot(netflix_data['release_year'], kde=True, color='#E50914', ax=ax)
    ax.set_title('Distribution of Release Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Count')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.read()).decode('utf-8')
    plots.append(plot_data)
    plt.clf()

    return plots

# Define a route for the default URL, which loads the data
@app.route('/')
def index():
    # Convert the dataframe to HTML with added styling
    table_html = netflix_data.to_html(classes='table table-striped table-dark table-bordered', index=False)

    # Create the plots and get the base64 strings
    plot_data_list = create_plots()

    # Render the plots and table on a webpage
    return render_template_string('''
        <!doctype html>
        <html>
            <head>
                <title>Netflix Titles</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                <style>
                    body {
                        background-color: #221F1F;
                        color: white;
                    }
                    .container {
                        margin-top: 30px;
                    }
                    h1, h2 {
                        color: #E50914;
                    }
                    .table-container {
                        margin-top: 30px;
                    }
                    .plot-container {
                        display: flex;
                        justify-content: space-around;
                        flex-wrap: wrap;
                    }
                    .plot-container img {
                        margin: 10px;
                        max-width: 30%;
                    }
                    .table th, .table td {
                        color: white;
                    }
                    .table-striped tbody tr:nth-of-type(odd) {
                        background-color: #2D2D2D;
                    }
                    .table-hover tbody tr:hover {
                        background-color: #3E3E3E;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Netflix Titles</h1>
                    <h2>Plots</h2>
                    <div class="plot-container">
                        {% for plot_data in plot_data_list %}
                        <img src="data:image/png;base64,{{ plot_data }}" alt="Plot">
                        {% endfor %}
                    </div>
                    <div class="table-container">
                        <h2>Netflix Data Table</h2>
                        {{ table_html|safe }}
                    </div>
                </div>
            </body>
        </html>
    ''', table_html=table_html, plot_data_list=plot_data_list)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
