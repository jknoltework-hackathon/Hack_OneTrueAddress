# OneTrueAddress - Address Search Application

A web application for searching Pinellas County, FL addresses with fuzzy matching and exact search capabilities.

## Features

- 🔍 **Smart Search**: Find addresses with fuzzy matching for similar results
- 🎯 **Exact Match**: Search for precise address matches
- 🎨 **Modern UI**: Beautiful, responsive interface
- ⚡ **Fast Results**: Quick PostgreSQL queries with optimized searching
- 📱 **Mobile Friendly**: Works seamlessly on all devices

## Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database access

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Hack_OneTrueAddress
```

2. Create a virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your database password
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Search Methods

**Similar Match (Default)**
- Finds addresses that contain your search terms
- Case-insensitive
- Returns up to 50 results
- Best for partial addresses or when unsure of exact format

**Exact Match**
- Finds addresses that exactly match your search
- Case-insensitive
- Returns up to 10 results
- Best when you know the complete address

### API Endpoints

**POST /search**
- Fuzzy/similar address search
- Body: `{"query": "your address"}`
- Returns: List of matching addresses with Full Address, Mailing City, and Zipcode

**POST /search/exact**
- Exact address match search
- Body: `{"query": "your address"}`
- Returns: List of exactly matching addresses

**GET /health**
- Health check endpoint
- Returns application and database status

## Database Schema

**Table**: `team_cool_and_gang.pinellas_fl`

**Columns**:
- `Full Address`: Complete address string
- `Mailing City`: City name
- `Zipcode`: ZIP code

## Development

### Project Structure
```
Hack_OneTrueAddress/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── templates/
    └── index.html        # Web interface
```

### Environment Variables

- `DB_HOST`: Database host (default: 212.2.245.85)
- `DB_PORT`: Database port (default: 6432)
- `DB_NAME`: Database name (default: postgres)
- `DB_USER`: Database username (default: postgres)
- `DB_PASSWORD`: Database password (required)
- `FLASK_ENV`: Flask environment (development/production)
- `FLASK_DEBUG`: Enable debug mode (True/False)

## Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Set `FLASK_DEBUG=False`
3. Use a production WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
