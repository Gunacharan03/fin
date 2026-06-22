"""
Validation helpers shared by routes/services.
"""
from fastapi import HTTPException, status
from bson import ObjectId


def validate_object_id(id_str: str, resource_name: str = "Resource") -> ObjectId:
    """Raise 400 if id_str isn't a valid Mongo ObjectId, else return ObjectId."""
    if not ObjectId.is_valid(id_str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {resource_name} ID format",
        )
    return ObjectId(id_str)


def validate_file_extension(filename: str, allowed: set = None) -> str:
    allowed = allowed or {"csv", "xlsx", "xls"}
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '.{ext}'. Allowed: {', '.join(allowed)}",
        )
    return ext


def ensure_owner(resource_user_id: str, current_user_id: str):
    """Raise 403 if the resource doesn't belong to the requesting user."""
    if str(resource_user_id) != str(current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
