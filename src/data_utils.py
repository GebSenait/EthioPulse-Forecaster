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
        if df.empty or 'record_type' not in df.columns:
            if df.empty:
                logger.info("DataFrame is empty - skipping events validation")
            else:
                logger.warning("record_type column not found - skipping events validation")
            return True  # Return True if empty or column doesn't exist (can't validate)
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
        if df.empty or 'record_type' not in df.columns:
            if df.empty:
                logger.info("DataFrame is empty - skipping impact links validation")
            else:
                logger.warning("record_type column not found - skipping impact links validation")
            return True  # Return True if empty or column doesn't exist (can't validate)
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
    
    # Basic validations - use the validator's valid types list
    # All valid types: observation, event, impact_link, target, baseline, forecast
    valid_types = ['observation', 'event', 'impact_link', 'target', 'baseline', 'forecast']
    
    if 'record_type' in df.columns:
        # Check for truly invalid record types
        invalid = df[~df['record_type'].isin(valid_types)]
        if len(invalid) > 0:
            invalid_types = invalid['record_type'].unique().tolist()
            logger.warning(f"Found invalid record_type values: {invalid_types}")
            raise ValueError(f"Invalid record_type values in dataset: {invalid_types}")
    
    # Validate events are pillar-agnostic
    
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
        'by_record_type': df['record_type'].value_counts().to_dict() if 'record_type' in df.columns and len(df) > 0 else {},
        'by_pillar': df[df['record_type'] == 'observation']['pillar'].value_counts().to_dict() if 'record_type' in df.columns and 'pillar' in df.columns and len(df[df['record_type'] == 'observation']) > 0 else {},
        'by_source_type': df['source_type'].value_counts().to_dict() if 'source_type' in df.columns and len(df) > 0 else {},
        'by_confidence': df['confidence'].value_counts().to_dict() if 'confidence' in df.columns and len(df) > 0 else {},
        'year_range': {
            'min': int(df['year'].min()) if 'year' in df.columns and len(df) > 0 and df['year'].notna().any() else None,
            'max': int(df['year'].max()) if 'year' in df.columns and len(df) > 0 and df['year'].notna().any() else None
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


def load_data_points_guide(file_path: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    """
    Load the Additional Data Points Guide Excel file (all 4 sheets)
    
    Parameters:
    -----------
    file_path : str, optional
        Path to Additional Data Points Guide.xlsx
        If None, looks in data/raw/ directory
        
    Returns:
    --------
    Dict[str, pd.DataFrame]
        Dictionary with sheet names as keys and DataFrames as values
        Keys: 'A. Alternative Baselines', 'B. Direct Corrln', 'C. Indirect Corrln', 'D. Market Naunces'
    """
    if file_path is None:
        # Default path
        default_path = Path(__file__).parent.parent / "data" / "raw" / "Additional Data Points Guide.xlsx"
        file_path = str(default_path)
    
    logger.info(f"Loading Additional Data Points Guide from {file_path}")
    
    try:
        # Load all sheets
        sheets = {
            'A. Alternative Baselines': pd.read_excel(file_path, sheet_name='A. Alternative Baselines'),
            'B. Direct Corrln': pd.read_excel(file_path, sheet_name='B. Direct Corrln'),
            'C. Indirect Corrln': pd.read_excel(file_path, sheet_name='C. Indirect Corrln'),
            'D. Market Naunces': pd.read_excel(file_path, sheet_name='D. Market Naunces')
        }
        
        logger.info(f"Loaded {len(sheets)} sheets from guide")
        for sheet_name, df in sheets.items():
            logger.info(f"  - {sheet_name}: {len(df)} rows")
        
        return sheets
    except Exception as e:
        logger.warning(f"Could not load Additional Data Points Guide: {e}")
        return {}


def get_source_info(guide_sheets: Dict[str, pd.DataFrame], source_name: str) -> Optional[Dict]:
    """
    Get information about a specific data source from the guide
    
    Parameters:
    -----------
    guide_sheets : Dict[str, pd.DataFrame]
        Dictionary of guide sheets (from load_data_points_guide)
    source_name : str
        Name of source to search for (e.g., 'IMF', 'GSMA', 'ITU', 'NBE')
        
    Returns:
    --------
    Dict or None
        Source information including type, geographic scope, Ethiopia inclusion, highlights, link
    """
    if not guide_sheets:
        return None
    
    # Search in Alternative Baselines sheet (most likely location)
    if 'A. Alternative Baselines' in guide_sheets:
        df = guide_sheets['A. Alternative Baselines']
        
        # Try to find source by name (case-insensitive, partial match)
        # Check common column names
        name_col = None
        for col in df.columns:
            if 'survey' in col.lower() or 'source' in col.lower() or 'name' in col.lower() or df.columns[0] == col:
                name_col = col
                break
        
        if name_col:
            # Search for source
            mask = df[name_col].astype(str).str.contains(source_name, case=False, na=False)
            matches = df[mask]
            
            if len(matches) > 0:
                row = matches.iloc[0]
                info = {
                    'source_name': str(row[name_col]) if name_col in row else source_name,
                    'type': str(row.get('Type', '')) if 'Type' in row else '',
                    'geographic_scope': str(row.get('Geographic Scope', '')) if 'Geographic Scope' in row else '',
                    'ethiopia_included': str(row.get('Ethiopia Included?', '')) if 'Ethiopia Included?' in row else '',
                    'highlights': str(row.get('Highlights', '')) if 'Highlights' in row else '',
                    'link': str(row.get('Link to Data', '')) if 'Link to Data' in row else ''
                }
                return info
    
    return None


def list_available_sources(guide_sheets: Dict[str, pd.DataFrame], ethiopia_only: bool = True) -> pd.DataFrame:
    """
    List all available data sources from the guide
    
    Parameters:
    -----------
    guide_sheets : Dict[str, pd.DataFrame]
        Dictionary of guide sheets (from load_data_points_guide)
    ethiopia_only : bool
        If True, only return sources that include Ethiopia
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with available sources and their characteristics
    """
    if not guide_sheets or 'A. Alternative Baselines' not in guide_sheets:
        return pd.DataFrame()
    
    df = guide_sheets['A. Alternative Baselines'].copy()
    
    # Filter for Ethiopia if requested
    if ethiopia_only and 'Ethiopia Included?' in df.columns:
        df = df[df['Ethiopia Included?'].astype(str).str.contains('Yes', case=False, na=False)]
    
    return df
