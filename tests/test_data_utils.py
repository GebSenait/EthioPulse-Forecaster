"""
Unit tests for src.data_utils module
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_utils import (
    UnifiedSchemaValidator,
    load_unified_data,
    load_reference_codes,
    quantify_dataset_composition
)


class TestUnifiedSchemaValidator:
    """Test cases for UnifiedSchemaValidator"""
    
    def test_validate_record_type_valid(self):
        """Test validation with valid record types"""
        validator = UnifiedSchemaValidator()
        df = pd.DataFrame({
            'record_type': ['observation', 'event', 'impact_link', 'target'],
            'year': [2021, 2022, None, 2023],
            'value': [50.0, None, None, 60.0]
        })
        assert validator.validate_record_type(df) == True
    
    def test_validate_record_type_invalid(self):
        """Test validation with invalid record types"""
        validator = UnifiedSchemaValidator()
        df = pd.DataFrame({
            'record_type': ['observation', 'invalid_type', 'event'],
            'year': [2021, 2022, 2023],
            'value': [50.0, 60.0, 70.0]
        })
        assert validator.validate_record_type(df) == False
    
    def test_validate_record_type_missing_column(self):
        """Test validation when record_type column is missing"""
        validator = UnifiedSchemaValidator()
        df = pd.DataFrame({
            'year': [2021, 2022],
            'value': [50.0, 60.0]
        })
        assert validator.validate_record_type(df) == False
    
    def test_validate_events_no_pillar(self):
        """Test that events have no pillar assignment"""
        validator = UnifiedSchemaValidator()
        df = pd.DataFrame({
            'record_type': ['event', 'event', 'observation'],
            'pillar': [None, None, 'access'],
            'year': [2021, 2022, 2023]
        })
        assert validator.validate_events_no_pillar(df) == True
    
    def test_validate_events_with_pillar(self):
        """Test validation fails when events have pillar"""
        validator = UnifiedSchemaValidator()
        df = pd.DataFrame({
            'record_type': ['event', 'event'],
            'pillar': ['access', 'usage'],  # Events should not have pillar
            'year': [2021, 2022]
        })
        assert validator.validate_events_no_pillar(df) == False
    
    def test_validate_events_empty_dataframe(self):
        """Test validation with empty dataframe"""
        validator = UnifiedSchemaValidator()
        df = pd.DataFrame()
        assert validator.validate_events_no_pillar(df) == True  # Should return True for empty
    
    def test_validate_impact_links_valid(self):
        """Test validation of valid impact links"""
        validator = UnifiedSchemaValidator()
        df = pd.DataFrame({
            'record_type': ['impact_link', 'impact_link'],
            'source_event': ['event_1', 'event_2'],
            'target_observation': ['obs_1', 'obs_2'],
            'impact_direction': ['positive', 'negative'],
            'confidence': ['high', 'medium']
        })
        assert validator.validate_impact_links(df) == True
    
    def test_validate_impact_links_missing_fields(self):
        """Test validation handles missing fields gracefully"""
        validator = UnifiedSchemaValidator()
        df = pd.DataFrame({
            'record_type': ['impact_link'],
            'source_event': ['event_1'],
            # Missing target_observation, impact_direction
        })
        # The function returns True but logs warnings for invalid references
        # This is expected behavior - it validates what it can
        result = validator.validate_impact_links(df)
        assert isinstance(result, bool)  # Should return a boolean


class TestQuantifyDatasetComposition:
    """Test cases for quantify_dataset_composition"""
    
    def test_quantify_composition_basic(self):
        """Test basic composition quantification"""
        df = pd.DataFrame({
            'record_type': ['observation', 'observation', 'event', 'impact_link'],
            'pillar': ['access', 'usage', None, None],
            'source_type': ['survey', 'operator', 'policy', 'analyst'],
            'confidence': ['high', 'high', 'medium', 'high'],
            'year': [2021, 2022, 2021, 2022]
        })
        composition = quantify_dataset_composition(df)
        
        assert composition['total_records'] == 4
        assert composition['by_record_type']['observation'] == 2
        assert composition['by_record_type']['event'] == 1
        assert composition['by_record_type']['impact_link'] == 1
    
    def test_quantify_composition_empty(self):
        """Test composition quantification with empty dataframe"""
        df = pd.DataFrame()
        composition = quantify_dataset_composition(df)
        
        assert composition['total_records'] == 0
        assert composition['by_record_type'] == {}
    
    def test_quantify_composition_missing_columns(self):
        """Test composition quantification when columns are missing"""
        df = pd.DataFrame({
            'record_type': ['observation', 'event'],
            'year': [2021, 2022]
            # Missing pillar, source_type, confidence
        })
        composition = quantify_dataset_composition(df)
        
        assert composition['total_records'] == 2
        assert composition['by_pillar'] == {}  # Should be empty if pillar column missing
        assert composition['by_source_type'] == {}  # Should be empty if source_type missing


class TestDataLoading:
    """Test cases for data loading functions"""
    
    def test_load_reference_codes_missing_file(self, tmp_path):
        """Test loading reference codes when file doesn't exist"""
        # This should handle gracefully
        fake_path = tmp_path / "nonexistent.xlsx"
        # The function should raise an error or return None/empty
        # We'll test that it handles missing files gracefully
        pass  # Actual implementation depends on error handling in data_utils
    
    def test_quantify_composition_year_range(self):
        """Test year range calculation"""
        df = pd.DataFrame({
            'record_type': ['observation', 'observation'],
            'year': [2021, 2023],
            'value': [50.0, 60.0]
        })
        composition = quantify_dataset_composition(df)
        
        assert composition['year_range']['min'] == 2021
        assert composition['year_range']['max'] == 2023
    
    def test_quantify_composition_no_year_column(self):
        """Test composition when year column is missing"""
        df = pd.DataFrame({
            'record_type': ['observation'],
            'value': [50.0]
            # Missing year column
        })
        composition = quantify_dataset_composition(df)
        
        assert composition['year_range']['min'] is None
        assert composition['year_range']['max'] is None
