print("The app is starting.\n")

import pipeline

# Should be extracted from the frontend
input = """Starting at 1 Austin Terrace, Toronto, ON M5R 1X8, Canada, we have deliveries to make tomorrow afternoon at various locations.
            Here are the addresss:
            King's College Cir, Toronto, ON, Canada;
            8 Adelaide St W, Toronto, ON M5H 0A9, Canada;
            1 Dundas St E, Toronto, ON M5B 2R8, Canada.;
            677 Bloor St W, Toronto, ON M6G 1L3, Canada;
            186 Spadina Ave. Unit 1A, Toronto, ON M5T 3B2, Canada;
            318 Wellington St W, Toronto, ON M5V 3T4, Canada;
            30 Yonge St, Toronto, ON M5E 1X8, Canada;
            789 Yonge St, Toronto, ON M4W 2G8, Canada;
            Toronto City Hall, 100 Queen St W, Toronto, ON M5H 2N3, Canada;
            45 Cecil St, ON M5T 1N1, Toronto, Canada;
            620 Vaughan Rd, York, ON M6C 2R5, Toronto, Canada;
            954 St Clair Ave W, Toronto, ON M6E 1A1, Toronto, Canada;
            1720 Eglinton Ave W, York, ON M6E 2H5, Toronto, Canada;
            2442 Dufferin St, York, ON M6E 3T1, Toronto, Canada;
            2609 Eglinton Ave W, York, ON M6M 1T3, Toronto, Canada;
            2679 Eglinton Ave W, York, ON M6M 1T8, Toronto, Canada;
            1710 Jane St, York, ON M9N 2S4, Toronto, Canada;

            We only have two delivery trucks. Please assist us in organizing the route to minimize the total driving time.
            """

print("Running the pipeline.\n")
results = pipeline.run(input)
print(results)