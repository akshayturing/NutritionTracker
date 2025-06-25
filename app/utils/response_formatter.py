from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import uuid

def format_nutrition_summary_response(
    user_id: int,
    period_type: str,
    period_start: datetime,
    period_end: datetime,
    
    # Intake data
    total_calories: float,
    total_protein: float, 
    total_carbs: float,
    total_fat: float,
    total_fiber: Optional[float] = None,
    total_sugar: Optional[float] = None,
    total_sodium: Optional[float] = None,
    total_potassium: Optional[float] = None,
    total_vitamin_a: Optional[float] = None,
    total_vitamin_c: Optional[float] = None,
    total_calcium: Optional[float] = None,
    total_iron: Optional[float] = None,
    
    # Fat components
    saturated_fat: Optional[float] = None,
    unsaturated_fat: Optional[float] = None,
    trans_fat: Optional[float] = None,
    
    # Targets
    calorie_target: Optional[float] = None,
    protein_target: Optional[float] = None,
    carbs_target: Optional[float] = None,
    fat_target: Optional[float] = None,
    
    # Meal data
    meals: Optional[List[Dict[str, Any]]] = None,
    
    # Diet plan
    diet_plan: Optional[Dict[str, Any]] = None,
    
    # Trends
    trend_data: Optional[List[Dict[str, Any]]] = None,
    
    # Recommendations
    recommendations: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Format nutrition data according to the standardized response schema.
    
    Args:
        Various nutritional data parameters
        
    Returns:
        A dictionary formatted according to the NutritionSummaryResponse schema
    """
    # Generate a unique ID for this summary
    summary_id = str(uuid.uuid4())
    
    # Calculate macronutrient distribution
    total_macro_calories = ((total_protein * 4) + (total_carbs * 4) + (total_fat * 9))
    
    if total_macro_calories > 0:
        protein_percentage = round((total_protein * 4 / total_macro_calories) * 100, 1)
        carbs_percentage = round((total_carbs * 4 / total_macro_calories) * 100, 1)
        fat_percentage = round((total_fat * 9 / total_macro_calories) * 100, 1)
    else:
        protein_percentage = carbs_percentage = fat_percentage = 0
    
    # Calculate remaining amounts
    remaining_calories = (calorie_target - total_calories) if calorie_target is not None else None
    remaining_protein = (protein_target - total_protein) if protein_target is not None else None
    remaining_carbs = (carbs_target - total_carbs) if carbs_target is not None else None
    remaining_fat = (fat_target - total_fat) if fat_target is not None else None
    
    # Determine overall status based on calories
    if calorie_target is None:
        overall_status = "no_target"
    elif remaining_calories is not None:
        if remaining_calories < -50:  # More than 50 calories over
            overall_status = "exceeded"
        elif remaining_calories > 50:  # More than 50 calories under
            overall_status = "under_target"
        else:
            overall_status = "on_target"
    else:
        overall_status = "unknown"
    
    # Calculate goal percentages and status for each nutrient
    calorie_percentage = _calculate_goal_percentage(total_calories, calorie_target)
    protein_percentage = _calculate_goal_percentage(total_protein, protein_target)
    carbs_percentage = _calculate_goal_percentage(total_carbs, carbs_target)
    fat_percentage = _calculate_goal_percentage(total_fat, fat_target)
    
    calorie_status = _determine_status(total_calories, calorie_target)
    protein_status = _determine_status(total_protein, protein_target)
    carbs_status = _determine_status(total_carbs, carbs_target)
    fat_status = _determine_status(total_fat, fat_target)
    
    # Format period label based on type
    period_label = _format_period_label(period_type, period_start, period_end)
    
    # Calculate averages for trend data if available
    trend_averages = None
    if trend_data:
        days = len(trend_data)
        if days > 0:
            trend_averages = {
                "calories": round(sum(day.get("calories", 0) for day in trend_data) / days, 1),
                "protein": round(sum(day.get("protein", 0) for day in trend_data) / days, 1),
                "carbohydrates": round(sum(day.get("carbohydrates", 0) for day in trend_data) / days, 1),
                "fat": round(sum(day.get("fat", 0) for day in trend_data) / days, 1)
            }
    
    # Format meal data if available
    formatted_meals = []
    if meals:
        for meal in meals:
            formatted_meal = {
                "meal_id": meal.get("id"),
                "name": meal.get("name") or "Unnamed Meal",
                "timestamp": meal.get("timestamp"),
                "calories": meal.get("calories") or 0,
                "protein": meal.get("protein") or 0,
                "carbohydrates": meal.get("carbs") or 0,
                "fat": meal.get("fat") or 0
            }
            formatted_meals.append(formatted_meal)
    
    # Build response structure according to schema
    response = {
        "summary_id": summary_id,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        
        "period": {
            "type": period_type,
            "start": period_start.isoformat(),
            "end": period_end.isoformat(),
            "label": period_label
        },
        
        "intake": {
            "calories": {
                "value": round(total_calories, 1),
                "unit": "kcal"
            },
            "macronutrients": {
                "protein": {
                    "value": round(total_protein, 1),
                    "unit": "g"
                },
                "carbohydrates": {
                    "value": round(total_carbs, 1),
                    "unit": "g",
                    "components": {}
                },
                "fat": {
                    "value": round(total_fat, 1),
                    "unit": "g",
                    "components": {}
                }
            },
            "distribution": {
                "protein_percentage": protein_percentage,
                "carbs_percentage": carbs_percentage,
                "fat_percentage": fat_percentage
            },
            "total_meals": len(formatted_meals) if formatted_meals else 0,
        },
        
        "targets": {
            "calories": {
                "value": calorie_target,
                "unit": "kcal"
            },
            "macronutrients": {
                "protein": {
                    "value": protein_target,
                    "unit": "g"
                },
                "carbohydrates": {
                    "value": carbs_target,
                    "unit": "g"
                },
                "fat": {
                    "value": fat_target,
                    "unit": "g"
                }
            },
            "active_diet_plan": diet_plan
        },
        
        "remaining": {
            "calories": {
                "value": round(remaining_calories, 1) if remaining_calories is not None else None,
                "unit": "kcal"
            },
            "macronutrients": {
                "protein": {
                    "value": round(remaining_protein, 1) if remaining_protein is not None else None,
                    "unit": "g"
                },
                "carbohydrates": {
                    "value": round(remaining_carbs, 1) if remaining_carbs is not None else None,
                    "unit": "g"
                },
                "fat": {
                    "value": round(remaining_fat, 1) if remaining_fat is not None else None,
                    "unit": "g"
                }
            },
            "status": overall_status
        },
        
        "status": {
            "goals": {
                "calories": {
                    "percentage": calorie_percentage,
                    "status": calorie_status
                },
                "protein": {
                    "percentage": protein_percentage,
                    "status": protein_status
                },
                "carbohydrates": {
                    "percentage": carbs_percentage,
                    "status": carbs_status
                },
                "fat": {
                    "percentage": fat_percentage,
                    "status": fat_status
                }
            }
        }
    }
    
    # Add optional components if values are provided
    if total_fiber is not None or total_sugar is not None:
        carb_components = {}
        
        if total_fiber is not None:
            carb_components["fiber"] = {
                "value": round(total_fiber, 1),
                "unit": "g"
            }
        
        if total_sugar is not None:
            carb_components["sugar"] = {
                "value": round(total_sugar, 1),
                "unit": "g"
            }
        
        response["intake"]["macronutrients"]["carbohydrates"]["components"] = carb_components
    
    if saturated_fat is not None or unsaturated_fat is not None or trans_fat is not None:
        fat_components = {}
        
        if saturated_fat is not None:
            fat_components["saturated"] = {
                "value": round(saturated_fat, 1),
                "unit": "g"
            }
        
        if unsaturated_fat is not None:
            fat_components["unsaturated"] = {
                "value": round(unsaturated_fat, 1),
                "unit": "g"
            }
        
        if trans_fat is not None:
            fat_components["trans"] = {
                "value": round(trans_fat, 1),
                "unit": "g"
            }
        
        response["intake"]["macronutrients"]["fat"]["components"] = fat_components
    
    # Add micronutrients if any are provided
    micronutrients = {}
    
    if total_sodium is not None:
        micronutrients["sodium"] = {
            "value": round(total_sodium, 1),
            "unit": "mg"
        }
    
    if total_potassium is not None:
        micronutrients["potassium"] = {
            "value": round(total_potassium, 1),
            "unit": "mg"
        }
    
    if total_vitamin_a is not None:
        micronutrients["vitamin_a"] = {
            "value": round(total_vitamin_a, 1),
            "unit": "IU"
        }
    
    if total_vitamin_c is not None:
        micronutrients["vitamin_c"] = {
            "value": round(total_vitamin_c, 1),
            "unit": "mg"
        }
    
    if total_calcium is not None:
        micronutrients["calcium"] = {
            "value": round(total_calcium, 1),
            "unit": "mg"
        }
    
    if total_iron is not None:
        micronutrients["iron"] = {
            "value": round(total_iron, 1),
            "unit": "mg"
        }
    
    if micronutrients:
        response["intake"]["micronutrients"] = micronutrients
    
    # Add meal breakdown if available
    if formatted_meals:
        response["intake"]["meal_breakdown"] = formatted_meals
    
    # Add trend data if available
    if trend_data:
        trend_response = {
            "period": period_type,
            "data": trend_data
        }
        
        if trend_averages:
            trend_response["averages"] = trend_averages
        
        response["trends"] = trend_response
    
    # Add recommendations if available
    if recommendations:
        response["recommendations"] = recommendations
    
    # Add dietary balance score
    if calorie_target is not None:
        # Simple dietary balance calculation
        macronutrient_score = _calculate_macro_balance_score(protein_percentage, carbs_percentage, fat_percentage)
        target_score = _calculate_target_adherence_score(
            calorie_percentage, protein_percentage, carbs_percentage, fat_percentage)
        
        balance_score = (macronutrient_score + target_score) / 2
        
        balance_rating = "poor"
        if balance_score >= 80:
            balance_rating = "excellent"
        elif balance_score >= 60:
            balance_rating = "good"
        elif balance_score >= 40:
            balance_rating = "fair"
        
        balance_analysis = []
        
        # Add analysis points based on scores
        if macronutrient_score < 60:
            balance_analysis.append({
                "category": "macronutrient_balance",
                "message": "Your macronutrient balance could be improved for optimal nutrition",
                "severity": "warning"
            })
        
        if protein_percentage < 10:
            balance_analysis.append({
                "category": "macronutrient_balance",
                "message": "Your protein intake is very low. Consider adding more protein-rich foods.",
                "severity": "alert"
            })
        
        if fat_percentage > 40:
            balance_analysis.append({
                "category": "macronutrient_balance",
                "message": "Your fat intake is high. Consider reducing high-fat foods.",
                "severity": "warning"
            })
        
        response["status"]["dietary_balance"] = {
            "score": round(balance_score, 1),
            "rating": balance_rating,
            "analysis": balance_analysis
        }
    
    return response

def _calculate_goal_percentage(actual: Optional[float], target: Optional[float]) -> Optional[float]:
    """Calculate percentage of goal achieved"""
    if actual is None or target is None or target == 0:
        return None
    return round((actual / target) * 100, 1)

def _determine_status(actual: Optional[float], target: Optional[float]) -> str:
    """Determine status relative to target"""
    if actual is None or target is None:
        return "no_target"
    
    percentage = (actual / target) * 100
    
    if percentage < 90:
        return "under_target"
    elif percentage <= 110:
        return "on_target"
    else:
        return "exceeded"

def _format_period_label(period_type: str, start: datetime, end: datetime) -> str:
    """Format a human-readable period label"""
    if period_type == "day":
        return f"{start.strftime('%A, %B %d, %Y')}"
    elif period_type == "week":
        return f"Week of {start.strftime('%B %d, %Y')}"
    elif period_type == "month":
        return f"{start.strftime('%B %Y')}"
    else:
        if start.date() == end.date():
            return f"{start.strftime('%A, %B %d, %Y')}"
        return f"{start.strftime('%B %d, %Y')} - {end.strftime('%B %d, %Y')}"

def _calculate_macro_balance_score(protein_pct: float, carbs_pct: float, fat_pct: float) -> float:
    """
    Calculate a score for macronutrient balance based on recommended ranges:
    - Protein: 10-35%
    - Carbs: 45-65%
    - Fat: 20-35%
    """
    protein_score = 100
    if protein_pct < 10:
        protein_score = (protein_pct / 10) * 100
    elif protein_pct > 35:
        protein_score = max(0, 100 - ((protein_pct - 35) * 5))
    
    carbs_score = 100
    if carbs_pct < 45:
        carbs_score = (carbs_pct / 45) * 100
    elif carbs_pct > 65:
        carbs_score = max(0, 100 - ((carbs_pct - 65) * 5))
    
    fat_score = 100
    if fat_pct < 20:
        fat_score = (fat_pct / 20) * 100
    elif fat_pct > 35:
        fat_score = max(0, 100 - ((fat_pct - 35) * 5))
    
    return (protein_score + carbs_score + fat_score) / 3

def _calculate_target_adherence_score(calorie_pct: Optional[float], 
                                    protein_pct: Optional[float], 
                                    carbs_pct: Optional[float], 
                                    fat_pct: Optional[float]) -> float:
    """Calculate how closely the user is adhering to their targets"""
    scores = []
    
    if calorie_pct is not None:
        calorie_score = 100
        if calorie_pct < 90:
            calorie_score = (calorie_pct / 90) * 100
        elif calorie_pct > 110:
            calorie_score = max(0, 100 - ((calorie_pct - 110) * 2))
        scores.append(calorie_score)
    
    if protein_pct is not None:
        protein_score = 100
        if protein_pct < 90:
            protein_score = (protein_pct / 90) * 100
        elif protein_pct > 120:  # Allow more protein than target
            protein_score = max(0, 100 - ((protein_pct - 120) * 2))
        scores.append(protein_score)
    
    if carbs_pct is not None:
        carbs_score = 100
        if carbs_pct < 90:
            carbs_score = (carbs_pct / 90) * 100
        elif carbs_pct > 110:
            carbs_score = max(0, 100 - ((carbs_pct - 110) * 2))
        scores.append(carbs_score)
    
    if fat_pct is not None:
        fat_score = 100
        if fat_pct < 90:
            fat_score = (fat_pct / 90) * 100
        elif fat_pct > 110:
            fat_score = max(0, 100 - ((fat_pct - 110) * 2))
        scores.append(fat_score)
    
    if not scores:
        return 0
    
    return sum(scores) / len(scores)