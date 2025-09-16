import csv
import os
from typing import Dict, Any, List
from src.utils.logger import logger


class DataManager:
    def __init__(self, csv_filename: str = "call_analysis.csv"):
        """
        Initialize DataManager with CSV filename.
        
        Args:
            csv_filename: Name of the CSV file to save results
        """
        self.csv_filename = csv_filename
        self.fieldnames = ['Transcript', 'Summary', 'Sentiment']

    def save_to_csv(self, data: Dict[str, Any]) -> bool:
        """
        Save analysis results to CSV file.
        
        Args:
            data: Dictionary containing transcript, summary, and sentiment
            
        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            # Prepare data with only the 3 required columns - no truncation
            csv_data = {
                'Transcript': data.get('transcript', ''),
                'Summary': data.get('summary', ''),
                'Sentiment': data.get('sentiment', '')
            }
            
            # Check if file exists to determine if we need to write headers
            file_exists = os.path.isfile(self.csv_filename)
            
            # Write to CSV
            with open(self.csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                
                # Write header if file is new
                if not file_exists:
                    writer.writeheader()
                    logger.info(f"Created new CSV file: {self.csv_filename}")
                
                # Write data row
                writer.writerow(csv_data)
                logger.info(f"Data saved to {self.csv_filename}")
                
            return True
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            return False

    