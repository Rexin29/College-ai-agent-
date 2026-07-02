from pathlib import Path
from .config import Config
from .logger import logger


def validate_file_extension(filename: str) -> bool:
    """Validate if file extension is allowed"""
    file_ext = Path(filename).suffix.lower().lstrip(".")
    is_valid = file_ext in Config.ALLOWED_EXTENSIONS
    if not is_valid:
        logger.warning(f"Invalid file extension: {file_ext}")
    return is_valid


def validate_file_size(file_size_bytes: int) -> bool:
    """Validate if file size is within limit"""
    max_size_bytes = Config.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    is_valid = file_size_bytes <= max_size_bytes
    if not is_valid:
        logger.warning(
            f"File size {file_size_bytes} exceeds limit {max_size_bytes}"
        )
    return is_valid


def validate_metadata(metadata: dict) -> bool:
    """Validate document metadata"""
    required_fields = ["file_name"]
    return all(field in metadata for field in required_fields)
