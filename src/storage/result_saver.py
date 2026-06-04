import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from utils.logger import get_logger

logger = get_logger(__name__)


class ResultSaver:
    """Utility to save extraction results to JSON files with timestamps."""

    def __init__(self, output_dir: str = 'data/processed'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _serialize_chunk(chunk: Any) -> Dict[str, Any]:
        """Convert a Chunk object to a dictionary for JSON serialization."""
        if hasattr(chunk, '__dict__'):
            # If it's a dataclass or object with __dict__
            chunk_dict = chunk.__dict__.copy()
            # Handle metadata dict
            if 'metadata' in chunk_dict and chunk_dict['metadata']:
                chunk_dict['metadata'] = chunk_dict['metadata'].copy()
            return chunk_dict
        else:
            # Fallback - try to convert to string
            return {'content': str(chunk)}

    def _prepare_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare result for JSON serialization by converting Chunk objects."""
        prepared = result.copy()

        # Convert chunks if present
        if 'chunks' in prepared and isinstance(prepared['chunks'], list):
            prepared['chunks'] = [
                self._serialize_chunk(chunk) for chunk in prepared['chunks']
            ]

        return prepared

    def save_result(
        self,
        result: Dict[str, Any],
        pdf_name: Optional[str] = None,
        include_chunks: bool = True,
    ) -> str:
        """
        Save extraction result to JSON file.
        
        Args:
            result: Dictionary containing extraction results
            pdf_name: Name of PDF (extracted from result if not provided)
            include_chunks: Whether to include chunk details in output
            
        Returns:
            Path to saved JSON file
        """
        if pdf_name is None:
            file_path = result.get('file_path', '')
            pdf_name = Path(file_path).stem if file_path else 'unknown'

        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{pdf_name}_{timestamp}.json'
        filepath = self.output_dir / filename

        # Prepare result for JSON serialization
        prepared_result = self._prepare_result(result)

        # Remove chunks if not included
        if not include_chunks and 'chunks' in prepared_result:
            prepared_result.pop('chunks')

        # Prepare output data
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'pdf_name': pdf_name,
            'extraction_results': prepared_result,
        }

        # Save to JSON
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)

        logger.info(f'Results saved to: {filepath}')
        return str(filepath)

    def save_results_batch(
        self,
        results: list,
        include_chunks: bool = True,
    ) -> list:
        """
        Save multiple extraction results to JSON files.
        
        Args:
            results: List of extraction result dictionaries
            include_chunks: Whether to include chunk details in output
            
        Returns:
            List of paths to saved JSON files
        """
        saved_paths = []
        for result in results:
            path = self.save_result(result, include_chunks=include_chunks)
            saved_paths.append(path)

        return saved_paths

    def save_combined_results(
        self,
        results: list,
        batch_name: Optional[str] = None,
    ) -> str:
        """
        Save all results in a single combined JSON file.
        
        Args:
            results: List of extraction result dictionaries
            batch_name: Name for the batch (defaults to timestamp)
            
        Returns:
            Path to saved JSON file
        """
        if batch_name is None:
            batch_name = 'batch'

        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{batch_name}_{timestamp}.json'
        filepath = self.output_dir / filename

        # Prepare output data
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'batch_name': batch_name,
            'total_files': len(results),
            'results': results,
        }

        # Save to JSON
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)

        logger.info(f'Combined results saved to: {filepath}')
        return str(filepath)
