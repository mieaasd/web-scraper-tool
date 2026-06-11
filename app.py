from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from datetime import datetime
from scrapers.ecommerce_scraper import EcommerceScraper
from scrapers.realestate_scraper import RealEstateScraper
from scrapers.job_scraper import JobScraper
from utils.data_processor import DataProcessor

app = Flask(__name__)
CORS(app)

if not os.path.exists('downloads'):
    os.makedirs('downloads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        url = data.get('url', '').strip()
        scrape_type = data.get('type', '')
        output_format = data.get('format', 'csv')
        
        if not url:
            return jsonify({'success': False, 'message': 'Please provide a URL'}), 400
        
        if not url.startswith('http'):
            url = 'https://' + url
        
        if scrape_type not in ['ecommerce', 'realestate', 'job']:
            return jsonify({'success': False, 'message': 'Invalid scrape type'}), 400
        
        scraper_map = {
            'ecommerce': EcommerceScraper(),
            'realestate': RealEstateScraper(),
            'job': JobScraper()
        }
        
        scraper = scraper_map[scrape_type]
        results = scraper.scrape(url)
        
        if not results:
            return jsonify({'success': False, 'message': 'No data found'}), 400
        
        processor = DataProcessor()
        filename = processor.save_data(results, scrape_type, output_format)
        
        return jsonify({
            'success': True,
            'message': f'Successfully scraped {len(results)} items',
            'data': results[:10],
            'total_items': len(results),
            'download_url': f'/api/download/{filename}'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/download/<filename>')
def download(filename):
    try:
        filepath = os.path.join('downloads', filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        return jsonify({'success': False, 'message': 'File not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))