# Cryptocurrency Charts

A simple web application built with Streamlit that displays cryptocurrency price and volume charts using data from the Crypto.com API.

## Features

- Real-time cryptocurrency price data
- Interactive price and volume charts
- Multiple time range options
- Top trading pairs supported
- Responsive design

## Requirements

- Python 3.8+
- Required packages listed in `requirements.txt`

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd cryptocurrency-charts
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Crypto.com API credentials:
```env
CRYPTOCOM_API_KEY=your_api_key
CRYPTOCOM_API_SECRET=your_api_secret
```

4. Run the application locally:
```bash
streamlit run app.py
```

## Deployment

This application can be deployed for free on Streamlit Cloud:

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy the application

## Data Source

All cryptocurrency data is provided by the [Crypto.com API](https://crypto.com/exchange/docs/api).

## License

MIT License