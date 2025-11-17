import os
from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '212.2.245.85'),
    'port': os.getenv('DB_PORT', '6432'),
    'database': os.getenv('DB_NAME', 'postgres'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'Tea_IWMZ5wuUta97gupb')
}

def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_address():
    """Search for addresses matching the query."""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Please enter an address to search'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Search for addresses using fuzzy matching
        # Using ILIKE for case-insensitive partial matching
        search_query = '''
            SELECT 
                "Full Address",
                "Mailing City",
                "zipcode"
            FROM team_cool_and_gang.pinellas_fl
            WHERE "Full Address" ILIKE %s
            ORDER BY 
                CASE 
                    WHEN LOWER("Full Address") = LOWER(%s) THEN 0
                    WHEN LOWER("Full Address") LIKE LOWER(%s) THEN 1
                    ELSE 2
                END,
                "Full Address"
            LIMIT 50
        '''
        
        search_pattern = f'%{query}%'
        cursor.execute(search_query, (search_pattern, query, f'{query}%'))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Convert results to list of dicts
        results_list = [dict(row) for row in results]
        
        return jsonify({
            'success': True,
            'count': len(results_list),
            'results': results_list
        })
        
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@app.route('/search/exact', methods=['POST'])
def search_exact():
    """Search for exact address matches."""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Please enter an address to search'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Exact match search (case-insensitive)
        search_query = '''
            SELECT 
                "Full Address",
                "Mailing City",
                "zipcode"
            FROM team_cool_and_gang.pinellas_fl
            WHERE LOWER("Full Address") = LOWER(%s)
            LIMIT 10
        '''
        
        cursor.execute(search_query, (query,))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        results_list = [dict(row) for row in results]
        
        return jsonify({
            'success': True,
            'count': len(results_list),
            'results': results_list
        })
        
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Check if the application and database are healthy."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

