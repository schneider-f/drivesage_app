import pipeline
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/submit', methods=['POST'])
def submit():
    input = request.form['prompttext']
    
    data, results = pipeline.run(input)
    
    #Generate map 
    warehouse_address = data["addresses"][0]
    delivery_addresses = data["addresses"][1:]
    routes = [d["route"] for d in results]
    map_html = pipeline.generate_visualization_map(warehouse_address, delivery_addresses, routes, data['addresses'])

    # Pass the map HTML to the results template
    return render_template('results_page.html', results=results, map_html=map_html)

if __name__ == '__main__':
    print("Running the app.\n")
    app.run(debug=True, host='0.0.0.0', port=5000)