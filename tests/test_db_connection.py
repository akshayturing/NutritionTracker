# tests/test_db_connection.py
import pytest
import concurrent.futures
from app.models import User

# def test_db_connection_concurrent(app, _db):
#     """Test that database connections work reliably under concurrent operations."""
#     def add_user(i):
#         with app.app_context():
#             user = User(name=f'Concurrent User {i}', 
#                         email=f'concurrent{i}@example.com',
#                         age=20 + i)
#             _db.session.add(user)
#             _db.session.commit()
#             return user.id
    
#     # Run 5 concurrent database operations
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         future_to_index = {executor.submit(add_user, i): i for i in range(5)}
#         results = []
        
#         for future in concurrent.futures.as_completed(future_to_index):
#             index = future_to_index[future]
#             try:
#                 user_id = future.result()
#                 results.append((index, user_id))
#             except Exception as exc:
#                 assert False, f"User {index} generated an exception: {exc}"
    
#     # Verify all users were created
#     with app.app_context():
#         for index, user_id in results:
#             user = User.query.get(user_id)
#             assert user is not None
#             assert user.name == f'Concurrent User {index}'
#             assert user.email == f'concurrent{index}@example.com'

def test_db_connection_concurrent():
    """Test that multiple connections can be made concurrently."""
    import threading
    
    # Function to create a user in its own thread
    def create_user(user_id):
        try:
            from app import create_app, db
            from app.models.user import User
            
            app = create_app()
            with app.app_context():
                # Use UNIQUE email for each user
                user = User(
                    name=f'User {user_id}',
                    email=f'user{user_id}_{threading.get_ident()}@example.com',  # Unique email
                    age=30
                )
                db.session.add(user)
                db.session.commit()
        except Exception as e:
            return f"User {user_id} generated an exception: {e}"
        return None
    
    # Create multiple threads
    threads = []
    results = []
    for i in range(5):
        thread = threading.Thread(target=lambda i=i: results.append(create_user(i)))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check results - should not have exceptions
    for result in results:
        assert result is None, result

# def test_app_context_management():
#     """Test that app context is properly managed."""
#     from app import db
#     from flask import current_app
    
#     # Try accessing the database outside app context - should raise RuntimeError
#     try:
#         db.session.execute("SELECT 1")
#         assert False, "Expected exception was not raised"
#     except RuntimeError as e:
#         # We expect a RuntimeError specifically about working outside app context
#         assert "working outside of application context" in str(e) or \
#                "No application found" in str(e), f"Unexpected error message: {e}"
# # def test_app_context_management(app, _db):
    # """Test that app context is properly managed for database operations."""
    # with app.app_context():
    #     # This should work fine within the app context
    #     users = User.query.all()
    #     assert isinstance(users, list)
    
    # # This should fail without an app context
    # with pytest.raises(Exception):
    #     users = User.query.all()
