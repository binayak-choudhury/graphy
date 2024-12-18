import unittest
from unittest.mock import patch
from app import app

class ProductControllerTestCase(unittest.TestCase):
    """
    Unit tests for the product endpoints.
    """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    # Cases with product lists

    @patch('services.product_service.get_all_products')
    def test_get_all_products_with_cache(self, mock_get_all_products):
        mock_get_all_products.return_value = [{'name': 'Product 1', 'category': 'Scooty'}]
        response = self.app.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Product 1', str(response.data))
        
    # Cases with product details

    @patch('services.product_service.get_product_by_id')
    def test_get_product_by_id_found(self, mock_get_product_by_id):
        mock_get_product_by_id.return_value = {'name': 'Royal Enfiled', 'category': 'Bike'}
        response = self.app.get("/products/67632b4884d1708a53fccef9")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Royal Enfiled', str(response.data))

    @patch('services.product_service.get_product_by_id')
    def test_get_product_by_id_not_found(self, mock_get_product_by_id):
        mock_get_product_by_id.return_value = None
        response = self.app.get("/products/676325347ed4a58336a2ad99")
        self.assertEqual(response.status_code, 404)

    # Cases with product CRUD operations
    
    def test_create_product(self):
        response = self.app.post("/products", json={
            "name": "MacBook Pro M3",
            "category": "Laptop",
            "price": 98000,
            "stock": 188880
        })
        self.assertEqual(response.status_code, 201)

    @patch('services.product_service.update_product')
    def test_update_product_success(self, mock_update_product):
        mock_update_product.return_value = {'name': 'Updated Product', 'price': 150}
        response = self.app.put("/products/67631e266ddbf30a23ca389e", json={
            "name": "Updated Product",
            "price": 150
        })
        self.assertEqual(response.status_code, 200)

    @patch('services.product_service.update_product')
    def test_update_product_not_found(self, mock_update_product):
        mock_update_product.return_value = None
        response = self.app.put("/products/67631036d6808eb1ca52d582", json={
            "name": "Updated Product",
            "price": 150
        })
        self.assertEqual(response.status_code, 404)

    @patch('services.product_service.delete_product')
    def test_delete_product_success(self, mock_delete_product):
        mock_delete_product.return_value = True
        response = self.app.delete("/products/676325347ed4a58336a2ad99")
        self.assertEqual(response.status_code, 200)

    @patch('services.product_service.delete_product')
    def test_delete_product_not_found(self, mock_delete_product):
        mock_delete_product.return_value = False
        response = self.app.delete("/products/12")
        self.assertEqual(response.status_code, 404)

    # Cases with product lists with filters

    def test_filter_products(self):
        response = self.app.get('/products/filter?category=Scooty&price_min=100000&price_max=150000')
        self.assertEqual(response.status_code, 200)

    def test_invalid_filter_products(self):
        response = self.app.get('/products/filter?category=Scooty&price_min=invalid')
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()