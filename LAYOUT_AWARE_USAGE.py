"""
Usage examples for layout-aware extraction and chunking.
"""

from src.ingestion.pipeline import RAGPipeline
from src.extractor.layout_analyzer import LayoutAnalyzer
from src.extractor.pdf.layout_aware_extractor import LayoutAwareExtractor
from src.chunking.layout_chunker import LayoutChunker


# Example 1: Using the pipeline with layout-aware mode
def example_pipeline_layout_aware():
    """Run pipeline with layout-aware extraction and chunking."""
    # Initialize pipeline with layout-aware mode
    pipeline = RAGPipeline(use_layout_aware=True)
    
    # Run the pipeline
    result = pipeline.run('path/to/document.pdf')
    
    # Result includes layout-specific metadata
    print(f"File: {result['file_path']}")
    print(f"Number of chunks: {result['num_chunks']}")
    print(f"Tables detected: {result.get('tables_detected', 0)}")
    print(f"Total pages: {result.get('num_pages', 0)}")
    print(f"Layout-aware: {result['layout_aware']}")


# Example 2: Direct layout analysis
def example_direct_layout_analysis():
    """Analyze PDF layout directly without running full pipeline."""
    analyzer = LayoutAnalyzer('path/to/document.pdf')
    
    # Analyze the PDF
    layout_pages = analyzer.analyze()
    
    # Access layout information
    for page in layout_pages:
        print(f"\nPage {page.page_num}:")
        print(f"  Dimensions: {page.page_width} x {page.page_height}")
        
        for element in page.elements:
            print(f"  - [{element.type}] {element.content[:50]}...")
            print(f"    Hierarchy: {element.hierarchy_level}")
            print(f"    Position: {element.bbox}")
            if element.type == 'table':
                print(f"    (Table with content)")
    
    # Get structured text preserving hierarchy
    structured_text = analyzer.get_structural_text(preserve_hierarchy=True)
    print("\nStructured Text:\n", structured_text[:500])


# Example 3: Layout-aware extraction
def example_layout_aware_extraction():
    """Extract text using layout awareness."""
    extractor = LayoutAwareExtractor('path/to/document.pdf', preserve_layout=True)
    
    # Extract text with layout preservation
    text = extractor.extract()
    print("Extracted text with layout:")
    print(text[:500])
    
    # Access layout pages for further analysis
    layout_pages = extractor.get_layout_pages()
    print(f"\nTotal pages: {len(layout_pages)}")


# Example 4: Custom layout chunking
def example_custom_layout_chunking():
    """Chunk text with custom layout-aware settings."""
    chunker = LayoutChunker(
        chunk_size=1500,          # Larger chunks
        chunk_overlap=200,        # More context
        respect_hierarchy=True,   # Respect document structure
        min_chunk_size=150,       # Minimum chunk size
    )
    
    # Read some text
    with open('path/to/extracted_text.txt', 'r') as f:
        text = f.read()
    
    # Chunk the text
    chunks = chunker.chunk(text, metadata={'source': 'document.pdf'})
    
    # Access chunk information
    for chunk in chunks:
        print(f"\nChunk {chunk.chunk_id}:")
        print(f"  Content length: {len(chunk.content)}")
        print(f"  Hierarchy level: {chunk.hierarchy_level}")
        print(f"  Source type: {chunk.source_type}")
        if chunk.metadata:
            print(f"  Metadata: {chunk.metadata}")
        print(f"  Content preview: {chunk.content[:100]}...")


# Example 5: Comparison - layout-aware vs semantic
def example_comparison():
    """Compare layout-aware vs traditional semantic chunking."""
    file_path = 'path/to/document.pdf'
    
    # Layout-aware pipeline
    layout_pipeline = RAGPipeline(use_layout_aware=True)
    layout_result = layout_pipeline.run(file_path)
    
    # Traditional semantic pipeline
    semantic_pipeline = RAGPipeline(use_layout_aware=False)
    semantic_result = semantic_pipeline.run(file_path)
    
    # Compare results
    print("Comparison:")
    print(f"Layout-aware chunks: {layout_result['num_chunks']}")
    print(f"Semantic chunks: {semantic_result['num_chunks']}")
    if 'tables_detected' in layout_result:
        print(f"Tables detected (layout-aware): {layout_result['tables_detected']}")


# Example 6: Using layout analyzer with custom chunking
def example_analyzer_with_custom_chunking():
    """Use layout analyzer results with custom chunking strategy."""
    # Analyze layout
    analyzer = LayoutAnalyzer('path/to/document.pdf')
    layout_pages = analyzer.analyze()
    
    # Create chunker
    chunker = LayoutChunker(chunk_size=1000, chunk_overlap=100)
    
    # Extract layout elements
    all_elements = []
    for page in layout_pages:
        all_elements.extend(page.elements)
    
    # Chunk using layout awareness
    if layout_pages:
        page = layout_pages[0]  # Use first page as example
        chunks = chunker.chunk_with_layout(
            all_elements,
            page_width=page.page_width,
            page_height=page.page_height,
        )
        
        # Access chunks with layout metadata
        for chunk in chunks:
            print(f"\nLayout Chunk {chunk.chunk_id}:")
            print(f"  Type: {chunk.source_type}")
            print(f"  Page: {chunk.page_num}")
            if chunk.metadata:
                bbox = chunk.metadata.get('bbox')
                print(f"  Position: {bbox}")


if __name__ == '__main__':
    print("Layout-Aware Extraction and Chunking Examples")
    print("=" * 50)
    
    # Uncomment to run examples:
    # example_pipeline_layout_aware()
    # example_direct_layout_analysis()
    # example_layout_aware_extraction()
    # example_custom_layout_chunking()
    # example_comparison()
    # example_analyzer_with_custom_chunking()
