"""
Data Handler Module
Handles CSV data loading and validation
"""

import pandas as pd
import os
from pathlib import Path

class DataHandler:
    def __init__(self, csv_path):
        """Initialize data handler with CSV file path"""
        self.csv_path = csv_path
        self.required_columns = ['name', 'course', 'completion_date']
    
    def load_participants(self):
        """Load participant data from CSV file"""
        try:
            # Check if file exists
            if not os.path.exists(self.csv_path):
                self._create_sample_csv()
            
            # Load CSV
            df = pd.read_csv(self.csv_path)
            
            # Validate columns
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                print(f"Warning: Missing columns in CSV: {missing_columns}")
                # Add missing columns with default values
                for col in missing_columns:
                    if col == 'course':
                        df[col] = 'General Course'
                    else:
                        df[col] = 'Unknown'
            
            # Clean data
            df = self._clean_data(df)
            
            return df
            
        except Exception as e:
            print(f"Error loading participant data: {e}")
            return pd.DataFrame()
    
    def _create_sample_csv(self):
        """Create a sample CSV file with participant data"""
        sample_data = {
            'name': [
                'John Smith',
                'Emily Johnson', 
                'Michael Brown',
                'Sarah Davis',
                'David Wilson',
                'Lisa Anderson',
                'Robert Taylor',
                'Jennifer Martinez',
                'William Garcia',
                'Maria Rodriguez'
            ],
            'course': [
                'Python Programming Fundamentals',
                'Web Development Bootcamp',
                'Data Science with Python',
                'Machine Learning Basics',
                'Full Stack Development',
                'Database Management',
                'Mobile App Development',
                'Cloud Computing Essentials',
                'Cybersecurity Fundamentals',
                'Digital Marketing Strategy'
            ],
            'completion_date': [
                'July 15, 2025',
                'July 16, 2025',
                'July 17, 2025',
                'July 18, 2025',
                'July 19, 2025',
                'July 20, 2025',
                'July 21, 2025',
                'July 22, 2025',
                'July 23, 2025',
                'July 24, 2025'
            ]
        }
        
        # Create data directory if it doesn't exist
        data_dir = os.path.dirname(self.csv_path)
        os.makedirs(data_dir, exist_ok=True)
        
        # Create sample CSV
        df = pd.DataFrame(sample_data)
        df.to_csv(self.csv_path, index=False)
        print(f"📊 Created sample CSV file at {self.csv_path}")
    
    def _clean_data(self, df):
        """Clean and validate participant data"""
        # Remove empty rows
        df = df.dropna(subset=['name'])
        
        # Strip whitespace
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
        
        # Remove duplicates based on name
        df = df.drop_duplicates(subset=['name'], keep='first')
        
        return df
    
    def add_participant(self, name, course, completion_date):
        """Add a new participant to the CSV file"""
        try:
            # Load existing data
            df = pd.read_csv(self.csv_path) if os.path.exists(self.csv_path) else pd.DataFrame()
            
            # Create new participant record
            new_participant = {
                'name': name,
                'course': course,
                'completion_date': completion_date
            }
            
            # Add to dataframe
            df = pd.concat([df, pd.DataFrame([new_participant])], ignore_index=True)
            
            # Save back to CSV
            df.to_csv(self.csv_path, index=False)
            
            return True
            
        except Exception as e:
            print(f"Error adding participant: {e}")
            return False
