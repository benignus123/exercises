from fastapi import APIRouter, Depends, HTTPException
from database import sync_engine, Base,  get_session
from classes import Categories, Exercises, Exercises_Users, UserExerciseCreate, Users, UserExerciseStatsCreate, Exercise_Stats
from depend import get_current_user
from sqlalchemy import or_
router = APIRouter()

one = ['Грудь', 'Спина', 'Плечи', 'Руки', 'Ноги', 'Пресс']
default_exercises = {
    'Грудь': [
        'Жим от груди вверх сидя в рычажном тренажере',
        'Жим от груди сидя в рычажном тренажере', 
        'Приведение плеча в блочном тренажере "Бабочка"',
        'Приведение плеча в блочном тренажере "Пек - Дек"',
        'Жим от груди широким хватом сидя в рычажном тренажере',
        'Жим от груди сидя в блочном тренажере',
        'Отжимания в тренажере Гравитрон',
        'Жим от груди в тренажере Смита',
        'Жим узким хватом в тренажере Смита',
        'Сведение на грудные мышцы в кроссовере',
        'Сгибание плеча стоя',
        'Жим от груди стоя'
    ],
    'Спина': [
        'Горизонтальная тяга тросовая в блочном тренажере',
        'Вертикальная тяга с раздельными рукоятями и упором в блочном тренажере',
        'Горизонтальная тяга нижняя в рычажном тренажере',
        'Вертикальная тяга в рычажном тренажере',
        'Горизонтальная тяга в рычажном тренажере',
        'Разгибание спины сидя в блочном тренажере',
        'Вертикальная тяга сидя',
        'Горизонтальная тяга с упором на верхнюю часть спины',
        'Горизонтальная тяга с упором сидя в блочном тренажере',
        'Экстензия на наклонной скамье с акцентом на спину',
        'Кроссовер: Пуловер',
        'Кроссовер: Тяга к поясу стоя',
        'Тяга Т-грифа с упором в рычажном тренажере',
        'Подтягивание в тренажере Гравитрон',
        'Тяга в Мультистанции',
        'Вертикальная тяга тросовая сидя в блочном тренажере'
    ],
    'Плечи': [
        'Жим от плеч сидя в рычажном тренажере',
        'Отведение плеча в блочном тренажере "Пек - Дек"',
        'Кроссовер: Тяга к подбородку',
        'Кроссовер: Лицевая тяга с канатной рукоятью',
        'Кроссовер: Отведение плеча',
        'Жим от плеч в блочном тренажере',
        'Отведение плеча сидя в блочном тренажере',
        'Отведение плеча в горизонтальной плоскости в блочном тренажере',
        'Вертикальный жим в тренажере Смита',
        'Сгибание плеча стоя',
        'Жим от плеч стоя'
    ],
    'Руки': [
        'Сгибание на бицепс в рычажном тренажере',
        'Сгибание на бицепс сидя в блочном тренажере',
        'Разгибание на трицепс сидя в блочном тренажере',
        'Жим на брусьях сидя в рычажном тренажере',
        'Кроссовер: Разгибание на трицепс с V-образной рукоятью',
        'Кроссовер: Разгибание на трицепс с канатной рукоятью',
        'Кроссовер: Сгибание на бицепс с V-образной рукоятью',
        'Кроссовер: Сгибание "Молото" с канатной рукоятью',
        'Отжимания в тренажере Гравитрон',
        'Жим узким хватом в тренажере Смита'
    ],
    'Ноги': [
        'Жим ногами в горизонтальный в блочном тренажере',
        'Приведение бедра сидя в сдвоенном блочном тренажере',
        'Сгибание голени лежа в блочном тренажере',
        'Сгибание голени сидя в блочном тренажере',
        'Разгибание голени сидя в блочном тренажере',
        'Разгибание голени сидя в рычажном тренажере',
        'Сгибание голени стоя в рычажном тренажере',
        'Жим ногами',
        'Жим ногами в рычажном тренажере',
        'Маятниковый присед',
        'Силовый присед в рычажном тренажере',
        'Приседание в тренажере Смита',
        'Выпады в тренажере Смита',
        'Становая тяга сумо в тренажере Смита',
        'Румынская тяга в тренажере Смита',
        'Приведение бедра стоя в тренажере Multi Hip',
        'Сгибание бедра стоя в тренажере Multi Hip',
        'Разгибание бедра стоя в тренажере Multi Hip',
        'Приведение бедра сидя в блочном тренажере'
    ],
    'Пресс': [
        'Скручивание на пресс сидя в блочном тренажере',
        'Скручивание на пресс в тренажере Panatta',
        'Вращение стоя в Мультистанции',
    ]   
}

# добавить группу
@router.post('/group', tags=['Группы'], summary='Добавить группу')
def add_group(session = Depends(get_session)):
    for ones in one:
        category = Categories(
            name = ones
        )
        session.add(category)
    session.commit()
    return {True}

# Добавить стандартное упражнение 
@router.post('/add_exercises', tags=['Упражнения'], summary='Добавить упражнения')
def add_exercises(session = Depends(get_session)):
    
    for category_name, exercise_list in default_exercises.items():

        category = session.query(Categories).filter(
            Categories.name == category_name,
            Categories.is_default == True
        ).first()
        
        if not category:
            category = Categories(
                name=category_name,
                is_default=True,
                user_id=None
            )
            session.add(category)
            session.flush()
        
        # Создаем стандартные упражнения
        for exercise_name in exercise_list:
            exercise = session.query(Exercises).filter(
                Exercises.name == exercise_name,
                Exercises.category_id == category.id,
                Exercises.is_default == True
            ).first()
            
            if not exercise:
                exercise = Exercises(
                    name=exercise_name,
                    category_id=category.id,
                    is_default=True,
                    user_id=None,
                    image_filename="default_exercise.jpg"
                )
                session.add(exercise)
    
    session.commit()
    
    return {"success": True, "message": "Стандартные упражнения добавлены"}

# Добавить кастомное упражнение
@router.post("/add-custom-exercise/", tags=['Упражнения'], summary='Добавить кастомное упражнение')
def add_custom_exercise(
    exercise_data: UserExerciseCreate,
    session = Depends(get_session),
    current_user: Users = Depends(get_current_user)
):
    
    category = session.query(Categories).filter(
        Categories.name == exercise_data.category_name
    ).filter(
        (Categories.user_id == current_user.id) |  
        (Categories.is_default == True)            
    ).first()
    
    if not category:
        category = Categories(
            name=exercise_data.category_name,
            is_default=False,
            user_id=current_user.id
        )
        session.add(category)
        session.flush()
    
    existing_exercise = session.query(Exercises).filter(
        Exercises.name == exercise_data.exercise_name,
        Exercises.category_id == category.id,
        Exercises.user_id == current_user.id
    ).first()
    
    if existing_exercise:
        raise HTTPException(
            status_code=400,
            detail="У вас уже есть такое упражнение"
        )
    
    new_exercise = Exercises(
        name=exercise_data.exercise_name,
        category_id=category.id,
        is_default=False,
        user_id=current_user.id,
        image_filename=exercise_data.image_filename
    )
    session.add(new_exercise)
    session.flush()
    
    user_exercise = Exercises_Users(
        user_id=current_user.id,
        exercise_id=new_exercise.id,
        notes="Мое упражнение"
    )
    session.add(user_exercise)
    
    session.commit()
    
    return {
        "success": True,
        "message": "Пользовательское упражнение добавлено",
        "data": {
            "exercise_id": new_exercise.id,
            "exercise_name": new_exercise.name,
            "category_name": category.name,
            "is_custom": True
        }
    }
    
# Получить упражнения
@router.get('/get_exercises', tags=['Упражнения'], summary='Получить упражнения')
def get_exercises(
    session = Depends(get_session),
    current_user = Depends(get_current_user)):
    
    exercises = session.query(Exercises).filter(
        or_(
            Exercises.is_default == True,
            Exercises.user_id == current_user.id
        )).all()
    
    result = []
    for exercise in exercises:
        result.append({
            'id': exercise.id,
            'name': exercise.name,
            'category_name': exercise.category.name,
            'is_default': exercise.is_default
            })
    
    return (result)

# Удалить упражнение   
@router.delete('/delete_exercise/{exercise_id}', tags=['Упражнения'], summary='Удалить упражнение')
def delete_exercise(
    exercise_id: int,
    session = Depends(get_session),
    current_user = Depends(get_current_user)):
    
    user_exercise = session.query(Exercises_Users).filter(
        Exercises_Users.exercise_id == exercise_id,
        Exercises_Users.user_id == current_user.id
    ).first()
    
    if not user_exercise:
        raise HTTPException(
            status_code=404, 
            detail="Упражнение не найдено или не принадлежит вам"
        )
    
    exercise = session.query(Exercises).filter(
        Exercises.id == exercise_id,
        Exercises.is_default == False 
    ).first()
    
    if not exercise:
        raise HTTPException(status_code=404, detail="Упражнение не найдено")


    session.query(Exercises_Users).filter(
        Exercises_Users.exercise_id == exercise_id
    ).delete()
    
    session.delete(exercise)
    session.commit()
    
    return {
        "success": True,
        "message": f"Упражнение успешно удалено"
    }
    
# Добавить статистику
@router.post('/add_statistics', tags=['Статистика'], summary='Добавить статистику')
def add_statistics(
    stats_data: UserExerciseStatsCreate,
    session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    
    exercise = session.query(Exercises).filter(
        Exercises.id == stats_data.exercise_id
    ).first()
    
    if not exercise:
        raise HTTPException(status_code=404, detail="Упражнение не найдено")
    
    if not exercise.is_default and exercise.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Это упражнение вам не доступно")
    
    stats = Exercise_Stats(
        user_id=current_user.id,
        exercise_id=stats_data.exercise_id,
        date=stats_data.date,
        weight=stats_data.weight,
        approach=stats_data.approach
    )
    
    session.add(stats)
    session.commit()
    
    session.refresh(stats)
    
    return {
        "success": True,
        "message": "Статистика добавлена",
        "data": {
            "id": stats.id,
            "exercise_name": exercise.name,
            "date": stats.date.isoformat(),
            "weight": stats.weight,
            "approach": stats.approach
        }
    }

# Получить статистику
@router.get('/get_stats', tags=['Статистика'], summary='Получить статистику')
def get_stats(
    session = Depends(get_session),
    current_user = Depends(get_current_user)
):

    stats = session.query(Exercise_Stats).filter(
        Exercise_Stats.user_id == current_user.id
    ).order_by(Exercise_Stats.date.desc()).all()
    
    result = []
    for stat in stats:
        exercise = session.query(Exercises).filter(Exercises.id == stat.exercise_id).first()
        result.append({
            "id": stat.id,
            "exercise_id": stat.exercise_id,
            "exercise_name": exercise.name if exercise else "Упражнение удалено",
            "date": stat.date.isoformat(),
            "weight": stat.weight,
            "approach": stat.approach
        })
    
    return result

# Удалить статистику
@router.delete('/delete_stats/{exercise_id}', tags=['Статистика'], summary='Удалить статистику')
def delete_stats(
    stats_id: int,
    session = Depends(get_session),
    current_user = Depends(get_current_user)):
    
    
    stats = session.query(Exercise_Stats).filter(
        Exercise_Stats.id == stats_id,
        Exercise_Stats.user_id == current_user.id
    ).first()
    
    if not stats:
        raise HTTPException(
            status_code=404, 
            detail="Упражнение не найдено или не принадлежит вам"
        )
    
    session.delete(stats)
    session.commit()
    
    return {
        "success": True,
        "message": f"Статистика успешно удалена"
    }
    
# Обновить описание упражнения
@router.put('/update_exercise_description/{exercise_id}', tags=['Упражнения'], summary='Обновить описание упражнения')
def update_exercise_description(
    exercise_id: int,
    request: dict, 
    session = Depends(get_session),
    current_user = Depends(get_current_user)
):

    exercise = session.query(Exercises).filter(
        Exercises.id == exercise_id,
        Exercises.is_default == False, 
        Exercises.user_id == current_user.id  
    ).first()
    
    if not exercise:
        raise HTTPException(
            status_code=404, 
            detail="Упражнение не найдено или не принадлежит вам"
        )
    

    new_description = request.get('description', '')
    exercise.description = new_description
    
    session.commit()
    
    return {
        "success": True,
        "message": "Описание успешно обновлено",
        "data": {
            "exercise_id": exercise.id,
            "description": exercise.description
        }
    }


@router.post('/setup_database', tags=['Создание бд'], summary='Создание бд')
def create_tables():
    sync_engine.echo = True
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True