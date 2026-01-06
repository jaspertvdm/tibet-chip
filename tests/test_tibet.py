"""
TIBET Safety Chip Tests
=======================

Tests for TIBET provenance and classification:
- DataTrail tracking
- Operation recording
- Threat classification
- TIBET token structure

Run: pytest tests/test_tibet.py -v
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tibet_chip.provenance import DataTrail, DataOperation, DataLocation


class TestDataTrail:
    """Test DataTrail provenance tracking."""

    def test_create_trail(self):
        """Test creating a data trail."""
        trail = DataTrail(
            data_id="test_001",
            content_hash="abc123"
        )
        assert trail.data_id == "test_001"
        assert trail.content_hash == "abc123"
        assert trail.operations == []

    def test_record_operation(self):
        """Test recording an operation."""
        trail = DataTrail(
            data_id="test_002",
            content_hash="def456"
        )

        token_id = trail.record_operation(
            operation=DataOperation.READ,
            actor="test_agent",
            location=DataLocation.MEMORY,
            details={"reason": "testing"}
        )

        assert token_id is not None
        assert len(trail.operations) == 1
        assert trail.operations[0]["operation"] == "read"
        assert trail.operations[0]["actor"] == "test_agent"

    def test_trail_chain(self):
        """Test that operations chain correctly."""
        trail = DataTrail(
            data_id="test_003",
            content_hash="ghi789"
        )

        # Record multiple operations
        trail.record_operation(DataOperation.READ, "agent1", DataLocation.DISK)
        trail.record_operation(DataOperation.TRANSFORM, "agent2", DataLocation.MEMORY)
        trail.record_operation(DataOperation.SEND, "agent3", DataLocation.NETWORK)

        assert len(trail.operations) == 3
        assert trail.current_location == DataLocation.NETWORK

    def test_tibet_structure_in_operation(self):
        """Test that operations contain TIBET structure."""
        trail = DataTrail(
            data_id="test_004",
            content_hash="jkl012"
        )

        trail.record_operation(
            operation=DataOperation.ANALYZE,
            actor="llm",
            location=DataLocation.LLM_CONTEXT
        )

        op = trail.operations[0]
        assert "tibet" in op
        assert "erin" in op["tibet"]
        assert "eromheen" in op["tibet"]
        assert "erachter" in op["tibet"]


class TestDataOperations:
    """Test DataOperation enum."""

    def test_all_operations_exist(self):
        """Test that expected operations exist."""
        expected = [
            "READ", "WRITE", "TRANSFORM", "SEND", "RECEIVE",
            "STORE", "DELETE", "COPY", "ANALYZE", "DISPLAY",
            "ENCRYPT", "DECRYPT"
        ]
        for op in expected:
            assert hasattr(DataOperation, op)

    def test_operation_values(self):
        """Test operation enum values."""
        assert DataOperation.READ.value == "read"
        assert DataOperation.TRANSFORM.value == "transform"
        assert DataOperation.SEND.value == "send"


class TestDataLocations:
    """Test DataLocation enum."""

    def test_all_locations_exist(self):
        """Test that expected locations exist."""
        expected = [
            "MEMORY", "DISK", "NETWORK", "BROWSER_TAB",
            "CLIPBOARD", "DATABASE", "API", "LLM_CONTEXT", "USER_DISPLAY"
        ]
        for loc in expected:
            assert hasattr(DataLocation, loc)


class TestTIBETToken:
    """Test TIBET token structure."""

    def test_tibet_has_four_dimensions(self):
        """Test that TIBET tokens have ERIN, ERAAN, EROMHEEN, ERACHTER."""
        trail = DataTrail(
            data_id="tibet_test",
            content_hash="tibet123"
        )

        trail.record_operation(
            operation=DataOperation.STORE,
            actor="root_ai",
            location=DataLocation.DATABASE,
            details={"table": "memories"}
        )

        tibet = trail.operations[0]["tibet"]

        # Check all four dimensions
        assert "erin" in tibet, "TIBET must have ERIN (what's IN)"
        assert "eromheen" in tibet, "TIBET must have EROMHEEN (what's AROUND)"
        assert "erachter" in tibet, "TIBET must have ERACHTER (what's BEHIND)"
        # eraan can be None for first operation
        assert "eraan" in tibet, "TIBET must have ERAAN (what's ATTACHED)"


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
