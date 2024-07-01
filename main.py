from fastapi import FastAPI, HTTPException, Depends
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import schema, crud
import models
from uuid import UUID

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/employees/", response_model=list[schema.Employee])
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees

@app.get("/employees/{employee_id}", response_model=schema.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    print(employee_id, db_employee)
    print(f"Employee ID: {employee_id}, DB Employee: {db_employee}") 

    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@app.post("/createmployee/", response_model=schema.Employee)
def create_employees(employee:schema.EmployeeCreate, db:Session=Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)

@app.put("/updateemployees/{employee_id}", response_model=schema.Employee)
def update_employee(employee_id:int, employee: schema.EmployeeUpdate, db: Session=Depends(get_db)):
    db_employee = crud.update_employee(db, employee_id=employee_id, employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@app.delete("/employees/{employee_id}", response_model=schema.Employee)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.delete_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee