import os
import pandas as pd
from typing import List
from fastapi import HTTPException

from app.core import logger


def check_csv_file_exists(file_path: str, columns: List[str]) -> None:
    """
    Check if the CSV file exists with specified columns
    
    Args:
        file_path: Path to the CSV file
        columns: List of column names
    """
    
    # Create directory if it doesn't exist
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")
        
    # Create file if it doesn't exist
    if not os.path.exists(file_path):
        # Create empty DataFrame with columns
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        logger.info(f"Created CSV file: {file_path} with columns: {columns}")
        
        
def read_csv_file(file_path: str, columns: List[str]) -> pd.DataFrame:
    """
    Read data from a CSV file
    
    Args:
        file_path: Path to the CSV file
        columns: Expected columns in the CSV file
        
    Returns:
        DataFrame containing the CSV data
    """
    
    try:
        # Check if file exists
        check_csv_file_exists(file_path, columns)
        
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Validate columns
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            logger.warning(f"Missing columns in CSV file: {missing_columns}")
            # Add missing columns
            for col in missing_columns:
                df[col] = None
            # Save updated DataFrame
            df.to_csv(file_path, index=False)
            logger.info(f"Added missing columns to CSV file: {missing_columns}")
            
        return df
    except Exception as e:
        logger.error(f"Error reading CSV file {file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    
def write_csv_file(file_path: str, df: pd.DataFrame) -> None:
    """
    Write data to a CSV file
    
    Args:
        file_path: Path to the CSV file
        df: DataFrame to write
    """
    
    try:
        df.to_csv(file_path, index=False)
        logger.debug(f"Wrote {len(df)} rows to CSV file: {file_path}")
    except Exception as e:
        logger.error(f"Error writing to CSV file {file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")