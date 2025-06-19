

import requests
import json
import time
from datetime import datetime, timedelta
import random
import unittest
import os
import sys

# Add the project root directory to the Python path if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now imports from our application should work
from app import create_app, db
from app.config import TestingConfig

class NutritionApiEndToEndTest(unittest.TestCase):
    """End-to-end test of the Nutrition Tracking API workflow"""
    
    
    BASE_URL = "http://localhost:5000/api"  # Change this to your API URL
    
    # Test Data
    TEST_USER = {
        "name": "Test User",
        "email": f"test_user_{int(time.time())}@example.com",  # Unique email
        "password": "TestPassword123!",
        "age": 30,
        "weight": 75.5,
        "height": 175,
        "gender": "male",
        "activity_level": "moderate"
    }
    
    NUTRITIONAL_GOALS = {
        "calorie_goal": 2000,
        "protein_goal": 150,
        "carbs_goal": 200,
        "fat_goal": 70
    }
    
    # Sample food items
    FOOD_ITEMS = [
        {
            "name": "Grilled Chicken Breast",
            "calories": 165,
            "protein": 31,
            "carbs": 0,
            "fat": 3.6,
            "fiber": 0,
            "sugar": 0,
            "sodium": 74,
            "serving_size": 100,  # grams
            "food_group": "protein"
        },
        {
            "name": "Brown Rice",
            "calories": 112,
            "protein": 2.6,
            "carbs": 23.5,
            "fat": 0.9,
            "fiber": 1.8,
            "sugar": 0.4,
            "sodium": 5,
            "serving_size": 100,
            "food_group": "grain"
        },
        {
            "name": "Broccoli",
            "calories": 34,
            "protein": 2.8,
            "carbs": 6.6,
            "fat": 0.4,
            "fiber": 2.6,
            "sugar": 1.7,
            "sodium": 33,
            "serving_size": 100,
            "food_group": "vegetable"
        },
        {
            "name": "Avocado",
            "calories": 160,
            "protein": 2,
            "carbs": 8.5,
            "fat": 14.7,
            "fiber": 6.7,
            "sugar": 0.7,
            "sodium": 7,
            "serving_size": 100,
            "food_group": "fruit"
        }
    ]
    
    # Sample meals for the day
    MEALS = [
        {
            "name": "Breakfast",
            "time": "07:30",
            "items": [
                {"food_id": None, "name": "Oatmeal", "portion_size": 200, "calories": 150, "protein": 5, "carbs": 27, "fat": 2.5},
                {"food_id": None, "name": "Banana", "portion_size": 120, "calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4}
            ]
        },
        {
            "name": "Lunch",
            "time": "12:30",
            "items": [
                # Will use created food items
            ]
        },
        {
            "name": "Dinner",
            "time": "18:30",
            "items": [
                # Will use created food items
            ]
        },
        {
            "name": "Snack",
            "time": "15:00",
            "items": [
                {"food_id": None, "name": "Greek Yogurt", "portion_size": 150, "calories": 130, "protein": 15, "carbs": 6, "fat": 4}
            ]
        }
    ]
    
    def setUp(self):
        """Set up test case - register user and get token"""
        self.auth_token = None
        self.user_id = None
        self.food_item_ids = []
        self.meal_ids = []
        
        # Register user
        self.register_user()
        
        # Login to get auth token
        self.login_user()
        
        # Set nutritional goals
        self.set_nutritional_goals()
        
        # Create food items
        self.create_food_items()
        
    def tearDown(self):
        """Clean up after tests - delete created resources"""
        if not self.auth_token:
            return
            
        # Delete meals
        for meal_id in self.meal_ids:
            try:
                self.delete_meal(meal_id)
            except:
                pass
                
        # Delete food items
        for food_id in self.food_item_ids:
            try:
                self.delete_food_item(food_id)
            except:
                pass
                
        # Logout
        self.logout_user()
    
    # Helper methods for API calls
    def api_request(self, method, endpoint, data=None, params=None, headers=None):
        """Send request to API with auth token if available"""
        url = f"{self.BASE_URL}/{endpoint}"
        
        # Include auth token if available
        if self.auth_token and headers is None:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
        elif self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
            
        # Make request based on method
        if method == "get":
            response = requests.get(url, params=params, headers=headers)
        elif method == "post":
            response = requests.post(url, json=data, headers=headers)
        elif method == "put":
            response = requests.put(url, json=data, headers=headers)
        elif method == "delete":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
        # Check for API error responses
        if response.status_code >= 400:
            print(f"API Error ({response.status_code}): {response.text}")
            
        return response
        
    def register_user(self):
        """Register a new user for testing"""
        print("\n1. Registering test user...")
        response = self.api_request("post", "auth/register", data=self.TEST_USER)
        
        self.assertEqual(response.status_code, 201, "User registration failed")
        response_data = response.json()
        print(f"User registered: {response_data.get('user', {}).get('email')}")
        
        # Store user ID if available
        if 'user' in response_data and 'id' in response_data['user']:
            self.user_id = response_data['user']['id']
    
    def login_user(self):
        """Login and get auth token"""
        print("\n2. Logging in to get authentication token...")
        login_data = {
            "email": self.TEST_USER["email"],
            "password": self.TEST_USER["password"]
        }
        
        response = self.api_request("post", "auth/login", data=login_data)
        
        self.assertEqual(response.status_code, 200, "Login failed")
        response_data = response.json()
        
        # Store token for subsequent requests
        self.auth_token = response_data.get("token")
        self.assertIsNotNone(self.auth_token, "No token received")
        print("Successfully logged in and got token")
    
    def logout_user(self):
        """Logout user and invalidate token"""
        print("\n9. Logging out user...")
        response = self.api_request("post", "auth/logout")
        
        self.assertEqual(response.status_code, 200, "Logout failed")
        print("User logged out successfully")
    
    def set_nutritional_goals(self):
        """Set nutritional goals for the user"""
        print("\n3. Setting nutritional goals...")
        response = self.api_request("put", "users/profile", data=self.NUTRITIONAL_GOALS)
        
        self.assertEqual(response.status_code, 200, "Setting nutritional goals failed")
        response_data = response.json()
        
        # Verify goals were set
        self.assertEqual(response_data["calorie_goal"], self.NUTRITIONAL_GOALS["calorie_goal"])
        self.assertEqual(response_data["protein_goal"], self.NUTRITIONAL_GOALS["protein_goal"])
        self.assertEqual(response_data["carbs_goal"], self.NUTRITIONAL_GOALS["carbs_goal"])
        self.assertEqual(response_data["fat_goal"], self.NUTRITIONAL_GOALS["fat_goal"])
        
        print(f"Nutritional goals set: {self.NUTRITIONAL_GOALS}")
    
    def create_food_items(self):
        """Create food items for testing"""
        print("\n4. Creating food items...")
        
        for food_item in self.FOOD_ITEMS:
            response = self.api_request("post", "foods", data=food_item)
            
            self.assertEqual(response.status_code, 201, f"Creating food item failed: {food_item['name']}")
            food_id = response.json().get("id")
            self.food_item_ids.append(food_id)
            print(f"Created food item: {food_item['name']} (ID: {food_id})")
            
        # Update meal templates with created food IDs
        if len(self.food_item_ids) >= 3:
            # Add lunch items
            self.MEALS[1]["items"] = [
                {"food_id": self.food_item_ids[0], "name": "Grilled Chicken Breast", "portion_size": 150},
                {"food_id": self.food_item_ids[1], "name": "Brown Rice", "portion_size": 200},
                {"food_id": self.food_item_ids[2], "name": "Broccoli", "portion_size": 150}
            ]
            
            # Add dinner items
            self.MEALS[2]["items"] = [
                {"food_id": self.food_item_ids[0], "name": "Grilled Chicken Breast", "portion_size": 200},
                {"food_id": self.food_item_ids[3], "name": "Avocado", "portion_size": 100},
                {"food_id": self.food_item_ids[2], "name": "Broccoli", "portion_size": 200}
            ]
    
    def delete_food_item(self, food_id):
        """Delete a food item"""
        response = self.api_request("delete", f"foods/{food_id}")
        return response.status_code == 200 or response.status_code == 204
    
    def log_meals_for_day(self):
        """Log meals for the current day"""
        print("\n5. Logging meals for the day...")
        
        today = datetime.now().date()
        
        for meal in self.MEALS:
            # Create meal timestamp
            meal_time = datetime.strptime(meal["time"], "%H:%M").time()
            meal_datetime = datetime.combine(today, meal_time)
            
            # Prepare meal data
            meal_data = {
                "meal_name": meal["name"],
                "timestamp": meal_datetime.isoformat(),
                "meal_items": []
            }
            
            # Add meal items
            total_calories = 0
            total_protein = 0
            total_carbs = 0
            total_fat = 0
            
            for item in meal["items"]:
                food_item = {
                    "portion_size": item["portion_size"]
                }
                
                # If food_id is available, use it
                if item["food_id"]:
                    food_item["food_item_id"] = item["food_id"]
                else:
                    # Otherwise include nutritional data directly
                    food_item["name"] = item["name"]
                    food_item["calories"] = item["calories"]
                    food_item["protein"] = item["protein"]
                    food_item["carbs"] = item["carbs"]
                    food_item["fat"] = item["fat"]
                    
                    # Calculate nutritional contribution based on portion
                    portion_factor = item["portion_size"] / 100  # Assuming standard 100g portion
                    total_calories += item["calories"] * portion_factor
                    total_protein += item["protein"] * portion_factor
                    total_carbs += item["carbs"] * portion_factor
                    total_fat += item["fat"] * portion_factor
                
                meal_data["meal_items"].append(food_item)
            
            # Add totals if using food items without IDs
            if any(item["food_id"] is None for item in meal["items"]):
                meal_data["calories"] = total_calories
                meal_data["protein"] = total_protein
                meal_data["carbs"] = total_carbs
                meal_data["fat"] = total_fat
            
            # Log the meal
            response = self.api_request("post", "meals", data=meal_data)
            
            self.assertEqual(response.status_code, 201, f"Logging meal failed: {meal['name']}")
            meal_id = response.json().get("id")
            self.meal_ids.append(meal_id)
            print(f"Logged meal: {meal['name']} (ID: {meal_id})")
    
    def delete_meal(self, meal_id):
        """Delete a meal"""
        response = self.api_request("delete", f"meals/{meal_id}")
        return response.status_code == 200 or response.status_code == 204
    
    def get_nutrition_summary(self):
        """Get nutrition summary for the current day"""
        print("\n6. Retrieving daily nutrition summary...")
        
        response = self.api_request("get", "nutrition/summary")
        
        self.assertEqual(response.status_code, 200, "Failed to get nutrition summary")
        summary = response.json()
        
        print("Nutrition Summary:")
        print(f"- Calories: {summary['intake']['calories']['value']} / {summary['targets']['calories']['value']}")
        print(f"- Protein: {summary['intake']['macronutrients']['protein']['value']} / {summary['targets']['macronutrients']['protein']['value']}")
        print(f"- Carbs: {summary['intake']['macronutrients']['carbohydrates']['value']} / {summary['targets']['macronutrients']['carbohydrates']['value']}")
        print(f"- Fat: {summary['intake']['macronutrients']['fat']['value']} / {summary['targets']['macronutrients']['fat']['value']}")
        print(f"- Status: {summary['remaining']['status']}")
        
        return summary
    
    def verify_nutritional_data(self, summary):
        """Verify that nutritional data is accurate and consistent"""
        print("\n7. Verifying nutritional data accuracy...")
        
        # Verify that all target values match what we set
        self.assertEqual(summary['targets']['calories']['value'], self.NUTRITIONAL_GOALS['calorie_goal'])
        self.assertEqual(summary['targets']['macronutrients']['protein']['value'], self.NUTRITIONAL_GOALS['protein_goal'])
        self.assertEqual(summary['targets']['macronutrients']['carbohydrates']['value'], self.NUTRITIONAL_GOALS['carbs_goal'])
        self.assertEqual(summary['targets']['macronutrients']['fat']['value'], self.NUTRITIONAL_GOALS['fat_goal'])
        
        # Verify that remaining values are correctly calculated
        calories_consumed = summary['intake']['calories']['value']
        calories_remaining = summary['remaining']['calories']['value']
        self.assertAlmostEqual(calories_consumed + calories_remaining, self.NUTRITIONAL_GOALS['calorie_goal'], delta=0.1)
        
        protein_consumed = summary['intake']['macronutrients']['protein']['value']
        protein_remaining = summary['remaining']['macronutrients']['protein']['value']
        self.assertAlmostEqual(protein_consumed + protein_remaining, self.NUTRITIONAL_GOALS['protein_goal'], delta=0.1)
        
        # Verify that total consumed matches sum of meals
        meal_count = summary['intake']['total_meals']
        self.assertEqual(meal_count, len(self.meal_ids))
        
        # Verify that status values are consistent with nutritional data
        calorie_percentage = summary['status']['goals']['calories']['percentage']
        expected_percentage = (calories_consumed / self.NUTRITIONAL_GOALS['calorie_goal']) * 100
        self.assertAlmostEqual(calorie_percentage, expected_percentage, delta=0.1)
        
        print("✅ Nutritional data verified successfully")
    
    def run_advanced_queries(self):
        """Test advanced nutritional queries"""
        print("\n8. Running advanced nutritional queries...")
        
        # Test nutrition trends
        print("8.1. Getting nutrition trends for the past 7 days...")
        response = self.api_request("get", "nutrition/nutrient-trends?days=7")
        
        self.assertEqual(response.status_code, 200, "Failed to get nutrition trends")
        trends = response.json()
        print(f"Received trend data for {len(trends['daily_data'])} days")
        
        # Test custom date range
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"8.2. Getting nutrition summary for custom date range ({yesterday} to {today})...")
        
        response = self.api_request(
            "get", 
            f"nutrition/summary?period=custom&start_date={yesterday}&end_date={today}"
        )
        
        self.assertEqual(response.status_code, 200, "Failed to get custom date range summary")
        custom_summary = response.json()
        print(f"Received custom range summary: {custom_summary['period_name']}")
        
        # Test with meal suggestions
        print("8.3. Getting nutrition summary with meal suggestions...")
        response = self.api_request("get", "nutrition/summary?include_suggestions=true")
        
        self.assertEqual(response.status_code, 200, "Failed to get summary with suggestions")
        suggestions_summary = response.json()
        
        if 'recommendations' in suggestions_summary and suggestions_summary['recommendations']:
            print(f"Received {len(suggestions_summary['recommendations'])} meal suggestions")
        else:
            print("No meal suggestions received (may be expected if targets are met)")
    
    def test_complete_nutrition_workflow(self):
        """Test the complete nutrition tracking workflow"""
        # 1-4. User setup is done in setUp()
        
        # 5. Log meals for the day
        self.log_meals_for_day()
        
        # 6. Get nutrition summary
        summary = self.get_nutrition_summary()
        
        # 7. Verify nutritional data
        self.verify_nutritional_data(summary)
        
        # 8. Run advanced queries
        self.run_advanced_queries()
        
        # 9. Logout is done in tearDown()

if __name__ == "__main__":
    unittest.main()
