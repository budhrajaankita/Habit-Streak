from datetime import datetime
import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db, Habit
from typing import Generator
import functools

class HabitTracker:
    def __init__(self):
        self.db: Generator[Session, None, None] = get_db()
        self.session = next(self.db)
        self._habits_cache = {}
        self._last_cache_update = None

    def _get_habit(self, habit_name: str):
        """Get habit with caching"""
        if habit_name not in self._habits_cache:
            self._habits_cache[habit_name] = self.session.query(Habit).filter(Habit.habit_name == habit_name).first()
        return self._habits_cache[habit_name]

    def _clear_cache(self):
        """Clear the habits cache"""
        self._habits_cache.clear()
        self._last_cache_update = None

    def load_habits(self):
        """Load habits from database with caching"""
        current_time = datetime.now()
        if self._last_cache_update is None or (current_time - self._last_cache_update).seconds > 300:
            habits = self.session.query(Habit).all()
            self._habits_cache = {habit.habit_name: habit for habit in habits}
            self._last_cache_update = current_time
        
        return [{
            'habit_name': habit.habit_name,
            'created_date': habit.created_date.strftime('%Y-%m-%d'),
            'target_frequency': habit.target_frequency,
            'check_ins': habit.check_ins
        } for habit in self._habits_cache.values()]

    def save_habit(self, habit_name: str, target_frequency: str):
        """Save a new habit"""
        if self._get_habit(habit_name):
            return False
            
        habit = Habit(
            habit_name=habit_name,
            target_frequency=target_frequency,
            check_ins=""
        )
        self.session.add(habit)
        self.session.commit()
        self._clear_cache()
        return True

    def check_in_habit(self, habit_name: str):
        """Record a check-in for a habit"""
        habit = self._get_habit(habit_name)
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

    def get_streak(self, habit_name: str) -> int:
        """Calculate current streak for a habit"""
        habit = self._get_habit(habit_name)

        if not habit.check_ins:
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
        habit = self._get_habit(habit_name)

        if not habit.check_ins:
            return 0

        check_ins = habit.check_ins.split(',')
        created_date = habit.created_date
        days_since_creation = (datetime.now().date() - created_date).days + 1

        return len(set(check_ins)) / days_since_creation * 100