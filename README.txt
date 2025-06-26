# NutritionTracker

## General Description:
The Nutrition Tracking App helps users monitor their daily food intake, track macronutrients, and receive personalized meal recommendations. It integrates a food database API for nutritional values, supports barcode scanning, and provides real-time analytics through interactive graphs. The backend, built with Flask, ensures secure authentication, efficient data storage, and seamless API interactions. It also features offline meal logging, AI-powered meal suggestions, and encrypted data protection for privacy. Designed for scalability, the app can integrate with wearable devices and health tracking platforms.

### Conversation 1: Database Design & Setup The first step in backend development is designing a structured and efficient database. Using PostgreSQL or SQLite, the system should define schemas for storing users, meals, nutrients, and tracking history. The backend should support easy retrieval of food logs, calorie data, and macro intake while ensuring relationships between food items and user activity are optimized for performance.

### Conversation 2: User Authentication & Profile Management User authentication is crucial for securing data and providing personalized experiences. Implementing JWT-based authentication ensures encrypted access control, allowing users to securely log in, manage profiles, and set dietary goals. Additionally, a profile management system should store preferences like food allergies, calorie targets, and meal frequency to tailor nutritional tracking accordingly.

### Conversation 3: Food Database Integration Integrating a nutrition API such as USDA FoodData Central or Edamam allows users to search for and log food items with accurate nutritional values. A barcode-scanning feature could further streamline food input, enabling users to scan packaged food items and automatically retrieve calorie and nutrient information, reducing manual entry errors.

### Conversation 4: Meal Logging & Tracking System Developing a meal logging system enables users to record meals, specify portion sizes, and track nutrient intake effortlessly. The backend should support CRUD operations for adding, updating, and deleting meals while providing a daily tracking dashboard that evaluates calorie intake and macronutrient distribution, helping users stay within their dietary goals.

### Conversation 5: Implement a real-time nutritional summary module that calculates calorie intake and macronutrient distribution from logged meals, compares them against user-defined targets, and includes comprehensive unit tests to validate meal logging, updates, data retrieval, and nutritional accuracy.

### Conversation 6: RESTful API Development A well-structured RESTful API ensures seamless data exchange between the backend and frontend. Modular API endpoints should be designed for meal retrieval, food searches, and user authentication. Efficient data caching mechanisms should be implemented to reduce server load and speed up responses, making the system highly scalable.

### Conversation 7: Backend Debugging & Performance Optimization To ensure reliable system performance, the backend should be thoroughly debugged and optimized for consistency and speed. Key tasks include fixing nutrient aggregation inaccuracies, resolving issues in time-based data grouping, and handling edge cases like missing or malformed entries. Optimizing database queries and integrating lightweight caching will improve response efficiency. Robust error handling will further enhance system resilience and reliability across various usage scenarios.

### Conversation 8: Testing & Deployment To ensure stability, thorough unit and integration testing must be carried out across all modules. Backend optimizations such as query indexing and API response caching should be refined for performance. Finally, deploying the application using Docker, AWS, or Heroku ensures scalability and accessibility across various environments.

## Code Execution Screenshots
### Conversation 1: Execution Output
![Conversation 1 Execution](https://drive.google.com/file/d/16-zwvLRWcUjhO2uSCllkJDgr0c7y5O1Y/view?usp=sharing)
### Conversation 2: Execution Output
![Conversation 2 Execution](https://drive.google.com/file/d/1r34BLRRodIUU6u0d_CAkeIpT--wP0T-O/view?usp=drive_link)
### Conversation 3: Execution Output
![Conversation 3 Execution](https://drive.google.com/file/d/1-bQ4XMV0aRHioikEt35KIIFymUsEJiBC/view?usp=drive_link)
### Conversation 4: Execution Output
![Conversation 4 Execution](https://drive.google.com/file/d/1Mhi-Lw--_G67lDh7YoxLD5NrrTZd-nBv/view?usp=drive_link)
### Conversation 5: Execution Output
![Conversation 5 Execution](https://drive.google.com/file/d/1M2vhqOui1Fdo0WRDbYfOqEXZXme44g-y/view?usp=drive_link)
### Conversation 6: Execution Output
![Conversation 6 Execution](https://drive.google.com/file/d/16KVLWflGhxEDj0Hztb8uz01V4rGr__yT/view?usp=drive_link)
### Conversation 7: Execution Output
![Conversation 7 Execution](https://drive.google.com/file/d/1o8aLZZ8fjJpk21e9Mb_pA0WOKXVUrAaE/view?usp=drive_link)
### Conversation 8: Execution Output
![Conversation 8 Execution](https://drive.google.com/file/d/1AJXrkKYBxi53m7zvfO3HKfbPH2FxR73s/view?usp=drive_link)


## Unit Test Outputs and Coverage
The following test cases validate critical components of the system.
### Conversation 1 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1dNe2Msm4dOOM-cAhhDu3ZO4sE-AuSZ6R/view?usp=drive_link)

### Conversation 2 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1ukOEo6hOKyNWJGIu_X9NnewOv7hKd1_T/view?usp=drive_link)


### Conversation 3 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1468SppJjAa2Shq_pfixRstLNpwsH1Cjr/view?usp=drive_link)

### Conversation 4 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1iKCcMthLdKLWug9lkRg2PeSFd4t0eeHf/view?usp=drive_link)

### Conversation 5 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/16lXVoYs1xSywoTDzCNUOyQHOFDFmE4-A/view?usp=drive_link)

### Conversation 6 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1wDSFqpVBWpI8akuOZYoTyon9YCil8qWK/view?usp=drive_link)

### Conversation 7 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/12patoB2-1PtfWjArE1qnJhX4jsbzXKfx/view?usp=drive_link)

### Conversation 8 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1UyswEdoDU5HHo_I2JCwsOzVFauHd3aZY/view?usp=drive_link)
- **Test 2**:
  ![Test 2](https://drive.google.com/file/d/1MChk22IA_icOR5HyuukosIL56_5-Z6NC/view?usp=drive_link)
