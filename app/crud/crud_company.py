from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import CompanyCreate


def create_company(db: Session, company: CompanyCreate, user_id: int) -> Company:
    db_company = Company(
        user_id=user_id,
        name=company.name,
        website=company.website,
        notes=company.notes
    )
    db.add(db_company)
    db.commit() 
    db.refresh(db_company)
    return db_company

def get_companies_by_user_id(db: Session, user_id: int) -> list[Company]:
    return db.query(Company).filter(Company.user_id == user_id).all()

def get_company_by_id(db: Session, company_id: int, user_id: int) -> Company | None:
    return db.query(Company).filter(Company.id == company_id,
                                    Company.user_id == user_id).first()

def update_company(db: Session, company_id: int, company_update: CompanyCreate, user_id: int) -> Company | None:
    company = get_company_by_id(db, company_id, user_id)
    if not company:
        return None
    company.name = company_update.name
    company.website = company_update.website
    company.notes = company_update.notes
    db.commit()
    db.refresh(company)
    return company

def delete_company(db: Session, company_id: int, user_id: int) -> bool:
    company = get_company_by_id(db, company_id, user_id)
    if not company:
        return False
    db.delete(company)
    db.commit()
    return True