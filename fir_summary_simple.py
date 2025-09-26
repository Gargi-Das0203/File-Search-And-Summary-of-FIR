import pandas as pd
import re
from datetime import datetime
import os
import sys

class FIRSummarySystemCLI:
    def __init__(self):
        self.fir_data = None
        self.default_file = "Data 1.csv"
    
    def load_data(self, file_path=None):
        """Load FIR data from CSV file with proper encoding handling"""
        if file_path is None:
            file_path = self.default_file
        
        if not os.path.exists(file_path):
            print(f"❌ Error: File '{file_path}' not found.")
            return False
        
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    self.fir_data = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if self.fir_data is None:
                print("❌ Error: Could not decode file with any supported encoding")
                return False
            
            # Validate required columns
            required_columns = ['FIR_NUM', 'FIR_CONTENTS']
            if not all(col in self.fir_data.columns for col in required_columns):
                print("❌ Error: CSV file must contain 'FIR_NUM' and 'FIR_CONTENTS' columns")
                print(f"Available columns: {list(self.fir_data.columns)}")
                return False
            
            # Clean data
            self.fir_data['FIR_NUM'] = self.fir_data['FIR_NUM'].astype(str).str.strip()
            self.fir_data['FIR_CONTENTS'] = self.fir_data['FIR_CONTENTS'].astype(str)
            
            print(f"✅ Successfully loaded {len(self.fir_data)} FIR records from '{os.path.basename(file_path)}'")
            return True
            
        except Exception as e:
            print(f"❌ Error loading file: {str(e)}")
            return False
    
    def extract_info(self, content):
        """Extract key information from FIR content"""
        if not content or pd.isna(content):
            return {}
        
        content = str(content)
        patterns = {
            'date': r'on\s+(?:dt\.?|dated?)\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4})',
            'complainant': r'[Cc]omplt?\.?\s+(?:Sri|Smt|Mr|Mrs|Ms)?\s*([A-Za-z\s]+)\s*\(',
            'location': r'(?:vill?\.?|village|PS|P\.S)[\s\-]*([A-Za-z\s]+)',
            'vehicle': r'(?:bearing|Regd?\.?\s*No\.?)\s*([A-Z]{2}[\-\s]?\d{2}[\-\s]?[A-Z]{1,2}[\-\s]?\d{1,5})',
            'accused': r'(?:accused|rider|driver|culprit)[\s\w]*?([A-Z][a-z]+\s+[A-Z][a-z]+)',
        }
        
        extracted_info = {}
        for key, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                extracted_info[key] = matches[0].strip()[:20] if isinstance(matches[0], str) else matches[0]
        
        return extracted_info
    
    def generate_summary(self, fir_content):
        """Generate a 2-line summary from FIR content"""
        if not fir_content or pd.isna(fir_content):
            return ("No content available for this FIR.", 
                   "Please check the FIR number and try again.")
        
        content = str(fir_content)
        info = self.extract_info(content)
        
        # Set default values
        complainant = info.get('complainant', 'complainant')
        date = info.get('date', 'unknown date')
        location = info.get('location', 'unknown location')
        accused = info.get('accused', 'accused person')
        vehicle = info.get('vehicle', 'vehicle')
        
        # Determine case type and generate summary
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['theft', 'stolen', 'steal']):
            # Theft case
            items = []
            if 'motor' in content_lower or 'm/c' in content_lower:
                items.append('motorcycle')
            if 'mobile' in content_lower or 'phone' in content_lower:
                items.append('mobile phone')
            if 'cash' in content_lower or 'money' in content_lower:
                items.append('cash')
            if 'gold' in content_lower:
                items.append('gold ornaments')
            
            items_text = ', '.join(items) if items else 'valuable items'
            
            line1 = f"Theft case reported by {complainant} on {date} at {location}."
            line2 = f"Stolen items include {items_text} - case registered for investigation."
            
        elif any(word in content_lower for word in ['accident', 'collision', 'dash']):
            # Accident case
            line1 = f"Road accident reported on {date} at {location} involving {vehicle}."
            line2 = f"Case registered for rash and negligent driving - investigation in progress."
            
        elif any(word in content_lower for word in ['drunk', 'alcohol', 'bac']):
            # Drunk driving case
            bac_match = re.search(r'(\d+(?:\.\d+)?)\s*[Mm]g/100\s*[Mm][Ll]', content)
            bac_level = bac_match.group(1) + 'mg/100ml' if bac_match else 'elevated'
            
            line1 = f"Drunk driving case against {accused} on {date} at {location}."
            line2 = f"BAC level: {bac_level}, {vehicle} seized - legal action initiated."
            
        elif any(word in content_lower for word in ['missing', 'fled', 'trace']):
            # Missing person case
            age_match = re.search(r'(\d+)\s*(?:years?|yrs?|Yrs?)', content)
            age = age_match.group(1) + ' years' if age_match else 'unknown age'
            
            line1 = f"Missing person case reported by {complainant} on {date} from {location}."
            line2 = f"Person aged {age} went missing - search and investigation underway."
            
        elif any(word in content_lower for word in ['assault', 'attack', 'beat']):
            # Assault case
            line1 = f"Assault case by {complainant} against {accused} on {date} at {location}."
            line2 = f"Physical assault reported with injuries - case registered for investigation."
            
        else:
            # General case
            line1 = f"Case reported by {complainant} on {date} at {location}."
            line2 = f"Legal case registered - investigation assigned to concerned officer."
        
        return line1, line2
    
    def search_fir(self, fir_number):
        """Search for FIR and return summary"""
        if self.fir_data is None:
            print("❌ Error: No FIR data loaded. Please load a data file first.")
            return None
        
        # Search for FIR (flexible matching)
        matches = self.fir_data[
            self.fir_data['FIR_NUM'].str.contains(fir_number, case=False, na=False) |
            self.fir_data['FIR_NUM'].str.endswith(fir_number, na=False)
        ]
        
        if matches.empty:
            print(f"❌ FIR Number '{fir_number}' not found.")
            print("💡 Use 'list' command to see all available FIR numbers.")
            return None
        
        # Get the first match
        fir_record = matches.iloc[0]
        actual_fir_num = fir_record['FIR_NUM']
        fir_content = fir_record['FIR_CONTENTS']
        
        # Generate summary
        line1, line2 = self.generate_summary(fir_content)
        
        return {
            'fir_number': actual_fir_num,
            'line1': line1,
            'line2': line2,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def list_available_firs(self):
        """List all available FIR numbers"""
        if self.fir_data is None:
            print("❌ Error: No FIR data loaded. Please load a data file first.")
            return
        
        fir_numbers = sorted(self.fir_data['FIR_NUM'].dropna().tolist())
        
        print(f"\n📋 Available FIR Numbers ({len(fir_numbers)} total):")
        print("=" * 50)
        
        # Display in columns
        for i, fir_num in enumerate(fir_numbers, 1):
            print(f"{fir_num:<15}", end="")
            if i % 4 == 0:  # New line every 4 FIRs
                print()
        
        if len(fir_numbers) % 4 != 0:
            print()  # Final newline if needed
        
        print("=" * 50)
    
    def display_summary(self, summary_data):
        """Display FIR summary in formatted output"""
        if not summary_data:
            return
        
        print("\n" + "=" * 60)
        print("📋 FIR SUMMARY REPORT")
        print("=" * 60)
        print(f"📄 FIR Number: {summary_data['fir_number']}")
        print(f"📅 Generated on: {summary_data['timestamp']}")
        print("-" * 60)
        print("📝 TWO-LINE SUMMARY:")
        print("-" * 30)
        print(f"1. {summary_data['line1']}")
        print(f"2. {summary_data['line2']}")
        print("=" * 60)
        print("💡 Tip: The summary above provides key information from the FIR.")
        print("   For detailed information, please refer to the complete FIR document.")
        print()

def main():
    """Main function for command line usage"""
    cli = FIRSummarySystemCLI()
    
    # Check if FIR number provided as command line argument
    if len(sys.argv) > 1:
        fir_number = sys.argv[1]
        
        # Load default file
        if not cli.load_data():
            print("❌ Cannot load FIR data. Please check if 'Data 1.csv' exists.")
            return
        
        # Search for FIR
        summary = cli.search_fir(fir_number)
        cli.display_summary(summary)
    else:
        print("🚔 FIR Summary System")
        print("Usage: python fir_summary_cli.py <FIR_NUMBER>")
        print("Example: python fir_summary_cli.py 0124/2025")
        
        # Load data to show available FIRs
        if cli.load_data():
            cli.list_available_firs()

if __name__ == "__main__":
    main()