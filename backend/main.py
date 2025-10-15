from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from services import FinancialAnalysisService
import os
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../frontend/dist')
CORS(app)  # Enable CORS for frontend integration

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """
    Advanced financial data analysis endpoint with comprehensive insights.
    """
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({
                'error': True,
                'message': 'No file uploaded',
                'code': 'NO_FILE'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'error': True,
                'message': 'No file selected',
                'code': 'EMPTY_FILENAME'
            }), 400
        
        # Get optional parameters
        industry = request.form.get('industry', 'default')
        business_size = request.form.get('business_size', 'small')
        
        # Validate file type
        allowed_extensions = {'.csv', '.xlsx', '.xls'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return jsonify({
                'error': True,
                'message': f'Unsupported file type: {file_ext}. Please upload CSV or Excel files.',
                'code': 'INVALID_FILE_TYPE',
                'supported_formats': list(allowed_extensions)
            }), 400
        
        # Process the file
        logger.info(f"Processing file: {file.filename}, Industry: {industry}, Size: {business_size}")
        
        analysis_result = FinancialAnalysisService.process_financial_data(
            file, 
            user_industry=industry, 
            business_size=business_size
        )
        
        # Log successful analysis
        if not analysis_result.get('error'):
            logger.info(f"Analysis completed successfully for {file.filename}")
        
        return jsonify(analysis_result)
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({
            'error': True,
            'message': f'Analysis failed: {str(e)}',
            'code': 'ANALYSIS_ERROR',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/templates', methods=['GET'])
def get_data_templates():
    """
    Get data format templates for different business types.
    """
    try:
        templates = FinancialAnalysisService.get_data_template()
        return jsonify({
            'success': True,
            'templates': templates,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Template retrieval error: {str(e)}")
        return jsonify({
            'error': True,
            'message': 'Failed to retrieve templates',
            'code': 'TEMPLATE_ERROR'
        }), 500

@app.route('/api/export/<format_type>', methods=['POST'])
def export_analysis(format_type):
    """
    Export analysis results in various formats.
    """
    try:
        analysis_data = request.get_json()
        if not analysis_data:
            return jsonify({
                'error': True,
                'message': 'No analysis data provided',
                'code': 'NO_DATA'
            }), 400
        
        exported_data = FinancialAnalysisService.export_analysis(analysis_data, format_type)
        
        response_data = {
            'success': True,
            'format': format_type,
            'data': exported_data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Set appropriate content type for different formats
        if format_type == 'csv':
            response_data['content_type'] = 'text/csv'
        elif format_type == 'json':
            response_data['content_type'] = 'application/json'
        else:
            response_data['content_type'] = 'text/plain'
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        return jsonify({
            'error': True,
            'message': f'Export failed: {str(e)}',
            'code': 'EXPORT_ERROR'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and deployment.
    """
    return jsonify({
        'status': 'healthy',
        'service': 'AI CFO Financial Analysis',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'features': [
            'Advanced Financial Analysis',
            'AI-Powered Insights',
            'Industry Benchmarking',
            'Anomaly Detection',
            'Financial Health Scoring',
            'Trend Forecasting'
        ]
    })

@app.route('/api/industries', methods=['GET'])
def get_industries():
    """
    Get list of supported industries for benchmarking.
    """
    industries = {
        'retail': 'Retail & E-commerce',
        'services': 'Professional Services',
        'manufacturing': 'Manufacturing',
        'technology': 'Technology & Software',
        'consulting': 'Consulting',
        'healthcare': 'Healthcare',
        'construction': 'Construction',
        'hospitality': 'Hospitality & Tourism',
        'education': 'Education',
        'default': 'Other/General Business'
    }
    
    return jsonify({
        'industries': industries,
        'default': 'default'
    })

@app.route('/api/business-sizes', methods=['GET'])
def get_business_sizes():
    """
    Get supported business size categories.
    """
    sizes = {
        'micro': 'Micro Business (1-9 employees)',
        'small': 'Small Business (10-49 employees)',
        'medium': 'Medium Business (50-249 employees)',
        'large': 'Large Business (250+ employees)'
    }
    
    return jsonify({
        'sizes': sizes,
        'default': 'small'
    })

@app.errorhandler(413)
def file_too_large(error):
    """Handle file too large error."""
    return jsonify({
        'error': True,
        'message': 'File too large. Maximum size is 16MB.',
        'code': 'FILE_TOO_LARGE'
    }), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': True,
        'message': 'Endpoint not found',
        'code': 'NOT_FOUND'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': True,
        'message': 'Internal server error',
        'code': 'INTERNAL_ERROR'
    }), 500

# Static file serving for production
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve React frontend."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting AI CFO Financial Analysis Service on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
