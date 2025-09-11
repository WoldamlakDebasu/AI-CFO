import React, { useState, useRef } from 'react';
import axios from 'axios';
import './FileUpload.css';

function FileUpload({ onAnalysis, onLoading }) {
    const [dragOver, setDragOver] = useState(false);
    const [industry, setIndustry] = useState('default');
    const [businessSize, setBusinessSize] = useState('small');
    const [error, setError] = useState(null);
    const [uploading, setUploading] = useState(false);
    const fileInputRef = useRef(null);

    const industries = {
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
    };

    const businessSizes = {
        'micro': 'Micro Business (1-9 employees)',
        'small': 'Small Business (10-49 employees)',
        'medium': 'Medium Business (50-249 employees)',
        'large': 'Large Business (250+ employees)'
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragOver(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setDragOver(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragOver(false);
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    };

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    };

    const handleFileUpload = async (file) => {
        setError(null);
        setUploading(true);
        onLoading(true);

        // Validate file type
        const allowedTypes = ['.csv', '.xlsx', '.xls'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(fileExtension)) {
            setError(`Unsupported file type: ${fileExtension}. Please upload CSV or Excel files.`);
            setUploading(false);
            onLoading(false);
            return;
        }

        // Validate file size (16MB max)
        const maxSize = 16 * 1024 * 1024; // 16MB
        if (file.size > maxSize) {
            setError('File too large. Maximum size is 16MB.');
            setUploading(false);
            onLoading(false);
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('industry', industry);
        formData.append('business_size', businessSize);

        try {
            const response = await axios.post('/api/analyze', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                timeout: 120000, // 2 minutes timeout
            });

            if (response.data.error) {
                setError(response.data.message || 'Analysis failed');
                onAnalysis(response.data);
            } else {
                onAnalysis(response.data);
            }
        } catch (error) {
            console.error('Upload error:', error);
            
            if (error.code === 'ECONNABORTED') {
                setError('Analysis timeout. Please try with a smaller file or check your connection.');
            } else if (error.response) {
                const errorData = error.response.data;
                setError(errorData.message || `Server error (${error.response.status})`);
            } else if (error.request) {
                setError('Network error. Please check your connection and try again.');
            } else {
                setError('An unexpected error occurred. Please try again.');
            }
        } finally {
            setUploading(false);
            onLoading(false);
        }
    };

    const handleButtonClick = () => {
        fileInputRef.current?.click();
    };

    const downloadSampleTemplate = () => {
        // Create sample CSV data
        const sampleData = [
            ['date', 'description', 'amount', 'category'],
            ['2024-01-01', 'Client Payment - Project A', '5000', 'income'],
            ['2024-01-02', 'Office Rent', '-1200', 'expense'],
            ['2024-01-03', 'Software License', '-299', 'expense'],
            ['2024-01-05', 'Consulting Revenue', '3500', 'income'],
            ['2024-01-08', 'Marketing Campaign', '-800', 'expense'],
            ['2024-01-10', 'Product Sales', '2200', 'income'],
            ['2024-01-12', 'Utilities', '-150', 'expense'],
            ['2024-01-15', 'Freelance Payment', '1500', 'income']
        ];

        const csvContent = sampleData.map(row => row.join(',')).join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'financial_data_template.csv';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    };

    return (
        <div className="file-upload-container">
            <div className="upload-header">
                <h2>🤖 AI CFO Financial Analysis</h2>
                <p>Upload your financial data and get instant AI-powered insights</p>
            </div>

            {/* Business Settings */}
            <div className="business-settings">
                <div className="setting-group">
                    <label htmlFor="industry">Industry Type:</label>
                    <select 
                        id="industry"
                        value={industry} 
                        onChange={(e) => setIndustry(e.target.value)}
                        className="setting-select"
                    >
                        {Object.entries(industries).map(([key, label]) => (
                            <option key={key} value={key}>{label}</option>
                        ))}
                    </select>
                </div>

                <div className="setting-group">
                    <label htmlFor="business-size">Business Size:</label>
                    <select 
                        id="business-size"
                        value={businessSize} 
                        onChange={(e) => setBusinessSize(e.target.value)}
                        className="setting-select"
                    >
                        {Object.entries(businessSizes).map(([key, label]) => (
                            <option key={key} value={key}>{label}</option>
                        ))}
                    </select>
                </div>
            </div>

            {/* File Upload Area */}
            <div 
                className={`upload-area ${dragOver ? 'drag-over' : ''} ${uploading ? 'uploading' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={handleButtonClick}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".csv,.xlsx,.xls"
                    onChange={handleFileSelect}
                    style={{ display: 'none' }}
                />
                
                {uploading ? (
                    <div className="upload-progress">
                        <div className="upload-spinner"></div>
                        <h3>🔄 Analyzing Your Data...</h3>
                        <p>Our AI is processing your financial information</p>
                        <div className="progress-steps">
                            <div className="step active">📊 Reading data</div>
                            <div className="step active">🧮 Computing metrics</div>
                            <div className="step active">🤖 Generating insights</div>
                            <div className="step">✅ Complete</div>
                        </div>
                    </div>
                ) : (
                    <div className="upload-content">
                        <div className="upload-icon">📈</div>
                        <h3>Drop your financial data here</h3>
                        <p>Or click to browse files</p>
                        <div className="supported-formats">
                            <span className="format-badge">CSV</span>
                            <span className="format-badge">Excel (.xlsx)</span>
                            <span className="format-badge">Excel (.xls)</span>
                        </div>
                        <div className="upload-limits">
                            Maximum file size: 16MB
                        </div>
                    </div>
                )}
            </div>

            {/* Error Display */}
            {error && (
                <div className="error-message">
                    <div className="error-icon">⚠️</div>
                    <div className="error-content">
                        <strong>Upload Error</strong>
                        <p>{error}</p>
                    </div>
                </div>
            )}

            {/* Help Section */}
            <div className="help-section">
                <div className="help-grid">
                    <div className="help-item">
                        <div className="help-icon">📋</div>
                        <h4>Data Format</h4>
                        <p>Ensure your file contains columns like 'date', 'amount', 'description', and 'category' for best results.</p>
                    </div>
                    
                    <div className="help-item">
                        <div className="help-icon">🎯</div>
                        <h4>AI Analysis</h4>
                        <p>Get insights on cash flow, profitability, trends, risks, and personalized recommendations.</p>
                    </div>
                    
                    <div className="help-item">
                        <div className="help-icon">🏆</div>
                        <h4>Benchmarking</h4>
                        <p>Compare your performance against industry standards and get competitive insights.</p>
                    </div>
                </div>

                <div className="template-section">
                    <h4>Need help formatting your data?</h4>
                    <button 
                        className="template-button"
                        onClick={downloadSampleTemplate}
                    >
                        📥 Download Sample Template
                    </button>
                </div>
            </div>

            {/* Features Preview */}
            <div className="features-preview">
                <h3>What you'll get:</h3>
                <div className="features-grid">
                    <div className="feature-item">
                        <span className="feature-icon">💰</span>
                        <span>Cash Flow Analysis</span>
                    </div>
                    <div className="feature-item">
                        <span className="feature-icon">📊</span>
                        <span>Profitability Insights</span>
                    </div>
                    <div className="feature-item">
                        <span className="feature-icon">📈</span>
                        <span>Trend Forecasting</span>
                    </div>
                    <div className="feature-item">
                        <span className="feature-icon">🎯</span>
                        <span>Health Score</span>
                    </div>
                    <div className="feature-item">
                        <span className="feature-icon">⚠️</span>
                        <span>Risk Detection</span>
                    </div>
                    <div className="feature-item">
                        <span className="feature-icon">💡</span>
                        <span>AI Recommendations</span>
                    </div>
                    <div className="feature-item">
                        <span className="feature-icon">🏆</span>
                        <span>Industry Benchmarks</span>
                    </div>
                    <div className="feature-item">
                        <span className="feature-icon">🔮</span>
                        <span>6-Month Forecast</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default FileUpload;
