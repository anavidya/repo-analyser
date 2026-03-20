# constants.py

PDF_STYLES = """
    body { font-family: Arial, sans-serif; font-size: 12px; color: #333; }
    
    .tabcontent {
        display: block !important;
        page-break-before: always;
        margin-bottom: 40px;
        padding: 20px;
    }
    .tabcontent:first-of-type { page-break-before: avoid; }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        font-size: 11px;
    }
    th {
        background-color: #2c3e50 !important;
        color: white !important;
        padding: 8px;
        text-align: left;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    td { padding: 6px 8px; border-bottom: 1px solid #ddd; }
    tr:nth-child(even) { background-color: #f9f9f9; }
    
    h1 { font-size: 24px; color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
    h2 { font-size: 18px; color: #2c3e50; margin-top: 30px; }
    h3 { font-size: 14px; color: #34495e; }
    
    .metrics-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
    .metric-card { border: 1px solid #ddd; padding: 10px; min-width: 100px; text-align: center; }
    
    code { background: #f4f4f4; padding: 2px 4px; border-radius: 3px; font-size: 10px; }
"""

PDF_TAB_ORDER = [
    'Overview',
    'Packages',
    'Security',
    'Code_Review',
    'PythonCode',
    'CI_CD',
    'Docker',
    'Mermaid',
    'Test_Coverage',
]