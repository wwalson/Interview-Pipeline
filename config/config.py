from dotenv import load_dotenv
import os

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")

#the below is just to make sure the .env is loading correctly
#print(FRED_API_KEY)