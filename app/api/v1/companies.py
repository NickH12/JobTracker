#api router
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_user
from app.models.user import User

from app.schemas.company import CompanyResponse

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.company import CompanyCreate
from app.crud import crud_company

router = APIRouter()

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(company: CompanyCreate,
                   current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)
):
    return crud_company.create_company(db, company, current_user.id)

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int,
                   company_update: CompanyCreate,
                   current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)
):
    company = crud_company.update_company(db, company_id, company_update, current_user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company

@router.get("/", response_model=list[CompanyResponse])
def get_companies(current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)
):
    return crud_company.get_companies_by_user_id(db, current_user.id)

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)
):
    company = crud_company.get_company_by_id(db, company_id, current_user.id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int,
                   current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)
):
    success = crud_company.delete_company(db, company_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return None