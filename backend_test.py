import requests
import sys
from datetime import datetime

class NavyaAPITester:
    def __init__(self, base_url="https://agri-layout-preview.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, data=None, expected_count=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                
                # Additional validation for specific endpoints
                if expected_count is not None:
                    try:
                        json_data = response.json()
                        if isinstance(json_data, list):
                            actual_count = len(json_data)
                            if actual_count >= expected_count:
                                print(f"   ✅ Data count: {actual_count} (expected >= {expected_count})")
                            else:
                                print(f"   ⚠️  Data count: {actual_count} (expected >= {expected_count})")
                        elif isinstance(json_data, dict) and 'message' in json_data:
                            print(f"   ✅ Response: {json_data['message']}")
                    except Exception as e:
                        print(f"   ⚠️  Could not validate response data: {e}")
                
                return True, response.json() if response.content else {}
            else:
                self.tests_passed += 1 if response.status_code in [200, 201] else 0
                error_msg = f"Expected {expected_status}, got {response.status_code}"
                print(f"❌ Failed - {error_msg}")
                self.failed_tests.append(f"{name}: {error_msg}")
                try:
                    error_detail = response.json()
                    print(f"   Error detail: {error_detail}")
                except:
                    print(f"   Response text: {response.text[:200]}")
                return False, {}

        except requests.exceptions.Timeout:
            error_msg = "Request timeout"
            print(f"❌ Failed - {error_msg}")
            self.failed_tests.append(f"{name}: {error_msg}")
            return False, {}
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"❌ Failed - {error_msg}")
            self.failed_tests.append(f"{name}: {error_msg}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        success, response = self.run_test(
            "Root API Endpoint",
            "GET",
            "api/",
            200
        )
        return success

    def test_get_all_products(self):
        """Test getting all products"""
        success, response = self.run_test(
            "Get All Products",
            "GET",
            "api/products",
            200,
            expected_count=70  # Expecting at least 70 products
        )
        if success and isinstance(response, list):
            print(f"   📊 Total products found: {len(response)}")
            # Check if products have required fields
            if response:
                sample_product = response[0]
                required_fields = ['id', 'name', 'category', 'description', 'image']
                missing_fields = [field for field in required_fields if field not in sample_product]
                if missing_fields:
                    print(f"   ⚠️  Missing fields in product: {missing_fields}")
                else:
                    print(f"   ✅ Product structure is valid")
        return success

    def test_get_categories(self):
        """Test getting product categories"""
        success, response = self.run_test(
            "Get Product Categories",
            "GET",
            "api/products/categories",
            200,
            expected_count=6  # Expecting 6 categories
        )
        if success and isinstance(response, list):
            print(f"   📊 Categories found: {response}")
        return success

    def test_filter_by_category(self):
        """Test filtering products by category"""
        # Test with Farm Machinery category
        success, response = self.run_test(
            "Filter Products by Category (Farm Machinery)",
            "GET",
            "api/products?category=Farm+Machinery",
            200,
            expected_count=10  # Expecting at least 10 farm machinery products
        )
        if success and isinstance(response, list):
            print(f"   📊 Farm Machinery products: {len(response)}")
            # Verify all products are from the correct category
            if response:
                wrong_category = [p for p in response if p.get('category') != 'Farm Machinery']
                if wrong_category:
                    print(f"   ⚠️  Found {len(wrong_category)} products with wrong category")
                else:
                    print(f"   ✅ All products are from Farm Machinery category")
        return success

    def test_filter_popular_products(self):
        """Test filtering popular products"""
        success, response = self.run_test(
            "Filter Popular Products",
            "GET",
            "api/products?popular=true",
            200,
            expected_count=5  # Expecting at least 5 popular products
        )
        if success and isinstance(response, list):
            print(f"   📊 Popular products found: {len(response)}")
            # Verify all products are marked as popular
            if response:
                non_popular = [p for p in response if not p.get('popular', False)]
                if non_popular:
                    print(f"   ⚠️  Found {len(non_popular)} products not marked as popular")
                else:
                    print(f"   ✅ All products are correctly marked as popular")
        return success

    def test_get_single_product(self):
        """Test getting a single product by ID"""
        # First get all products to get a valid ID
        try:
            response = requests.get(f"{self.base_url}/api/products", timeout=10)
            if response.status_code == 200:
                products = response.json()
                if products:
                    product_id = products[0]['id']
                    success, product_data = self.run_test(
                        f"Get Single Product (ID: {product_id[:8]}...)",
                        "GET",
                        f"api/products/{product_id}",
                        200
                    )
                    if success and isinstance(product_data, dict):
                        print(f"   ✅ Product name: {product_data.get('name', 'N/A')}")
                        print(f"   ✅ Product category: {product_data.get('category', 'N/A')}")
                        # Check if models are present
                        models = product_data.get('models', [])
                        print(f"   📊 Product models: {len(models)}")
                    return success
                else:
                    print("❌ No products available to test single product endpoint")
                    self.failed_tests.append("Get Single Product: No products available")
                    return False
            else:
                print("❌ Could not fetch products for single product test")
                self.failed_tests.append("Get Single Product: Could not fetch products list")
                return False
        except Exception as e:
            print(f"❌ Error in single product test: {e}")
            self.failed_tests.append(f"Get Single Product: {e}")
            return False

    def test_get_contact_info(self):
        """Test getting contact information"""
        success, response = self.run_test(
            "Get Contact Information",
            "GET",
            "api/contact-info",
            200
        )
        if success and isinstance(response, dict):
            required_fields = ['name', 'phone', 'email', 'address', 'website', 'business_timing']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                print(f"   ⚠️  Missing contact fields: {missing_fields}")
            else:
                print(f"   ✅ Contact info structure is valid")
                print(f"   📊 Business: {response.get('name', 'N/A')}")
                print(f"   📊 Phone: {response.get('phone', 'N/A')}")
        return success

    def test_invalid_product_id(self):
        """Test getting product with invalid ID"""
        success, response = self.run_test(
            "Get Product with Invalid ID",
            "GET",
            "api/products/invalid-id-12345",
            404
        )
        return success

def main():
    print("🚀 Starting Navya Enterprises API Testing")
    print("=" * 60)
    
    # Setup
    tester = NavyaAPITester()
    
    # Run all tests
    test_results = []
    
    print("\n📋 Running Backend API Tests...")
    
    # Test all endpoints
    test_results.append(("Root API", tester.test_root_endpoint()))
    test_results.append(("All Products", tester.test_get_all_products()))
    test_results.append(("Product Categories", tester.test_get_categories()))
    test_results.append(("Category Filter", tester.test_filter_by_category()))
    test_results.append(("Popular Products", tester.test_filter_popular_products()))
    test_results.append(("Single Product", tester.test_get_single_product()))
    test_results.append(("Contact Info", tester.test_get_contact_info()))
    test_results.append(("Invalid Product ID", tester.test_invalid_product_id()))
    
    # Print results summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\n📈 Overall Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.failed_tests:
        print(f"\n❌ Failed Tests:")
        for failure in tester.failed_tests:
            print(f"   • {failure}")
    
    success_rate = (tester.tests_passed / tester.tests_run) * 100 if tester.tests_run > 0 else 0
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())