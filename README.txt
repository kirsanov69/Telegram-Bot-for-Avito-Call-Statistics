Telegram Bot for Avito Call Statistics
Overview
This is a Telegram bot designed to fetch and present call statistics for your Avito listings. It allows users to add their Avito API tokens, parse call statistics for their ads, and generate reports in a simple and intuitive format.

Features
Add Avito API Token: Users can securely add multiple Avito API tokens via a Telegram command.
Fetch Call Statistics: Bot parses Avito API to fetch call statistics for all listings associated with each token.
XLSX Report Generation: Generates an Excel report with call statistics for each ad.
Error Handling: Clear error messages in case of issues with the API or bot.
Table of Contents
Technologies
Installation
Bot Commands
API Structure
Running the Bot
Docker Support
Testing Mode
Technologies
Python 3.11
aiogram for Telegram bot interaction
aiohttp for async HTTP requests
SQLAlchemy for database interactions
Avito API
pandas for XLSX report generation
docker and docker-compose for containerization
Installation
Clone the repository:

bash

git clone https://github.com/kirsanov69/Telegram-Bot-for-Avito-Call-Statistics.git
cd Telegram-Bot-for-Avito-Call-Statistics      
Install dependencies:

bash

python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Set environment variables for your bot:

bash

export BOT_TOKEN="your-telegram-bot-token"
export DATABASE_URL="your-database-url"
Setup the database (PostgreSQL or SQLite can be used):

bash

python setup_db.py
Bot Commands
/start - Start the bot and display the welcome message.
/token <your_avito_token> - Add your Avito API token for tracking statistics.
📊 Показать статистику - Fetch and display statistics for all your Avito ads.
/help - Display help information about bot usage.
Example:
bash

/token abc123xyz456
📊 Показать статистику
API Structure
The bot communicates with the Avito API to fetch data on the user's listings and their respective call statistics:

Listings Endpoint: https://api.avito.ru/core/v1/items
Call Stats Endpoint: https://api.avito.ru/core/v1/accounts/{user_id}/calls/stats
The statistics include:

answered: Answered calls
calls: Total calls
new: New calls
newAnswered: New and answered calls
Running the Bot
Run the bot locally:

bash

python webhook.py
You can also set up the bot to work with a webhook for more efficient communication:

bash

python setup_webhook.py
Docker Support
This project is fully containerized using Docker.

Building and Running the Docker Container:
Build the Docker image:

bash

docker-compose build
Run the bot using Docker Compose:

bash

docker-compose up
This will set up both the bot and the database inside Docker containers, enabling easy deployment.

Testing Mode
The bot includes a testing mode for development purposes, allowing you to simulate Avito API responses with mock data. To enable the test mode, simply set the environment variable:

bash

export TEST_MODE=True
In testing mode, the bot will return predefined statistics, useful for testing interaction without needing real API access.

Future Enhancements
Add support for other marketplaces.
Implement advanced report filters (e.g., time range).
Provide options to export reports in additional formats (e.g., CSV, PDF).
