from utils.logger import get_logger

logger = get_logger(__name__)

def text_parser(text: str) -> str:
    """
    A simple text parser that can be extended with more complex logic.
    For now, it just normalizes whitespace and removes extra newlines.
    """
    import re
    # Normalize whitespace
    cleaned_text = re.sub(r'\s+', ' ', text).strip()
    # logger.info(f'Parsed text: {cleaned_text}')
    return cleaned_text