# VALRLendingRates
This script fetches ZAR loan rate data from the VALR API, converts rates to annualized percentages, and uploads them to InfluxDB to be analyzed. It uses HMAC authentication for secure API access, processes data, and schedules hourly execution at 5 minutes past the hour, with credentials managed via environment variables.
