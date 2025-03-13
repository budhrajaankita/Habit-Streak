from datetime import datetime
import os
from sqlalchemy.orm import Session
from sqlalchemy import func, Column, Integer, String, DateTime, ForeignKey
from database import get_db, Base, engine
from typing import Generator, Optional, List, Dict, Any
import functools

# Update Habit model to include user_id
class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    habit_name = Column(String, index=True)
    created_date = Column(DateTime, default=datetime.now)
    target_frequency = Column(String)
    check_ins = Column(String, default="")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

class HabitTracker:
    def __init__(self, user_id: Optional[int] = None):
        self.db: Generator[Session, None, None] = get_db()
        self.session = next(self.db)
        self._habits_cache = {}
        self._last_cache_update = None
        self.user_id = user_id

    def _get_habit(self, habit_name: str):
        """Get habit with caching"""
        cache_key = f"{self.user_id}_{habit_name}"
        if cache_key not in self._habits_cache:
            self._habits_cache[cache_key] = self.session.query(Habit).filter(
                Habit.habit_name == habit_name,
                Habit.user_id == self.user_id
            ).first()
        return self._habits_cache[cache_key]

    def _clear_cache(self):
        """Clear the habits cache"""
        self._habits_cache.clear()
        self._last_cache_update = None

    def load_habits(self) -> List[Dict[str, Any]]:
        """Load habits from database with caching"""
        if not self.user_id:
            return []
            
        current_time = datetime.now()
        if self._last_cache_update is None or (current_time - self._last_cache_update).seconds > 300:
            habits = self.session.query(Habit).filter(Habit.user_id == self.user_id).all()
            self._habits_cache = {f"{self.user_id}_{habit.habit_name}": habit for habit in habits}
            self._last_cache_update = current_time
        
        return [{
            'habit_name': habit.habit_name,
            'created_date': habit.created_date.strftime('%Y-%m-%d'),
            'target_frequency': habit.target_frequency,
            'check_ins': habit.check_ins
        } for habit in self._habits_cache.values()]

    def save_habit(self, habit_name: str, target_frequency: str) -> bool:
        """Save a new habit"""
        if not self.user_id:
            return False
            
        if self._get_habit(habit_name):
            return False
            
        habit = Habit(
            user_id=self.user_id,
            habit_name=habit_name,
            target_frequency=target_frequency,
            check_ins=""
        )
        self.session.add(habit)
        self.session.commit()
        self._clear_cache()
        return True

    def check_in_habit(self, habit_name: str) -> bool:
        """Record a check-in for a habit"""
        if not self.user_id:
            return False
            
        habit = self._get_habit(habit_name)
        if not habit:
            return False
            
        today = datetime.now().strftime('%Y-%m-%d')

        if not habit.check_ins:
            habit.check_ins = today
        else:
            check_ins = habit.check_ins.split(',')
            if today not in check_ins:
                check_ins.append(today)
                habit.check_ins = ','.join(check_ins)

        self.session.commit()
        self._clear_cache()
        return True

    def get_streak(self, habit_name: str) -> int:
        """Calculate current streak for a habit"""
        if not self.user_id:
            return 0
            
        habit = self._get_habit(habit_name)
        if not habit or not habit.check_ins:
            return 0

        check_ins = sorted([datetime.strptime(date, '%Y-%m-%d') 
                          for date in habit.check_ins.split(',')])

        if not check_ins:
            return 0

        current_streak = 1
        today = datetime.now().date()
        last_date = check_ins[-1].date()

        if (today - last_date).days > 1:
            return 0

        for i in range(len(check_ins)-1, 0, -1):
            if (check_ins[i].date() - check_ins[i-1].date()).days == 1:
                current_streak += 1
            else:
                break

        return current_streak

    def get_completion_rate(self, habit_name: str) -> float:
        """Calculate habit completion rate"""
        if not self.user_id:
            return 0
            
        habit = self._get_habit(habit_name)
        if not habit or not habit.check_ins:
            return 0

        check_ins = habit.check_ins.split(',')
        created_date = habit.created_date
        days_since_creation = (datetime.now().date() - created_date).days + 1

        return len(set(check_ins)) / days_since_creation * 100