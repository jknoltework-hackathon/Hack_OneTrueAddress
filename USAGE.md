# OneTrueAddress - Usage Guide

## Quick Start

The application is now running! Open your web browser and navigate to:

```
http://localhost:5000
```

## How to Use

### Web Interface

1. **Enter an Address**: Type any address or partial address in the search box
   - Example: "Main St"
   - Example: "123 Maple"
   - Example: "Clearwater"

2. **Choose Search Type**:
   - **Similar Match** (Default): Finds all addresses containing your search text
   - **Exact Match**: Finds only exact matches

3. **Click Search**: Results will display showing:
   - Full Address
   - Mailing City
   - Zipcode

### API Endpoints

#### Fuzzy/Similar Search
```bash
POST http://localhost:5000/search
Content-Type: application/json

{
  "query": "your search text"
}
```

**Example Response:**
```json
{
  "success": true,
  "count": 26,
  "results": [
    {
      "Full Address": "10 VILLAGE LN",
      "Mailing City": "SAFETY HARBOR",
      "zipcode": 34695
    },
    ...
  ]
}
```

#### Exact Match Search
```bash
POST http://localhost:5000/search/exact
Content-Type: application/json

{
  "query": "10 VILLAGE LN"
}
```

#### Health Check
```bash
GET http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## PowerShell Examples

### Search with Fuzzy Match
```powershell
Invoke-RestMethod -Uri http://localhost:5000/search `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"query": "Main St"}'
```

### Search with Exact Match
```powershell
Invoke-RestMethod -Uri http://localhost:5000/search/exact `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"query": "10 VILLAGE LN"}'
```

### Health Check
```powershell
curl http://localhost:5000/health
```

## Database Information

- **Database**: Pinellas County, FL Addresses
- **Total Records**: 29,962 addresses
- **Schema**: `team_cool_and_gang.pinellas_fl`
- **Search Column**: `Full Address`
- **Return Columns**: `Full Address`, `Mailing City`, `zipcode`

## Search Tips

1. **Partial Searches**: You don't need the complete address. Try street names, numbers, or city names.
   
2. **Case Insensitive**: Search is case-insensitive, so "main st" and "MAIN ST" work the same.

3. **Wildcards**: The similar match automatically adds wildcards, so "Village" finds "10 VILLAGE LN".

4. **Result Limits**: 
   - Similar match returns up to 50 results
   - Exact match returns up to 10 results

## Stopping the Server

To stop the Flask application, press `Ctrl+C` in the terminal where it's running.

## Restarting the Server

```bash
python app.py
```

The server will start on `http://0.0.0.0:5000` by default.

