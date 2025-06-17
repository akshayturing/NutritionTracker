from models.food_database import db, FoodItem, Nutrient, NutrientValue, FoodCategory
from flask import Flask
import csv
import os

def create_nutrients():
    """Create standard nutrients in the database"""
    nutrients = [
        # Macronutrients
        ('ENERC_KCAL', 'Energy', 'kcal', 'Macronutrients', 1),
        ('PROCNT', 'Protein', 'g', 'Macronutrients', 2),
        ('FAT', 'Total Fat', 'g', 'Macronutrients', 3),
        ('CHOCDF', 'Total Carbohydrate', 'g', 'Macronutrients', 4),
        ('FIBTG', 'Dietary Fiber', 'g', 'Macronutrients', 5),
        ('SUGAR', 'Sugars', 'g', 'Macronutrients', 6),
        
        # Fats
        ('FASAT', 'Saturated Fat', 'g', 'Fats', 1),
        ('FAMS', 'Monounsaturated Fat', 'g', 'Fats', 2),
        ('FAPU', 'Polyunsaturated Fat', 'g', 'Fats', 3),
        ('FATRN', 'Trans Fat', 'g', 'Fats', 4),
        ('CHOLE', 'Cholesterol', 'mg', 'Fats', 5),
        
        # Minerals
        ('NA', 'Sodium', 'mg', 'Minerals', 1),
        ('CA', 'Calcium', 'mg', 'Minerals', 2),
        ('MG', 'Magnesium', 'mg', 'Minerals', 3),
        ('K', 'Potassium', 'mg', 'Minerals', 4),
        ('FE', 'Iron', 'mg', 'Minerals', 5),
        ('ZN', 'Zinc', 'mg', 'Minerals', 6),
        ('P', 'Phosphorus', 'mg', 'Minerals', 7),
        
        # Vitamins
        ('VITA_RAE', 'Vitamin A', 'µg', 'Vitamins', 1),
        ('VITC', 'Vitamin C', 'mg', 'Vitamins', 2),
        ('VITD', 'Vitamin D', 'µg', 'Vitamins', 3),
        ('VITB12', 'Vitamin B12', 'µg', 'Vitamins', 4),
        ('FOLFD', 'Folate', 'µg', 'Vitamins', 5),
        ('NIA', 'Niacin', 'mg', 'Vitamins', 6),
        ('VITB6A', 'Vitamin B6', 'mg', 'Vitamins', 7),
        ('RIBF', 'Riboflavin', 'mg', 'Vitamins', 8),
        ('THIA', 'Thiamin', 'mg', 'Vitamins', 9),
        ('TOCPHA', 'Vitamin E', 'mg', 'Vitamins', 10),
        ('VITK1', 'Vitamin K', 'µg', 'Vitamins', 11),
    ]
    
    for code, name, unit, category, display_order in nutrients:
        nutrient = Nutrient(
            code=code,
            name=name,
            unit=unit,
            category=category,
            display_order=display_order
        )
        db.session.add(nutrient)
    
    db.session.commit()
    print(f"Created {len(nutrients)} nutrients")

def create_categories():
    """Create standard food categories"""
    categories = [
        ('Fruits', 'Fresh, frozen, canned, and dried fruits'),
        ('Vegetables', 'Fresh, frozen, canned, and dried vegetables'),
        ('Grains', 'Rice, pasta, bread, and other grain products'),
        ('Protein Foods', 'Meat, poultry, seafood, eggs, nuts, seeds'),
        ('Dairy', 'Milk, yogurt, cheese, and other dairy products'),
        ('Oils', 'Cooking oils, butter, and other fats'),
        ('Beverages', 'Water, juice, soda, coffee, tea'),
        ('Snacks', 'Chips, crackers, and other snack items'),
        ('Sweets', 'Desserts, candy, and other sweet items'),
        ('Condiments', 'Sauces, dressings, and other condiments'),
        ('Mixed Dishes', 'Recipes and prepared meals'),
        ('Fast Food', 'Foods from fast food restaurants'),
        ('Supplements', 'Protein powders and other supplements'),
    ]
    
    for name, description in categories:
        category = FoodCategory(name=name, description=description)
        db.session.add(category)
    
    db.session.commit()
    print(f"Created {len(categories)} categories")

def create_sample_foods():
    """Create sample food items for demonstration"""
    # Get nutrients and categories for reference
    nutrients = {n.code: n for n in Nutrient.query.all()}
    categories = {c.name: c for c in FoodCategory.query.all()}
    
    sample_foods = [
        {
            'name': 'Apple', 
            'description': 'Fresh medium apple with skin',
            'brand': '',
            'serving_size': 182,
            'serving_unit': 'g',
            'serving_description': '1 medium (3" dia)',
            'categories': ['Fruits'],
            'nutrients': {
                'ENERC_KCAL': 95,
                'PROCNT': 0.47,
                'FAT': 0.31,
                'CHOCDF': 25.13,
                'FIBTG': 4.4,
                'SUGAR': 18.91,
                'NA': 1.82,
                'CA': 11.0,
                'K': 195.0,
                'VITC': 8.4,
            }
        },
        {
            'name': 'Chicken Breast', 
            'description': 'Boneless, skinless chicken breast',
            'brand': '',
            'serving_size': 100,
            'serving_unit': 'g',
            'serving_description': '100g',
            'categories': ['Protein Foods'],
            'nutrients': {
                'ENERC_KCAL': 165,
                'PROCNT': 31.02,
                'FAT': 3.57,
                'CHOCDF': 0,
                'FIBTG': 0,
                'SUGAR': 0,
                'NA': 74,
                'CA': 15,
                'K': 256,
                'CHOLE': 85,
            }
        },
        {
            'name': 'Brown Rice', 
            'description': 'Cooked long-grain brown rice',
            'brand': '',
            'serving_size': 100,
            'serving_unit': 'g',
            'serving_description': '1/2 cup',
            'categories': ['Grains'],
            'nutrients': {
                'ENERC_KCAL': 112,
                'PROCNT': 2.32,
                'FAT': 0.83,
                'CHOCDF': 23.51,
                'FIBTG': 1.8,
                'SUGAR': 0.35,
                'NA': 5,
                'MG': 43,
                'P': 77,
            }
        },
        {
            'name': 'Spinach', 
            'description': 'Raw spinach leaves',
            'brand': '',
            'serving_size': 30,
            'serving_unit': 'g',
            'serving_description': '1 cup',
            'categories': ['Vegetables'],
            'nutrients': {
                'ENERC_KCAL': 7,
                'PROCNT': 0.86,
                'FAT': 0.12,
                'CHOCDF': 1.09,
                'FIBTG': 0.7,
                'NA': 24,
                'CA': 30,
                'FE': 0.81,
                'VITA_RAE': 141,
                'VITC': 8.4,
            }
        },
        {
            'name': 'Greek Yogurt', 
            'description': 'Plain, nonfat Greek yogurt',
            'brand': '',
            'serving_size': 170,
            'serving_unit': 'g',
            'serving_description': '6 oz container',
            'categories': ['Dairy'],
            'nutrients': {
                'ENERC_KCAL': 100,
                'PROCNT': 18.0,
                'FAT': 0.0,
                'CHOCDF': 6.0,
                'SUGAR': 6.0,
                'NA': 65,
                'CA': 200,
            }
        }
    ]
    
    for food_data in sample_foods:
        # Create the food item
        food = FoodItem(
            name=food_data['name'],
            description=food_data['description'],
            brand=food_data['brand'],
            serving_size=food_data['serving_size'],
            serving_unit=food_data['serving_unit'],
            serving_description=food_data['serving_description'],
            source='internal',
            verified=True
        )
        
        # Add categories
        for category_name in food_data['categories']:
            if category_name in categories:
                food.categories.append(categories[category_name])
        
        # Add nutrients
        for nutrient_code, value in food_data['nutrients'].items():
            if nutrient_code in nutrients:
                nutrient_value = NutrientValue(
                    nutrient=nutrients[nutrient_code],
                    value=value
                )
                food.nutrients.append(nutrient_value)
        
        db.session.add(food)
    
    db.session.commit()
    print(f"Created {len(sample_foods)} sample foods")

def init_database(app):
    """Initialize the database with default data"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if database is already populated
        if Nutrient.query.count() == 0:
            create_nutrients()
        
        if FoodCategory.query.count() == 0:
            create_categories()
        
        if FoodItem.query.count() == 0:
            create_sample_foods()
            
        print("Database initialized successfully!")

def import_from_csv(app, csv_file):
    """Import food data from a CSV file"""
    with app.app_context():
        # Get nutrients and categories for reference
        nutrients = {n.code: n for n in Nutrient.query.all()}
        categories_dict = {c.name: c for c in FoodCategory.query.all()}
        
        foods_added = 0
        
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Basic food information
                name = row.get('name', '').strip()
                
                # Skip if no name
                if not name:
                    continue
                    
                # Check if food already exists
                existing_food = FoodItem.query.filter_by(name=name).first()
                if existing_food:
                    continue
                
                food = FoodItem(
                    name=name,
                    description=row.get('description', ''),
                    brand=row.get('brand', ''),
                    serving_size=float(row.get('serving_size', 100)),
                    serving_unit=row.get('serving_unit', 'g'),
                    serving_description=row.get('serving_description', ''),
                    source='csv-import',
                    verified=True
                )
                
                # Add categories
                categories = row.get('categories', '').split(',')
                for category_name in categories:
                    category_name = category_name.strip()
                    if not category_name:
                        continue
                        
                    # Get or create category
                    if category_name in categories_dict:
                        category = categories_dict[category_name]
                    else:
                        category = FoodCategory(name=category_name)
                        db.session.add(category)
                        categories_dict[category_name] = category
                    
                    food.categories.append(category)
                
                # Add nutrients
                for field, value in row.items():
                    # Skip non-nutrient fields
                    if field in ['name', 'description', 'brand', 'serving_size', 
                                'serving_unit', 'serving_description', 'categories']:
                        continue
                    
                    # Try to match field to a nutrient code
                    if field in nutrients:
                        try:
                            nutrient_value = float(value) if value else 0
                            food.nutrients.append(NutrientValue(
                                nutrient=nutrients[field],
                                value=nutrient_value
                            ))
                        except (ValueError, TypeError):
                            # Skip invalid values
                            pass
                
                db.session.add(food)
                foods_added += 1
                
                # Commit in batches to prevent memory issues
                if foods_added % 100 == 0:
                    db.session.commit()
                    print(f"Added {foods_added} foods...")
        
        # Final commit for any remaining foods
        db.session.commit()
        print(f"Successfully imported {foods_added} foods from {csv_file}")

if __name__ == '__main__':
    # Create a Flask app context for database operations
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_nutrition.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database
    db.init_app(app)
    
    # Run the initialization
    init_database(app)
    
    # Optionally import from CSV if provided
    csv_path = os.environ.get('FOOD_CSV_PATH')
    if csv_path and os.path.exists(csv_path):
        import_from_csv(app, csv_path)
