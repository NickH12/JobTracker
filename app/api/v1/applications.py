from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_user
from app.models.enums import ApplicationStatus
from app.models.user import User    
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import crud_application

router = APIRouter()


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationCreate,
                       current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)
):
    application = crud_application.create_application(db, application, current_user.id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return application


@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_application(application_id: int,
                       application_update: ApplicationUpdate,
                       current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)
):
    application = crud_application.update_application(db, application_id, application_update, current_user.id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application

@router.get("/", response_model=list[ApplicationResponse])
def get_applications(current_user: User = Depends(get_current_user),
                     db: Session = Depends(get_db),
                     status: ApplicationStatus | None = None,
                     company_id: int | None = None,
                     search: str | None = None
):
    return crud_application.get_applications_by_user_id(db, current_user.id, status, company_id, search)

@router.get("/stats")
def get_application_stats(current_user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    
    return crud_application.get_application_stats(db, current_user.id)

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)
):
    application = crud_application.get_application_by_id(db, application_id, current_user.id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int,
                       current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)
):
    success = crud_application.delete_application(db, application_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return None

