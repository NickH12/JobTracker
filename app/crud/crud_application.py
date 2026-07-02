from sqlalchemy.orm import Session
from app.models.application import Application
from app.models.company import Company
from app.models.enums import ApplicationStatus
from app.schemas.application import ApplicationCreate, ApplicationStatResponse, ApplicationUpdate

def create_application(db: Session, application: ApplicationCreate, user_id: int) -> Application | None:
    #query for company first if exists

    company = db.query(Company).filter(Company.id == application.company_id,
                                    Company.user_id == user_id).first()
    if not company:
        return None

    db_application = Application(
            user_id=user_id,
            company_id=application.company_id,
            position=application.position,
            status=application.status,
            job_url=application.job_url,
            notes=application.notes,
            applied_at=application.applied_at
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_application_by_id(db: Session, application_id: int, user_id: int) -> Application | None:

    return db.query(Application).filter(Application.id == application_id,
                                        Application.user_id == user_id).first()

def get_applications_by_user_id(db: Session,
                                user_id: int,
                                status: ApplicationStatus | None = None,
                                company_id: int | None = None,
                                search: str | None = None) -> list[Application]:

    query = db.query(Application).filter(Application.user_id == user_id)

    if status is not None:
        query = query.filter(Application.status == status)
    if company_id is not None:
        query = query.filter(Application.company_id == company_id)
    if search is not None:
        query = query.filter(Application.position.ilike(f"%{search}%"))

    return query.order_by(Application.created_at.desc()).all()

def update_application(db: Session, application_id: int, application_update: ApplicationUpdate, user_id: int) -> Application | None:
    application = get_application_by_id(db, application_id, user_id)
    if not application:
        return None
    
    update_data = application_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application

def delete_application(db: Session, application_id: int, user_id: int) -> bool:
    db_application = get_application_by_id(db,application_id, user_id)
    if not db_application:
        return False
    db.delete(db_application)
    db.commit()
    return True

def get_application_stats(db: Session, user_id: int) -> ApplicationStatResponse:
    applications = get_applications_by_user_id(db, user_id)

    counts = {status.value: 0 for status in ApplicationStatus}

    for app in applications:
        counts[app.status.value] += 1

    return ApplicationStatResponse(
        total=len(applications),
        **counts
    )
