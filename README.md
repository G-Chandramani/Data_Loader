# Data_Loader
Data Loader Using CSV File &amp; CRUD operations on CSV file

### Create & Start Virtual Environment
  python -m venv venv
  venv\Scripts\activate

### Install Dependencies and Packages
  pip install Flask SQLAlchemy pandas

### Run Python File
  python app.py

### Retrive Product Information (Select Operation)
   Method: GET
   URL: http://127.0.0.1:5000/products

### Update product  (Update)
  Method: PUT
  URL: http://127.0.0.1:5000/product/<id>
  		  (e.g., /product/1)
      
  Body:
    {
      "product_name": "Updated Tea",
      "product_type": "Solid",
      "unit": "2Kg"
    }  
### Delete an perticular Product using product id (Delete)
    Method: DELETE
    URL: http://127.0.0.1:5000/product/<id>
    Replace <id> with the ID of the product you want to delete (e.g., /product/1).
