"""
CSV upload routes — upload a bank statement, preview parsed transactions,
then confirm to save them.
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from app.auth.jwt_handler import get_current_user
from app.utils.validators import validate_file_extension
from app.services.csv_service import parse_bank_statement_csv, save_transactions
from app.config.settings import settings

router = APIRouter(prefix="/api/csv", tags=["CSV Upload"])


@router.post("/preview")
async def preview_csv(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Parses the uploaded file and returns transactions WITHOUT saving them."""
    validate_file_extension(file.filename, {"csv", "xlsx", "xls"})

    file_bytes = await file.read()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large ({size_mb:.1f}MB). Max allowed: {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    try:
        transactions = parse_bank_statement_csv(file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid transactions could be parsed from this file",
        )

    return {
        "preview_count": len(transactions),
        "transactions": transactions,
    }


@router.post("/confirm")
async def confirm_csv_import(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Parses AND saves the uploaded file's transactions in one step."""
    validate_file_extension(file.filename, {"csv", "xlsx", "xls"})
    file_bytes = await file.read()

    try:
        transactions = parse_bank_statement_csv(file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    saved_count = await save_transactions(str(current_user["_id"]), transactions)
    return {"message": f"Successfully imported {saved_count} transactions", "imported_count": saved_count}
