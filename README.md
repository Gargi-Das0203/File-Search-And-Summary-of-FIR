# 🚔 FIR Summary System

A comprehensive system to upload FIR (First Information Report) data and generate concise two-line summaries for any FIR number. This system provides multiple interfaces to access FIR summaries quickly and efficiently.

## 📁 Files Overview

- **`Data 1.csv`** - Sample FIR data file (already provided)
- **`fir_summary_system.py`** - Desktop GUI application (Tkinter)
- **`fir_summary_web.html`** - Web-based interface (runs in browser)
- **`fir_summary_cli.py`** - Command-line interface

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)
1. Open `fir_summary_web.html` in your web browser
2. Click "Choose CSV File" to upload your FIR data or use the pre-loaded data
3. Enter a FIR number (e.g., `0124/2025`) and click "Get Summary"
4. Get instant two-line summaries!

### Option 2: Desktop Application
1. Run the desktop application:
   ```bash
   python fir_summary_system.py
   ```
2. Upload your CSV file or use the default `Data 1.csv`
3. Enter FIR number and get summary

### Option 3: Command Line
1. Interactive mode:
   ```bash
   python fir_summary_cli.py
   ```
2. Direct search:
   ```bash
   python fir_summary_cli.py 0124/2025
   ```

## 📊 CSV File Format

Your CSV file must contain these columns:
- **FIR_NUM** - FIR number (e.g., "0124/2025")
- **FIR_CONTENTS** - Detailed FIR content/description

Example:
```csv
FIR_NUM,FIR_CONTENTS
0124/2025,"The brief fact of the case is that on dt 14.02.2025..."
0145/2025,"The brief fact of the case is that on dt 23.02.2025..."
```

## 🔍 Sample Queries

Try these FIR numbers with the provided data:

- **`0124/2025`** - Drunk driving case
- **`0145/2025`** - Another drunk driving incident  
- **`0682/2024`** - Murder case
- **`0526/2024`** - Theft case
- **`0255/2025`** - Missing person case

## ✨ Features

### 🧠 Intelligent Summarization
The system automatically detects case types and generates appropriate summaries:

- **📱 Theft Cases** - Identifies stolen items (motorcycles, phones, cash, gold)
- **🚗 Accidents** - Extracts vehicle details and incident location
- **🍺 Drunk Driving** - Shows BAC levels and penalties
- **👤 Missing Persons** - Includes age and location details  
- **⚔️ Assault Cases** - Identifies parties and incident details
- **📋 General Cases** - Provides basic case information

### 🎯 Sample Output
```
📋 FIR Number: 0124/2025
📅 Generated on: 2025-09-26 14:30:15
═══════════════════════════════════════════════════════════

📄 TWO-LINE SUMMARY:
──────────────────────────────
1. Drunk driving case against Saroj Banichor on 14.02.2025 at Thana Chhak, Angul.
2. BAC level: 286mg/100ml, Mahindra Bolero Plus OD35B-8376 seized - legal action initiated.
```

## 🔧 Advanced Usage

### Command Line Interface Commands
```bash
search <FIR_NUMBER>  # Get summary for specific FIR
list                 # Show all available FIR numbers  
load <FILE_PATH>     # Load different CSV file
help                # Show help message
exit                # Exit program
```

### Web Interface Features
- **📁 File Upload** - Drag & drop or click to upload CSV files
- **🔍 Smart Search** - Flexible FIR number matching
- **📋 Browse FIRs** - View all available FIR numbers
- **📱 Responsive** - Works on desktop and mobile devices

## 🛠️ Technical Details

### System Requirements
- **Python 3.6+** (for GUI and CLI versions)
- **pandas** library for data processing
- **tkinter** for desktop GUI (usually included with Python)
- **Modern web browser** for web interface

### Installation
```bash
# Install required packages
pip install pandas

# No additional installation needed - ready to run!
```

### Data Processing
- Handles various FIR number formats (0124/2025, 124/2025, etc.)
- Extracts key information using regex patterns:
  - Dates and times
  - Complainant names
  - Locations and addresses
  - Vehicle registration numbers
  - Accused persons
  - Case types and sections

## 📈 Use Cases

### 👮 Law Enforcement
- Quick case overview for officers
- Rapid case type identification
- Efficient case briefing

### 📊 Administrative
- Case statistics and reporting
- Quick case lookup for queries
- Case categorization

### 🎓 Training & Research  
- Case study preparation
- Legal research assistance
- Training material generation

## 🔐 Privacy & Security

- **Local Processing** - All data processing happens locally
- **No Data Storage** - System doesn't store uploaded data permanently
- **Privacy First** - No data sent to external servers

## 🤝 Contributing

Feel free to enhance the system by:
- Adding new case type detection patterns
- Improving summary generation algorithms
- Adding export features
- Enhancing the user interface

## 📞 Support

For questions or issues:
1. Check the sample FIR numbers provided
2. Ensure CSV file format is correct
3. Verify FIR number formatting
4. Use the "Show Available FIR Numbers" feature

## 📋 Example Workflow

1. **Upload Data** → Load your FIR CSV file
2. **Browse FIRs** → See all available FIR numbers  
3. **Search** → Enter any FIR number
4. **Get Summary** → Receive instant two-line summary
5. **Copy/Use** → Use the summary for reports or briefings

---

**🚔 FIR Summary System** - Making case information accessible and actionable!
