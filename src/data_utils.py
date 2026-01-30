"""
Data utility functions for EthioPulse-Forecaster

This module provides functions for:
- Loading and validating unified schema data
- Enriching datasets with new observations, events, and impact links
- Data quality checks and transformations
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedSchemaValidator:
    """Validates data against the unified schema requirements"""
    
    REQUIRED_COLUMNS = {
        'observations': ['record_type', 'year', 'value', 'pillar', 'source_type', 'confidence'],
        'events': ['record_type', 'year', 'event_name', 'event_type', 'source_type', 'confidence'],
        'impact_links': ['record_type', 'source_event', 'target_observation', 'impact_direction', 'confidence']
    }
    
    @staticmethod
    def validate_record_type(df: pd.DataFrame) -> bool:
        """Ensure record_type is one of: observation, event, impact_link, target, baseline, forecast"""
        valid_types = ['observation', 'event', 'impact_link', 'target', 'baseline', 'forecast']
        if 'record_type' not in df.columns:
            return False
        invalid = df[~df['record_type'].isin(valid_types)]
        if len(invalid) > 0:
            logger.warning(f"Invalid record_type values found: {invalid['record_type'].unique()}")
            return False
        return True
    
    @staticmethod
    def validate_events_no_pillar(df: pd.DataFrame) -> bool:
        """Ensure events have NO pillar assignment (pillar-agnostic)"""
        events = df[df['record_type'] == 'event']
        if len(events) > 0 and 'pillar' in events.columns:
            has_pillar = events['pillar'].notna().any()
            if has_pillar:
                logger.error("Events must NOT have pillar assignments")
                return False
        return True
    
    @staticmethod
    def validate_impact_links(df: pd.DataFrame) -> bool:
        """Validate impact_link records reference valid events and observations"""
        impact_links = df[df['record_type'] == 'impact_link']
        if len(impact_links) == 0:
            return True
        
        events = set(df[df['record_type'] == 'event'].index)
        observations = set(df[df['record_type'] == 'observation'].index)
        
        if 'source_event' in impact_links.columns:
            invalid_events = impact_links[~impact_links['source_event'].isin(events)]
            if len(invalid_events) > 0:
                logger.warning(f"Impact links reference invalid events: {len(invalid_events)}")
        
        if 'target_observation' in impact_links.columns:
            invalid_obs = impact_links[~impact_links['target_observation'].isin(observations)]
            if len(invalid_obs) > 0:
                logger.warning(f"Impact links reference invalid observations: {len(invalid_obs)}")
        
        return True


def load_unified_data(file_path: str) -> pd.DataFrame:
    """
    Load the unified schema dataset (supports CSV and Excel formats)
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV or Excel file
        
    Returns:
    --------
    pd.DataFrame
        Loaded dataset with validated schema
    """
    logger.info(f"Loading unified data from {file_path}")
    
    # Support both CSV and Excel formats
    if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)
    
    validator = UnifiedSchemaValidator()
    
    # Basic validations
    if not validator.validate_record_type(df):
        raise ValueError("Invalid record_type values in dataset")
    
    if not validator.validate_events_no_pillar(df):
        raise ValueError("Events must not have pillar assignments")
    
    logger.info(f"Loaded {len(df)} records")
    logger.info(f"Record types: {df['record_type'].value_counts().to_dict()}")
    
    return df


def load_reference_codes(file_path: str) -> pd.DataFrame:
    """
    Load reference codes for data interpretation (supports CSV and Excel formats)
    
    Parameters:
    -----------
    file_path : str
        Path to reference_codes.csv or .xlsx
        
    Returns:
    --------
    pd.DataFrame
        Reference codes dataframe
    """
    logger.info(f"Loading reference codes from {file_path}")
    
    # Support both CSV and Excel formats
    if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path)
    else:
        return pd.read_csv(file_path)


def quantify_dataset_composition(df: pd.DataFrame) -> Dict:
    """
    Quantify dataset composition by record_type, pillar, source_type, confidence
    
    Parameters:
    -----------
    df : pd.DataFrame
        Unified schema dataset
        
    Returns:
    --------
    Dict
        Composition statistics
    """
    composition = {
        'total_records': len(df),
        'by_record_type': df['record_type'].value_counts().to_dict(),
        'by_pillar': df[df['record_type'] == 'observation']['pillar'].value_counts().to_dict() if 'pillar' in df.columns else {},
        'by_source_type': df['source_type'].value_counts().to_dict() if 'source_type' in df.columns else {},
        'by_confidence': df['confidence'].value_counts().to_dict() if 'confidence' in df.columns else {},
        'year_range': {
            'min': int(df['year'].min()) if 'year' in df.columns else None,
            'max': int(df['year'].max()) if 'year' in df.columns else None
        }
    }
    
    return composition


def add_observation(
    df: pd.DataFrame,
    year: int,
    value: float,
    pillar: str,
    source_type: str,
    confidence: str,
    metadata: Optional[Dict] = None
) -> pd.DataFrame:
    """
    Add a new observation record to the dataset
    
    Parameters:
    -----------
    df : pd.DataFrame
        Existing dataset
    year : int
        Year of observation
    value : float
        Observed value
    pillar : str
        'access' or 'usage'
    source_type : str
        Source identifier (e.g., 'IMF_FAS', 'GSMA', 'ITU', 'NBE')
    confidence : str
        Confidence level ('high', 'medium', 'low')
    metadata : Dict, optional
        Additional metadata fields
        
    Returns:
    --------
    pd.DataFrame
        Dataset with new observation added
    """
    if pillar not in ['access', 'usage']:
        raise ValueError(f"Pillar must be 'access' or 'usage', got '{pillar}'")
    
    new_record = {
        'record_type': 'observation',
        'year': year,
        'value': value,
        'pillar': pillar,
        'source_type': source_type,
        'confidence': confidence
    }
    
    if metadata:
        new_record.update(metadata)
    
    # Ensure all columns exist
    for col in df.columns:
        if col not in new_record:
            new_record[col] = None
    
    new_df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    logger.info(f"Added observation: {pillar} {year} = {value} ({source_type}, {confidence})")
    
    return new_df


def add_event(
    df: pd.DataFrame,
    year: int,
    event_name: str,
    event_type: str,
    source_type: str,
    confidence: str,
    metadata: Optional[Dict] = None
) -> pd.DataFrame:
    """
    Add a new event record (pillar-agnostic)
    
    Parameters:
    -----------
    df : pd.DataFrame
        Existing dataset
    year : int
        Year of event
    event_name : str
        Name/description of event
    event_type : str
        Type of event (e.g., 'policy', 'infrastructure', 'market')
    source_type : str
        Source identifier
    confidence : str
        Confidence level
    metadata : Dict, optional
        Additional metadata
        
    Returns:
    --------
    pd.DataFrame
        Dataset with new event added
    """
    new_record = {
        'record_type': 'event',
        'year': year,
        'event_name': event_name,
        'event_type': event_type,
        'source_type': source_type,
        'confidence': confidence
        # NOTE: NO pillar field - events are pillar-agnostic
    }
    
    if metadata:
        new_record.update(metadata)
    
    # Ensure all columns exist
    for col in df.columns:
        if col not in new_record:
            new_record[col] = None
    
    new_df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    logger.info(f"Added event: {event_name} ({year}, {event_type}, {confidence})")
    
    return new_df


def add_impact_link(
    df: pd.DataFrame,
    source_event_idx: int,
    target_observation_idx: int,
    impact_direction: str,
    confidence: str,
    metadata: Optional[Dict] = None
) -> pd.DataFrame:
    """
    Add an impact_link connecting an event to an observation
    
    Parameters:
    -----------
    df : pd.DataFrame
        Existing dataset
    source_event_idx : int
        Index of source event record
    target_observation_idx : int
        Index of target observation record
    impact_direction : str
        'positive', 'negative', or 'neutral'
    confidence : str
        Confidence level
    metadata : Dict, optional
        Additional metadata
        
    Returns:
    --------
    pd.DataFrame
        Dataset with new impact_link added
    """
    # Validate indices
    if df.loc[source_event_idx, 'record_type'] != 'event':
        raise ValueError(f"Source index {source_event_idx} is not an event")
    if df.loc[target_observation_idx, 'record_type'] != 'observation':
        raise ValueError(f"Target index {target_observation_idx} is not an observation")
    
    new_record = {
        'record_type': 'impact_link',
        'source_event': source_event_idx,
        'target_observation': target_observation_idx,
        'impact_direction': impact_direction,
        'confidence': confidence
    }
    
    if metadata:
        new_record.update(metadata)
    
    # Ensure all columns exist
    for col in df.columns:
        if col not in new_record:
            new_record[col] = None
    
    new_df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    logger.info(f"Added impact_link: event {source_event_idx} -> observation {target_observation_idx} ({impact_direction})")
    
    return new_df


def save_enriched_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save enriched dataset to CSV
    
    Parameters:
    -----------
    df : pd.DataFrame
        Enriched dataset
    output_path : str
        Output file path
    """
    logger.info(f"Saving enriched data to {output_path}")
    df.to_csv(output_path, index=False)
    logger.info(f"Saved {len(df)} records")


def get_observations_by_pillar(df: pd.DataFrame, pillar: str) -> pd.DataFrame:
    """
    Get all observations for a specific pillar
    
    Parameters:
    -----------
    df : pd.DataFrame
        Unified dataset
    pillar : str
        'access' or 'usage'
        
    Returns:
    --------
    pd.DataFrame
        Filtered observations
    """
    obs = df[df['record_type'] == 'observation']
    return obs[obs['pillar'] == pillar].copy()


def get_events_by_year(df: pd.DataFrame, year: Optional[int] = None) -> pd.DataFrame:
    """
    Get events, optionally filtered by year
    
    Parameters:
    -----------
    df : pd.DataFrame
        Unified dataset
    year : int, optional
        Year to filter by
        
    Returns:
    --------
    pd.DataFrame
        Event records
    """
    events = df[df['record_type'] == 'event'].copy()
    if year is not None:
        events = events[events['year'] == year]
    return events


def get_impact_links_for_event(df: pd.DataFrame, event_idx: int) -> pd.DataFrame:
    """
    Get all impact links for a specific event
    
    Parameters:
    -----------
    df : pd.DataFrame
        Unified dataset
    event_idx : int
        Index of event record
        
    Returns:
    --------
    pd.DataFrame
        Impact link records
    """
    impact_links = df[df['record_type'] == 'impact_link'].copy()
    return impact_links[impact_links['source_event'] == event_idx]
