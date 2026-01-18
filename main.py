from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db, engine, Base
from models import Term
from schemas import TermCreate, TermUpdate, TermResponse

# Создание таблиц при запуске приложения
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WebGL/WebGPU Glossary API",
    description="REST API для управления глоссарием терминов WebGL/WebGPU",
    version="1.0.0",
)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "WebGL/WebGPU Glossary API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/terms", response_model=List[TermResponse], tags=["Terms"])
def get_all_terms(db: Session = Depends(get_db)):
    """Получение списка всех терминов"""
    terms = db.query(Term).all()
    return terms


@app.get("/terms/{keyword}", response_model=TermResponse, tags=["Terms"])
def get_term_by_keyword(keyword: str, db: Session = Depends(get_db)):
    """Получение термина по ключевому слову"""
    term = db.query(Term).filter(Term.keyword == keyword).first()
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Термин с ключевым словом '{keyword}' не найден"
        )
    return term


@app.post("/terms", response_model=TermResponse, status_code=status.HTTP_201_CREATED, tags=["Terms"])
def create_term(term_data: TermCreate, db: Session = Depends(get_db)):
    """Создание нового термина"""
    # Проверка на существование термина с таким же keyword
    existing_term = db.query(Term).filter(Term.keyword == term_data.keyword).first()
    if existing_term:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Термин с ключевым словом '{term_data.keyword}' уже существует"
        )
    
    new_term = Term(keyword=term_data.keyword, description=term_data.description)
    db.add(new_term)
    db.commit()
    db.refresh(new_term)
    return new_term


@app.put("/terms/{keyword}", response_model=TermResponse, tags=["Terms"])
def update_term(keyword: str, term_data: TermUpdate, db: Session = Depends(get_db)):
    """Обновление существующего термина"""
    term = db.query(Term).filter(Term.keyword == keyword).first()
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Термин с ключевым словом '{keyword}' не найден"
        )
    
    # Если обновляется keyword, проверяем уникальность
    if term_data.keyword and term_data.keyword != keyword:
        existing_term = db.query(Term).filter(Term.keyword == term_data.keyword).first()
        if existing_term:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Термин с ключевым словом '{term_data.keyword}' уже существует"
            )
    
    # Обновление полей
    if term_data.keyword is not None:
        term.keyword = term_data.keyword
    if term_data.description is not None:
        term.description = term_data.description
    
    term.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(term)
    return term


@app.delete("/terms/{keyword}", status_code=status.HTTP_204_NO_CONTENT, tags=["Terms"])
def delete_term(keyword: str, db: Session = Depends(get_db)):
    """Удаление термина из глоссария"""
    term = db.query(Term).filter(Term.keyword == keyword).first()
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Термин с ключевым словом '{keyword}' не найден"
        )
    
    db.delete(term)
    db.commit()
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

