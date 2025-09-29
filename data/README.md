# Data Directory

## Overview

This directory contains data files, uploads, temporary files, and analytics reports for the Real-Estate-Marketplace application.

**Author:** Gabriel Demetrios Lafis  
**Date:** September 2025

## Directory Structure

```
data/
├── README.md           # This file
├── sample.csv          # Sample real estate data
├── uploads/            # User uploaded files
├── temp/               # Temporary processing files
└── reports/            # Generated analytics reports
```

## Subdirectories

### uploads/
Stores files uploaded by users through the web interface. Supported formats:
- CSV (.csv)
- Excel (.xlsx, .xls)
- JSON (.json)
- Text (.txt)

### temp/
Temporary directory for data processing operations. Files in this directory are automatically cleaned up after processing.

### reports/
Stores generated analytics reports and visualizations:
- PDF reports
- CSV exports
- JSON data exports
- PNG/JPEG visualizations from R analytics

## Sample Data

The `sample.csv` file contains example real estate data with the following structure:

| Column | Description | Type |
|--------|-------------|------|
| property_id | Unique property identifier | Integer |
| address | Property address | String |
| city | City location | String |
| state | State/Province | String |
| price | Listing price | Float |
| bedrooms | Number of bedrooms | Integer |
| bathrooms | Number of bathrooms | Float |
| square_feet | Property size in sq ft | Integer |
| year_built | Year of construction | Integer |
| property_type | Type (House, Condo, etc.) | String |
| listing_date | Date listed | Date |
| status | Listing status | String |

## Usage Guidelines

### Data Processing
1. Place input data files in this directory
2. Reference them in your Python scripts or R analytics
3. Processed results will be saved to appropriate subdirectories

### File Management
- Maximum file size: 16MB (configurable in config.py)
- Temporary files are auto-deleted after 24 hours
- Reports are kept indefinitely unless manually deleted

### Security
- Do not commit sensitive or personal data to version control
- Add `.gitignore` rules for uploaded files and temporary data
- Ensure proper file permissions for production deployments

## Data Analytics

The R analytics script (`analytics.R`) can process data from this directory:

```r
# Load data
analyzer <- DataAnalyzer$new()
analyzer$load_data('data/sample.csv')

# Run analysis
analyzer$analyze()
analyzer$generate_report(output_dir='data/reports')
```

## API Integration

The application's API endpoints interact with this directory:

- `POST /api/upload` - Upload files to `uploads/`
- `GET /api/data` - Retrieve data files
- `GET /api/reports` - Access generated reports

## Maintenance

### Cleanup
```bash
# Remove temporary files
rm -rf data/temp/*

# Archive old reports
tar -czf reports_archive_$(date +%Y%m%d).tar.gz data/reports/
```

### Backup
Regularly backup important data:
```bash
# Backup data directory
cp -r data/ ../backups/data_$(date +%Y%m%d)/
```

## Contact

For questions about data structure or processing:
- Email: gabrieldemetrios@gmail.com
- GitHub: @galafis
