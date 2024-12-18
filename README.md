# # Prerequisites:
Python 3.7+ installed on your machine.
MongoDB and Redis installed locally or on a remote server.

# # Steps to Set Up:
1. Clone the Repository

2. Install Python Dependencies:

    # # Create a virtual environment:
    - virtualenv venv
    - source venv/bin/activate

    # # Install the required dependencies:
    - pip install -r requirements.txt

3. Set Up MongoDB:

    # # Install MongoDB:
    - brew tap mongodb/brew
    - brew install mongodb-community@6.0
    - brew services start mongodb/brew/mongodb-community

    # # Verify MongoDB is running:
    - ps aux | grep -v grep | grep mongod

4. Set Up Redis:

    # # Install Redis using Homebrew:
    - brew install redis
    - brew services start redis
    # # Verify Redis is running:
    - ps aux | grep redis

5. Configure Environment Variables:

    Create a .env file in the project root and define the following variables:

    MONGODB_URI=mongodb://localhost:27017/
    MONGODB_DB=product_catalog
    REDIS_HOST=localhost
    REDIS_PORT=6379

6. Run the Flask Application:

    # # Start the Flask application:
    - python app.py

    # # Verify the Application:
    - Access the API at http://127.0.0.1:5000.




# # Without Cache & With Cache Response Time
