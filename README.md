# VALR Lending Rates

This Python script periodically fetches loan rate data from the VALR API and uploads it to an InfluxDB instance for storage and analysis. Key features include:

API Integration:

Fetches loan rate data using a GET request to the VALR API, signed with HMAC SHA-512 for authentication.
Focuses specifically on ZAR (South African Rand) loan rates.
Data Processing:

Converts annualized interest rates (previousFundingRate, estimatedNextRate, estimatedNextBorrowRate) to percentage values.
InfluxDB Storage:

Writes processed loan rate data to an InfluxDB database using the InfluxDBClient.
Scheduled Execution:

Uses the schedule library to execute the data fetching and uploading task every hour at 5 minutes past the hour.
Environment Variables:

Utilizes environment variables for sensitive information like API keys, secrets, and InfluxDB configuration, loaded via python-dotenv.
The script continuously runs in a loop, ensuring regular data ingestion and storage.
