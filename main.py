#!/usr/bin/env python3
"""
Certificate Generator - Main Entry Point
Author: AI Assistant
Date: July 2025
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from certificate_generator import CertificateGenerator
from data_handler import DataHandler
import yaml

def load_config(config_path="CERTIFICATE GENERATOR/config/config.yaml"):
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Config file not found: {config_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing config file: {e}")
        return None

def main():
    """Main function to run certificate generation"""
    print("🎓 Certificate Generator - Starting...")
    
    # Load configuration
    config = load_config()
    if not config:
        print("❌ Failed to load configuration. Exiting.")
        return
    
    # Initialize data handler
    data_handler = DataHandler(config['data']['csv_path'])
    
    # Load participant data
    participants = data_handler.load_participants()
    if participants.empty:
        print("❌ No participant data found. Fill the data. Exiting.")
        return
    
    print(f"📊 Loaded {len(participants)} participants")
    
    # Initialize certificate generator
    cert_generator = CertificateGenerator(config)
    
    # Create output directory if it doesn't exist
    output_dir = Path(config['certificate']['output_path'])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate certificates
    successful = 0
    failed = 0
    
    for index, participant in participants.iterrows():
        try:
            cert_generator.generate_certificate(participant)
            successful += 1
            print(f"✅ Generated certificate for {participant['name']}")
        except Exception as e:
            failed += 1
            print(f"❌ Failed to generate certificate for {participant['name']}: {e}")
    
    print(f"\n🎉 Certificate generation complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Certificates saved to: {config['certificate']['output_path']}")

if __name__ == "__main__":
    main()
