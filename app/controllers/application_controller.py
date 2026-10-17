from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.dependencies.dependency import get_current_user
from app.schema.application_schema import ApplicationInput

from app.services.application_service import (
    job_apply as job_apply_service
)

from app.exceptions.exception import (
    JobExpiredError,
    UserInactiveError,
    AuthorizationError,
    DuplicateApplicationError
)

from app.db.connection import get_db


router = APIRouter(
    prefix="/applications",
    tags=["applications"]
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESUME_DIR = PROJECT_ROOT / "uploads" / "resumes"

MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx"
}


if RESUME_DIR.exists() and not RESUME_DIR.is_dir():
    raise RuntimeError(
        f"Resume path exists but is not a directory: {RESUME_DIR}"
    )

RESUME_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/apply/me")
async def apply(
    job_id: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    saved_path = None

    try:
        # 1. Validate job_id using the existing Pydantic schema.
        try:
            payload = ApplicationInput.model_validate(
                {
                    "job_id": job_id
                }
            )
        except ValidationError as error:
            raise HTTPException(
                status_code=422,
                detail=error.errors(include_input=False)
            )

        # 2. Validate the resume extension.
        extension = Path(
            resume.filename or ""
        ).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="INVALID_RESUME_FORMAT"
            )

        # 3. Validate resume size.
        content = await resume.read(
            MAX_FILE_SIZE + 1
        )

        if not content:
            raise HTTPException(
                status_code=400,
                detail="EMPTY_RESUME"
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="RESUME_TOO_LARGE"
            )

        # 4. Save the resume using a unique filename.
        filename = f"{uuid4().hex}{extension}"

        saved_path = RESUME_DIR / filename

        with saved_path.open("xb") as file:
            file.write(content)

        resume_path = f"uploads/resumes/{filename}"

        # 5. Apply through the service.
        result = job_apply_service(
            db,
            user_id=current_user.user_id,
            job_id=payload.job_id,
            user_role=current_user.role,
            resume_path=resume_path
        )

        return result

    except DuplicateApplicationError as error:
        db.rollback()

        if saved_path and saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

    except AuthorizationError as error:
        db.rollback()

        if saved_path and saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=401,
            detail=error.msg
        )

    except UserInactiveError as error:
        db.rollback()

        if saved_path and saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=403,
            detail=str(error)
        )

    except JobExpiredError as error:
        db.rollback()

        if saved_path and saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=403,
            detail=str(error)
        )

    except IntegrityError as error:
        db.rollback()

        if saved_path and saved_path.exists():
            saved_path.unlink()

        # The unique constraint catches simultaneous duplicate requests.
        original_error = str(error.orig).lower()

        if (
            "uq_user_job_application" in original_error
            or "1062" in original_error
            or "duplicate entry" in original_error
        ):
            raise HTTPException(
                status_code=409,
                detail="You have already applied for this job."
            )

        raise HTTPException(
            status_code=409,
            detail="DATABASE_ERROR"
        )

    except HTTPException:
        db.rollback()

        if saved_path and saved_path.exists():
            saved_path.unlink()

        raise

    except Exception:
        db.rollback()

        if saved_path and saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="INTERNAL_SERVER_ERROR"
        )

    finally:
        await resume.close()