import json
from tests.base_test import BaseTestCase
from app.models.food import Food, UserCustomFood

class FoodTestCase(BaseTestCase):
    """Test cases for food endpoints"""
    
    def test_get_all_foods(self):
        """Test listing all foods"""
        headers = self.get_auth_headers()
        
        response = self.client.get(
            '/api/foods',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('foods', data)
        self.assertIn('pagination', data)
        self.assertGreaterEqual(len(data['foods']), 3)  # At least our 3 test foods
    
    def test_get_food_by_id(self):
        """Test getting a specific food by ID"""
        headers = self.get_auth_headers()
        
        response = self.client.get(
            f'/api/foods/{self.apple_id}',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        food = json.loads(response.data)
        self.assertEqual(food['name'], 'Apple')
        self.assertEqual(food['category'], 'fruits')
        self.assertEqual(food['calories'], 95)
    
    def test_food_not_found(self):
        """Test requesting non-existent food"""
        headers = self.get_auth_headers()
        
        response = self.client.get(
            '/api/foods/99999',  # Non-existent ID
            headers=headers
        )
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error']['code'], 'RESOURCE_NOT_FOUND')
    
    def test_create_custom_food(self):
        """Test creating a custom food"""
        headers = self.get_auth_headers()
        
        custom_food = {
            'name': 'My Custom Smoothie',
            'category': 'beverage',
            'reference_portion_size': 1.0,
            'reference_portion_unit': 'cup',
            'calories': 150,
            'protein': 5,
            'carbohydrates': 30,
            'fat': 2,
            'fiber': 3
        }
        
        response = self.client.post(
            '/api/foods/custom',
            data=json.dumps(custom_food),
            headers=headers
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('food_id', data)
        
        # Verify food was created
        food = Food.query.filter_by(name='My Custom Smoothie').first()
        self.assertIsNotNone(food)
        self.assertTrue(food.is_custom)
        
        # Verify user-custom-food association
        assoc = UserCustomFood.query.filter_by(food_id=food.id).first()
        self.assertIsNotNone(assoc)
        self.assertEqual(assoc.user_id, self.test_user_id)
    
    def test_create_custom_food_validation(self):
        """Test custom food creation with invalid data"""
        headers = self.get_auth_headers()
        
        # Missing required fields
        invalid_food = {
            'name': 'Invalid Food',
            'category': 'test'
            # Missing nutritional info
        }
        
        response = self.client.post(
            '/api/foods/custom',
            data=json.dumps(invalid_food),
            headers=headers
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error']['code'], 'VALIDATION_ERROR')
    
    def test_update_custom_food(self):
        """Test updating a custom food"""
        headers = self.get_auth_headers()
        
        # First create a custom food
        custom_food = {
            'name': 'Food to Update',
            'category': 'test',
            'calories': 100,
            'protein': 5,
            'carbohydrates': 10,
            'fat': 2
        }
        
        create_response = self.client.post(
            '/api/foods/custom',
            data=json.dumps(custom_food),
            headers=headers
        )
        
        food_id = json.loads(create_response.data)['food_id']
        
        # Now update it
        updates = {
            'name': 'Updated Food Name',
            'calories': 120,
            'protein': 8
            # Only update some fields
        }
        
        response = self.client.put(
            f'/api/foods/custom/{food_id}',
            data=json.dumps(updates),
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify the food was updated
        food = Food.query.get(food_id)
        self.assertEqual(food.name, 'Updated Food Name')
        self.assertEqual(food.calories, 120)
        self.assertEqual(food.protein, 8)
        self.assertEqual(food.carbohydrates, 10)  # Unchanged
    
    def test_update_other_users_food(self):
        """Test attempting to update another user's custom food"""
        # Create a custom food for test_user
        headers = self.get_auth_headers()
        
        custom_food = {
            'name': 'Test User Food',
            'category': 'test',
            'calories': 100,
            'protein': 5,
            'carbohydrates': 10,
            'fat': 2
        }
        
        create_response = self.client.post(
            '/api/foods/custom',
            data=json.dumps(custom_food),
            headers=headers
        )
        
        food_id = json.loads(create_response.data)['food_id']
        
        # Try to update as other_user
        other_headers = self.get_auth_headers('other@example.com', 'password123')
        
        response = self.client.put(
            f'/api/foods/custom/{food_id}',
            data=json.dumps({'name': 'Hacked Food'}),
            headers=other_headers
        )
        
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_delete_custom_food(self):
        """Test deleting a custom food"""
        headers = self.get_auth_headers()
        
        # First create a custom food
        custom_food = {
            'name': 'Food to Delete',
            'category': 'test',
            'calories': 100,
            'protein': 5,
            'carbohydrates': 10,
            'fat': 2
        }
        
        create_response = self.client.post(
            '/api/foods/custom',
            data=json.dumps(custom_food),
            headers=headers
        )
        
        food_id = json.loads(create_response.data)['food_id']
        
        # Now delete it
        response = self.client.delete(
            f'/api/foods/custom/{food_id}',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify the food was deleted
        food = Food.query.get(food_id)
        self.assertIsNone(food)
    
    def test_food_search(self):
        """Test searching for foods by name"""
        headers = self.get_auth_headers()
        
        response = self.client.get(
            '/api/foods?search=chick',  # Should match Chicken Breast
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data['foods']), 1)
        self.assertIn('Chicken', data['foods'][0]['name'])
    
    def test_filter_by_category(self):
        """Test filtering foods by category"""
        headers = self.get_auth_headers()
        
        response = self.client.get(
            '/api/foods?category=fruits',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data['foods']), 1)
        self.assertEqual(data['foods'][0]['category'], 'fruits')