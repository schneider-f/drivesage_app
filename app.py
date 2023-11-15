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
    # print("Input received:", input)
    # Overidding result to avoid multiple API calls billing
    #data, results = pipeline.run(input)
    data = {'addresses': ['1 Austin Terrace, Toronto, ON M5R 1X8, Canada', "King's College Cir, Toronto, ON, Canada", '8 Adelaide St W, Toronto, ON M5H 0A9, Canada', '1 Dundas St E, Toronto, ON M5B 2R8, Canada', '677 Bloor St W, Toronto, ON M6G 1L3, Canada', '186 Spadina Ave. Unit 1A, Toronto, ON M5T 3B2, Canada', '318 Wellington St W, Toronto, ON M5V 3T4, Canada', '30 Yonge St, Toronto, ON M5E 1X8, Canada', '789 Yonge St, Toronto, ON M4W 2G8, Canada', '45 Cecil St, ON M5T 1N1, Toronto, Canada', '620 Vaughan Rd, York, ON M6C 2R5, Toronto, Canada', '954 St Clair Ave W, Toronto, ON M6E 1A1, Toronto, Canada', '1720 Eglinton Ave W, York, ON M6E 2H5, Toronto, Canada', '2442 Dufferin St, York, ON M6E 3T1, Toronto, Canada', '2609 Eglinton Ave W, York, ON M6M 1T3, Toronto, Canada', '2679 Eglinton Ave W, York, ON M6M 1T8, Toronto, Canada', '1710 Jane St, York, ON M9N 2S4, Toronto, Canada'], 'depot': 0, 'num_vehicles': 2, 'datetime': (2023, 11, 16, 14, 0)}
    results = ["https://www.google.com/maps/dir/?api=1&origin=1%20Austin%20Terrace%2C%20Toronto%2C%20ON%20M5R%201X8%2C%20Canada&destination=1%20Austin%20Terrace%2C%20Toronto%2C%20ON%20M5R%201X8%2C%20Canada&waypoints=677%20Bloor%20St%20W%2C%20Toronto%2C%20ON%20M6G%201L3%2C%20Canada|954%20St%20Clair%20Ave%20W%2C%20Toronto%2C%20ON%20M6E%201A1%2C%20Toronto%2C%20Canada|2609%20Eglinton%20Ave%20W%2C%20York%2C%20ON%20M6M%201T3%2C%20Toronto%2C%20Canada|2679%20Eglinton%20Ave%20W%2C%20York%2C%20ON%20M6M%201T8%2C%20Toronto%2C%20Canada|1710%20Jane%20St%2C%20York%2C%20ON%20M9N%202S4%2C%20Toronto%2C%20Canada|2442%20Dufferin%20St%2C%20York%2C%20ON%20M6E%203T1%2C%20Toronto%2C%20Canada|1720%20Eglinton%20Ave%20W%2C%20York%2C%20ON%20M6E%202H5%2C%20Toronto%2C%20Canada|620%20Vaughan%20Rd%2C%20York%2C%20ON%20M6C%202R5%2C%20Toronto%2C%20Canada", "https://www.google.com/maps/dir/?api=1&origin=1%20Austin%20Terrace%2C%20Toronto%2C%20ON%20M5R%201X8%2C%20Canada&destination=1%20Austin%20Terrace%2C%20Toronto%2C%20ON%20M5R%201X8%2C%20Canada&waypoints=45%20Cecil%20St%2C%20ON%20M5T%201N1%2C%20Toronto%2C%20Canada|186%20Spadina%20Ave.%20Unit%201A%2C%20Toronto%2C%20ON%20M5T%203B2%2C%20Canada|318%20Wellington%20St%20W%2C%20Toronto%2C%20ON%20M5V%203T4%2C%20Canada|30%20Yonge%20St%2C%20Toronto%2C%20ON%20M5E%201X8%2C%20Canada|8%20Adelaide%20St%20W%2C%20Toronto%2C%20ON%20M5H%200A9%2C%20Canada|Toronto%20City%20Hall%2C%20100%20Queen%20St%20W%2C%20Toronto%2C%20ON%20M5H%202N3%2C%20Canada|1%20Dundas%20St%20E%2C%20Toronto%2C%20ON%20M5B%202R8%2C%20Canada|King%27s%20College%20Cir%2C%20Toronto%2C%20ON%2C%20Canada|789%20Yonge%20St%2C%20Toronto%2C%20ON%20M4W%202G8%2C%20Canada"]
    
    # Generate map 
    warehouse_address = data["addresses"][0]
    delivery_addresses = data["addresses"][1:]
    map_html = pipeline.generate_visualization_map(warehouse_address, delivery_addresses)

    # Pass the map HTML to the results template
    return render_template('results_page.html', results=results, map_html=map_html)

if __name__ == '__main__':
    print("Running the app.\n")
    app.run(debug=True, host='0.0.0.0', port=5000)