# app/utils/nutrition_summary.py

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import func, and_
from app.models.user import User
from app.models.meal import Meal
from NutritionTracker.app.models.fooditem import FoodItem, MealFoodItem

def calculate_nutrition_summary(user_id: int, 
                                start_date: Optional[datetime] = None,
                                end_date: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Calculate comprehensive nutrition summary for a user within a specified date range.
    
    Args:
        user_id: The ID of the user
        start_date: Optional start date for the summary period (defaults to beginning of current day)
        end_date: Optional end date for the summary period (defaults to current time)
        
    Returns:
        Dictionary containing comprehensive nutrition information including:
        - Daily targets and current progress
        - Macronutrient distribution
        - Micronutrient intake
        - Meal breakdown
        - Historical trends
    """
    # Set default date range to current day if not provided
    if start_date is None:
        start_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    if end_date is None:
        end_date = datetime.utcnow()
        
    # Get user profile with nutritional targets
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found")
    
    # Fetch all meals in the specified time range
    meals = Meal.query.filter(
        and_(
            Meal.user_id == user_id,
            Meal.timestamp >= start_date,
            Meal.timestamp <= end_date
        )
    ).all()
    
    # Initialize counters for nutritional totals
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    total_fiber = 0
    total_sugar = 0
    total_sodium = 0
    meal_breakdown = []
    
    # Calculate totals and build meal breakdown
    for meal in meals:
        # Add to meal breakdown
        meal_data = {
            'id': meal.id,
            'name': meal.meal_name,
            'timestamp': meal.timestamp.isoformat(),
            'calories': meal.calories or 0,
            'protein': meal.protein or 0,
            'carbs': meal.carbs or 0,
            'fat': meal.fat or 0,
        }
        meal_breakdown.append(meal_data)
        
        # Add to totals
        total_calories += meal.calories or 0
        total_protein += meal.protein or 0
        total_carbs += meal.carbs or 0
        total_fat += meal.fat or 0
        
        # Get detailed nutrition from food items in this meal
        meal_items = MealFoodItem.query.filter_by(meal_id=meal.id).all()
        for item in meal_items:
            food = FoodItem.query.get(item.food_item_id)
            if food:
                portion_multiplier = item.portion_size / 100  # Assuming standard portion is 100g
                total_fiber += (food.fiber or 0) * portion_multiplier
                total_sugar += (food.sugar or 0) * portion_multiplier
                total_sodium += (food.sodium or 0) * portion_multiplier
    
    # Calculate macronutrient percentages
    total_macro_calories = (
        (total_protein * 4) +  # 4 calories per gram of protein
        (total_carbs * 4) +    # 4 calories per gram of carbs
        (total_fat * 9)        # 9 calories per gram of fat
    )
    
    if total_macro_calories > 0:
        protein_percent = (total_protein * 4 / total_macro_calories) * 100
        carbs_percent = (total_carbs * 4 / total_macro_calories) * 100
        fat_percent = (total_fat * 9 / total_macro_calories) * 100
    else:
        protein_percent = carbs_percent = fat_percent = 0
    
    # Calculate percentage of daily targets
    calorie_percent = _calculate_percentage(total_calories, user.calorie_goal)
    protein_target_percent = _calculate_percentage(total_protein, user.protein_goal)
    carbs_target_percent = _calculate_percentage(total_carbs, user.carbs_goal)
    fat_target_percent = _calculate_percentage(total_fat, user.fat_goal)
    
    # Get historical data for trends (last 7 days)
    trends = _calculate_historical_trends(user_id, end_date)
    
    # Generate remaining values to hit targets
    remaining = {
        'calories': max(0, user.calorie_goal - total_calories) if user.calorie_goal else None,
        'protein': max(0, user.protein_goal - total_protein) if user.protein_goal else None,
        'carbs': max(0, user.carbs_goal - total_carbs) if user.carbs_goal else None,
        'fat': max(0, user.fat_goal - total_fat) if user.fat_goal else None
    }
    
    # Build the complete summary
    summary = {
        'timestamp': datetime.utcnow().isoformat(),
        'period': {
            'start': start_date.isoformat(),
            'end': end_date.isoformat()
        },
        'targets': {
            'calories': user.calorie_goal,
            'protein': user.protein_goal,
            'carbs': user.carbs_goal,
            'fat': user.fat_goal
        },
        'consumed': {
            'calories': total_calories,
            'protein': total_protein,
            'carbs': total_carbs,
            'fat': total_fat,
            'fiber': total_fiber,
            'sugar': total_sugar,
            'sodium': total_sodium
        },
        'percentage_of_targets': {
            'calories': calorie_percent,
            'protein': protein_target_percent,
            'carbs': carbs_target_percent,
            'fat': fat_target_percent
        },
        'macronutrient_distribution': {
            'protein_percent': round(protein_percent, 1),
            'carbs_percent': round(carbs_percent, 1),
            'fat_percent': round(fat_percent, 1)
        },
        'remaining': remaining,
        'meal_count': len(meals),
        'meal_breakdown': meal_breakdown,
        'trends': trends,
        'updated_at': datetime.utcnow().isoformat()
    }
    
    return summary

def _calculate_percentage(value: float, target: Optional[float]) -> Optional[float]:
    """Calculate percentage of target achieved"""
    if target is None or target == 0:
        return None
    return round((value / target) * 100, 1)

def _calculate_historical_trends(user_id: int, end_date: datetime, days: int = 7) -> Dict[str, Any]:
    """Calculate historical nutrition trends for visualization"""
    trends = {
        'dates': [],
        'calories': [],
        'protein': [],
        'carbs': [],
        'fat': []
    }
    
    for day_offset in range(days - 1, -1, -1):
        target_date = end_date.date() - timedelta(days=day_offset)
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())
        
        # Get meals for this day
        day_meals = Meal.query.filter(
            and_(
                Meal.user_id == user_id,
                Meal.timestamp >= start_datetime,
                Meal.timestamp <= end_datetime
            )
        ).all()
        
        # Calculate totals for the day
        day_calories = sum(meal.calories or 0 for meal in day_meals)
        day_protein = sum(meal.protein or 0 for meal in day_meals)
        day_carbs = sum(meal.carbs or 0 for meal in day_meals)
        day_fat = sum(meal.fat or 0 for meal in day_meals)
        
        # Add to trends
        trends['dates'].append(target_date.isoformat())
        trends['calories'].append(day_calories)
        trends['protein'].append(day_protein)
        trends['carbs'].append(day_carbs)
        trends['fat'].append(day_fat)
    
    # Calculate averages
    if days > 0:
        trends['averages'] = {
            'calories': round(sum(trends['calories']) / days, 1),
            'protein': round(sum(trends['protein']) / days, 1),
            'carbs': round(sum(trends['carbs']) / days, 1),
            'fat': round(sum(trends['fat']) / days, 1)
        }
    
    return trends

def suggest_remaining_meals(user_id: int, summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate meal suggestions to meet remaining nutritional targets
    
    Args:
        user_id: The ID of the user
        summary: The current nutrition summary
        
    Returns:
        List of meal suggestions with nutritional content
    """
    # This would be a complex recommendation system in a real implementation
    # Here we'll just create some basic recommendations based on remaining targets
    
    remaining = summary['remaining']
    suggestions = []
    
    # Only suggest if significant calories remaining
    if remaining['calories'] and remaining['calories'] > 200:
        if remaining['protein'] and remaining['protein'] > 20:
            # High protein suggestion
            suggestions.append({
                'name': 'Protein-rich meal',
                'description': 'Grilled chicken breast with vegetables',
                'calories': 350,
                'protein': 35,
                'carbs': 10,
                'fat': 15
            })
            
        if remaining['carbs'] and remaining['carbs'] > 30:
            # High carb suggestion
            suggestions.append({
                'name': 'Carb-focused meal',
                'description': 'Whole grain pasta with tomato sauce',
                'calories': 400,
                'protein': 12,
                'carbs': 65,
                'fat': 8
            })
            
        if remaining['fat'] and remaining['fat'] > 15:
            # Healthy fats suggestion
            suggestions.append({
                'name': 'Healthy fats meal',
                'description': 'Avocado and salmon salad',
                'calories': 450,
                'protein': 25,
                'carbs': 15,
                'fat': 30
            })
            
    # Snack suggestion for small remaining amounts
    if remaining['calories'] and 100 < remaining['calories'] < 300:
        suggestions.append({
            'name': 'Balanced snack',
            'description': 'Greek yogurt with berries and nuts',
            'calories': 200,
            'protein': 15,
            'carbs': 20,
            'fat': 8
        })
        
    return suggestions