import pipeline
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route('/')
def index():
    # Check if the Home.html file exists
    # template_path = os.path.join(os.getcwd(), 'html', 'Home.html')
    # if os.path.exists(template_path):
    #     print("Template file exists:", template_path)
    # template_path = './html/Home.html'
    # if os.path.exists(template_path):
    #     print("Template file exists:", template_path)
    return render_template('Home.html')

@app.route('/submit', methods=['POST'])
def submit():
    input = request.form['prompttext']
    print("Input received:", input)
    # Overidding result to avoid multiple API calls billing
    # results = pipeline.run(input)
    results = ["https://www.google.com/maps/dir/?api=1&origin=1%20Austin%20Terrace%2C%20Toronto%2C%20ON%20M5R%201X8%2C%20Canada&destination=1%20Austin%20Terrace%2C%20Toronto%2C%20ON%20M5R%201X8%2C%20Canada&waypoints=677%20Bloor%20St%20W%2C%20Toronto%2C%20ON%20M6G%201L3%2C%20Canada|954%20St%20Clair%20Ave%20W%2C%20Toronto%2C%20ON%20M6E%201A1%2C%20Toronto%2C%20Canada|2609%20Eglinton%20Ave%20W%2C%20York%2C%20ON%20M6M%201T3%2C%20Toronto%2C%20Canada|2679%20Eglinton%20Ave%20W%2C%20York%2C%20ON%20M6M%201T8%2C%20Toronto%2C%20Canada|1710%20Jane%20St%2C%20York%2C%20ON%20M9N%202S4%2C%20Toronto%2C%20Canada|2442%20Dufferin%20St%2C%20York%2C%20ON%20M6E%203T1%2C%20Toronto%2C%20Canada|1720%20Eglinton%20Ave%20W%2C%20York%2C%20ON%20M6E%202H5%2C%20Toronto%2C%20Canada|620%20Vaughan%20Rd%2C%20York%2C%20ON%20M6C%202R5%2C%20Toronto%2C%20Canada", "https://www.google.com/maps/dir/?api=1&origin=1%20Austin%20Terrace%2C%20Toronto%2C%20ON%20M5R%201X8%2C%20Canada&destination=1%20Austin%20Terrace%2C%20Toronto%2C%20ON%20M5R%201X8%2C%20Canada&waypoints=45%20Cecil%20St%2C%20ON%20M5T%201N1%2C%20Toronto%2C%20Canada|186%20Spadina%20Ave.%20Unit%201A%2C%20Toronto%2C%20ON%20M5T%203B2%2C%20Canada|318%20Wellington%20St%20W%2C%20Toronto%2C%20ON%20M5V%203T4%2C%20Canada|30%20Yonge%20St%2C%20Toronto%2C%20ON%20M5E%201X8%2C%20Canada|8%20Adelaide%20St%20W%2C%20Toronto%2C%20ON%20M5H%200A9%2C%20Canada|Toronto%20City%20Hall%2C%20100%20Queen%20St%20W%2C%20Toronto%2C%20ON%20M5H%202N3%2C%20Canada|1%20Dundas%20St%20E%2C%20Toronto%2C%20ON%20M5B%202R8%2C%20Canada|King%27s%20College%20Cir%2C%20Toronto%2C%20ON%2C%20Canada|789%20Yonge%20St%2C%20Toronto%2C%20ON%20M4W%202G8%2C%20Canada"]

    # Return some response if needed
    return jsonify({'status': 'success', 'result': results})


if __name__ == '__main__':
    print("Running the app.\n")
    app.run(debug=True, host='0.0.0.0', port=5000)