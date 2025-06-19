from datetime import datetime, time, timedelta
from sqlalchemy import and_, func
from typing import Dict, Any, Optional, Tuple

from app.models.meal import Meal
from app.models.user import User

def calculate_daily_nutrients(user_id: int, date: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Calculate the total nutrient intake for a user on a specific day.
    
    Args:
        user_id (int): The ID of the user
        date (datetime, optional): The date to calculate nutrients for.
                                  If None, uses current date.
                                  
    Returns:
        Dict with total calories, protein, carbs, and fat consumed for the day,
        plus comparison to user's goals if available.
    """
    # Use current date if none provided
    if date is None:
        date = datetime.utcnow().date()
    else:
        # Ensure we're working with just the date portion
        date = date.date() if isinstance(date, datetime) else date
    
    # Define start and end of the day in UTC
    start_datetime = datetime.combine(date, time.min)
    end_datetime = datetime.combine(date, time.max)
    
    # Query all meals for the user within the specified day
    meals = Meal.query.filter(
        and_(
            Meal.user_id == user_id,
            Meal.timestamp >= start_datetime,
            Meal.timestamp <= end_datetime
        )
    ).all()
    
    # Initialize nutrient totals
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    # Sum up nutrients from all meals
    for meal in meals:
        total_calories += meal.calories or 0
        total_protein += meal.protein or 0
        total_carbs += meal.carbs or 0
        total_fat += meal.fat or 0
    
    # Get user's nutritional goals if available
    user = User.query.get(user_id)
    
    # Calculate percentage of goals met
    result = {
        "date": date.isoformat(),
        "total_meals": len(meals),
        "nutrients": {
            "calories": {
                "consumed": total_calories,
                "goal": user.calorie_goal if user and user.calorie_goal else None,
                "percentage": _calculate_percentage(total_calories, user.calorie_goal if user else None)
            },
            "protein": {
                "consumed": total_protein,
                "goal": user.protein_goal if user and user.protein_goal else None,
                "percentage": _calculate_percentage(total_protein, user.protein_goal if user else None)
            },
            "carbs": {
                "consumed": total_carbs,
                "goal": user.carbs_goal if user and user.carbs_goal else None,
                "percentage": _calculate_percentage(total_carbs, user.carbs_goal if user else None)
            },
            "fat": {
                "consumed": total_fat,
                "goal": user.fat_goal if user and user.fat_goal else None,
                "percentage": _calculate_percentage(total_fat, user.fat_goal if user else None)
            }
        },
        "meals": [meal.id for meal in meals]  # Just include meal IDs for reference
    }
    
    return result


def _calculate_percentage(value: Optional[float], target: Optional[float]) -> Optional[float]:
    """Calculate percentage of target met"""
    if value is None or target is None or target == 0:
        return None
    return round((value / target) * 100, 1)


def calculate_nutrient_trends(user_id: int, days: int = 7) -> Dict[str, Any]:
    """
    Calculate nutrient intake trends for a user over the specified number of days.
    
    Args:
        user_id (int): The ID of the user
        days (int): Number of past days to include (default: 7)
        
    Returns:
        Dict with daily nutrient totals and averages over the specified period
    """
    today = datetime.utcnow().date()
    daily_nutrients = []
    
    for day_offset in range(days):
        target_date = today - timedelta(days=day_offset)
        daily_result = calculate_daily_nutrients(user_id, target_date)
        daily_nutrients.append(daily_result)
    
    # Calculate averages
    avg_calories = sum(day['nutrients']['calories']['consumed'] for day in daily_nutrients) / days
    avg_protein = sum(day['nutrients']['protein']['consumed'] for day in daily_nutrients) / days
    avg_carbs = sum(day['nutrients']['carbs']['consumed'] for day in daily_nutrients) / days
    avg_fat = sum(day['nutrients']['fat']['consumed'] for day in daily_nutrients) / days
    
    return {
        "period": {
            "start_date": (today - timedelta(days=days-1)).isoformat(),
            "end_date": today.isoformat(),
            "days": days
        },
        "averages": {
            "calories": round(avg_calories, 1),
            "protein": round(avg_protein, 1),
            "carbs": round(avg_carbs, 1),
            "fat": round(avg_fat, 1)
        },
        "daily_data": daily_nutrients
    }
