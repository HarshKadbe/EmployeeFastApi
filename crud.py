from sqlalchemy.orm import Session
from uuid import UUID
import models, schema

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def create_employee(db:Session, employee:schema.EmployeeCreate):
    db_employee = models.Employee(name=employee.name, age=employee.age, email=employee.email)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id:UUID, employee: schema.EmployeeUpdate):
    db_employee=get_employee(db, employee_id)
    if db_employee:
        db_employee.name = employee.name
        db_employee.age = employee.age
        db_employee.email = employee.email
        db.commit()
        db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: UUID):
    db_employee = get_employee(db, employee_id)
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee