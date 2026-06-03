class TextValidator:
    def is_valid(self, text: str) -> bool:
        return bool(text and len(text.strip()) >= 50)

    def clean(self, text: str) -> str:
        return ' '.join(text.split()) if text else ''
