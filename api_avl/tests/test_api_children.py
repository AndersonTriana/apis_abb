"""
Integration Tests for Children Management API.

This module contains comprehensive tests for all REST API endpoints
using FastAPI's TestClient and pytest fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import date

from api_avl.main import app
from api_avl.service.child_service import ChildService


@pytest.fixture(autouse=True)
def reset_tree():
    """
    Fixture to reset the AVL tree before each test.
    
    This ensures test isolation by clearing all data from the singleton
    ChildService instance before each test runs.
    
    autouse=True means this fixture runs automatically for every test.
    """
    service = ChildService()
    service.clear_all()
    yield
    # Cleanup after test
    service.clear_all()


@pytest.fixture
def client():
    """
    Fixture to create a TestClient for the FastAPI application.
    
    Returns:
        TestClient instance for making HTTP requests to the API.
    """
    return TestClient(app)


@pytest.fixture
def sample_child():
    """
    Fixture providing sample child data for testing.
    
    Returns:
        Dictionary with valid child data.
    """
    return {
        "document": 123456,
        "name": "Ana García",
        "age": 6,
        "guardian": "María López"
    }


@pytest.fixture
def multiple_children():
    """
    Fixture providing multiple children for testing traversals.
    
    Returns:
        List of dictionaries with child data.
    """
    return [
        {
            "document": 500000,
            "name": "Alice Johnson",
            "age": 8,
            "guardian": "Robert Johnson"
        },
        {
            "document": 300000,
            "name": "Bob Smith",
            "age": 7,
            "guardian": "Linda Smith"
        },
        {
            "document": 700000,
            "name": "Carol Williams",
            "age": 9,
            "guardian": "James Williams"
        },
        {
            "document": 200000,
            "name": "David Brown",
            "age": 5,
            "guardian": "Susan Brown"
        },
        {
            "document": 800000,
            "name": "Eve Davis",
            "age": 10,
            "guardian": "Michael Davis"
        }
    ]


# ============================================================================
# TEST 1: INSERCIÓN DE UN NIÑO
# ============================================================================

class TestChildInsertion:
    """Tests for child insertion (POST /children)."""
    
    def test_insert_child_success(self, client, sample_child):
        """
        Test successful child insertion.
        
        Verifies:
        - Status code is 201 Created
        - Response contains all fields from request
        - All field values match the input
        """
        response = client.post("/children", json=sample_child)
        
        assert response.status_code == 201, "Should return 201 Created"
        
        data = response.json()
        assert data["document"] == sample_child["document"]
        assert data["name"] == sample_child["name"]
        assert data["age"] == sample_child["age"]
        assert data["guardian"] == sample_child["guardian"]
    
    def test_insert_child_duplicate_document(self, client, sample_child):
        """
        Test insertion with duplicate document.
        
        Verifies:
        - First insertion succeeds with 201
        - Second insertion with same document fails with 400
        - Error message indicates duplicate document
        """
        # First insertion should succeed
        response1 = client.post("/children", json=sample_child)
        assert response1.status_code == 201, "First insertion should succeed"
        
        # Second insertion with same document should fail
        response2 = client.post("/children", json=sample_child)
        assert response2.status_code == 400, "Should return 400 Bad Request for duplicate"
        
        data = response2.json()
        assert "detail" in data
        assert "already exists" in data["detail"].lower()
    
    def test_insert_child_invalid_document_range(self, client, sample_child):
        """
        Test insertion with invalid document (out of range).
        
        Verifies:
        - Document > 999999 returns 400
        - Document < 0 returns 400
        """
        # Document too large
        invalid_child = sample_child.copy()
        invalid_child["document"] = 1000000
        response = client.post("/children", json=invalid_child)
        assert response.status_code == 400 or response.status_code == 422
        
        # Negative document
        invalid_child["document"] = -1
        response = client.post("/children", json=invalid_child)
        assert response.status_code == 400 or response.status_code == 422
    
    def test_insert_child_missing_required_fields(self, client):
        """
        Test insertion with missing required fields.
        
        Verifies:
        - Missing fields return 400 or 422 (validation error)
        """
        incomplete_child = {
            "document": 123456,
            "first_name": "John"
            # Missing other required fields
        }
        response = client.post("/children", json=incomplete_child)
        assert response.status_code in [400, 422], "Should return 400 or 422 for missing fields"
    
    def test_insert_child_invalid_age(self, client, sample_child):
        """
        Test insertion with invalid age.
        
        Verifies:
        - Invalid age returns 400 or 422 (validation error)
        """
        invalid_child = sample_child.copy()
        invalid_child["age"] = 25  # Too old for a child
        response = client.post("/children", json=invalid_child)
        assert response.status_code in [400, 422], "Should return 400 or 422 for invalid age"
    
    def test_insert_child_negative_age(self, client, sample_child):
        """
        Test insertion with negative age.
        
        Verifies:
        - Negative age returns 400 or 422 (validation error)
        """
        invalid_child = sample_child.copy()
        invalid_child["age"] = -1
        response = client.post("/children", json=invalid_child)
        assert response.status_code in [400, 422], "Should return 400 or 422 for negative age"


# ============================================================================
# TEST 2: BÚSQUEDA DE UN NIÑO EXISTENTE Y NO EXISTENTE
# ============================================================================

class TestChildRetrieval:
    """Tests for child retrieval (GET /children/{document})."""
    
    def test_get_existing_child(self, client, sample_child):
        """
        Test retrieval of an existing child.
        
        Verifies:
        - Status code is 200 OK
        - Response contains correct child data
        - All fields match the inserted data
        """
        # First, insert a child
        client.post("/children", json=sample_child)
        
        # Then retrieve it
        response = client.get(f"/children/{sample_child['document']}")
        
        assert response.status_code == 200, "Should return 200 OK"
        
        data = response.json()
        assert data["document"] == sample_child["document"]
        assert data["name"] == sample_child["name"]
        assert data["age"] == sample_child["age"]
        assert data["guardian"] == sample_child["guardian"]
    
    def test_get_non_existent_child(self, client):
        """
        Test retrieval of a non-existent child.
        
        Verifies:
        - Status code is 404 Not Found
        - Error message indicates child not found
        """
        response = client.get("/children/999999")
        
        assert response.status_code == 404, "Should return 404 Not Found"
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_get_child_invalid_document(self, client):
        """
        Test retrieval with invalid document format.
        
        Verifies:
        - Invalid document returns 400 or 422
        """
        response = client.get("/children/1000000")  # Out of range
        assert response.status_code == 400 or response.status_code == 404


# ============================================================================
# TEST 3: LISTAR NIÑOS CON DISTINTOS RECORRIDOS
# ============================================================================

class TestChildTraversals:
    """Tests for listing children with different traversal orders."""
    
    def test_list_children_in_order(self, client, multiple_children):
        """
        Test in-order traversal (sorted by document).
        
        Verifies:
        - Status code is 200 OK
        - Children are returned in ascending order by document
        - Total count is correct
        - Order field indicates 'in'
        """
        # Insert multiple children
        for child in multiple_children:
            client.post("/children", json=child)
        
        # Get in-order traversal
        response = client.get("/children?order=in")
        
        assert response.status_code == 200, "Should return 200 OK"
        
        data = response.json()
        assert data["total"] == len(multiple_children)
        assert data["order"] == "in"
        assert len(data["children"]) == len(multiple_children)
        
        # Verify children are sorted by document in ascending order
        documents = [child["document"] for child in data["children"]]
        expected_order = sorted([c["document"] for c in multiple_children])
        assert documents == expected_order, f"Expected {expected_order}, got {documents}"
    
    def test_list_children_pre_order(self, client, multiple_children):
        """
        Test pre-order traversal (root-left-right).
        
        Verifies:
        - Status code is 200 OK
        - Children are returned in pre-order
        - Total count is correct
        - Order field indicates 'pre'
        
        Tree structure after insertions (500000 is root):
                500000
               /      \\
           300000    700000
           /            \\
        200000        800000
        """
        # Insert multiple children
        for child in multiple_children:
            client.post("/children", json=child)
        
        # Get pre-order traversal
        response = client.get("/children?order=pre")
        
        assert response.status_code == 200, "Should return 200 OK"
        
        data = response.json()
        assert data["total"] == len(multiple_children)
        assert data["order"] == "pre"
        assert len(data["children"]) == len(multiple_children)
        
        # Verify pre-order: root, left subtree, right subtree
        documents = [child["document"] for child in data["children"]]
        # Expected pre-order: 500000, 300000, 200000, 700000, 800000
        expected_order = [500000, 300000, 200000, 700000, 800000]
        assert documents == expected_order, f"Expected {expected_order}, got {documents}"
    
    def test_list_children_post_order(self, client, multiple_children):
        """
        Test post-order traversal (left-right-root).
        
        Verifies:
        - Status code is 200 OK
        - Children are returned in post-order
        - Total count is correct
        - Order field indicates 'post'
        """
        # Insert multiple children
        for child in multiple_children:
            client.post("/children", json=child)
        
        # Get post-order traversal
        response = client.get("/children?order=post")
        
        assert response.status_code == 200, "Should return 200 OK"
        
        data = response.json()
        assert data["total"] == len(multiple_children)
        assert data["order"] == "post"
        assert len(data["children"]) == len(multiple_children)
        
        # Verify post-order: left subtree, right subtree, root
        documents = [child["document"] for child in data["children"]]
        # Expected post-order: 200000, 300000, 800000, 700000, 500000
        expected_order = [200000, 300000, 800000, 700000, 500000]
        assert documents == expected_order, f"Expected {expected_order}, got {documents}"
    
    def test_list_children_invalid_order(self, client):
        """
        Test listing with invalid order parameter.
        
        Verifies:
        - Invalid order returns 400 or 422 (validation error)
        """
        response = client.get("/children?order=invalid")
        assert response.status_code in [400, 422], "Should return 400 or 422 for invalid order"
    
    def test_list_children_empty_tree(self, client):
        """
        Test listing when tree is empty.
        
        Verifies:
        - Status code is 200 OK
        - Total is 0
        - Children list is empty
        """
        response = client.get("/children?order=in")
        
        assert response.status_code == 200, "Should return 200 OK"
        
        data = response.json()
        assert data["total"] == 0
        assert len(data["children"]) == 0


# ============================================================================
# TEST 4: ACTUALIZAR UN NIÑO
# ============================================================================

class TestChildUpdate:
    """Tests for child update (PUT /children/{document})."""
    
    def test_update_child_success(self, client, sample_child):
        """
        Test successful child update.
        
        Verifies:
        - Status code is 200 OK
        - Updated fields are reflected in response
        - Document field remains unchanged
        - Non-updated fields remain unchanged
        """
        # First, insert a child
        client.post("/children", json=sample_child)
        
        # Update some fields
        update_data = {
            "name": "Jane García",
            "age": 7,
            "guardian": "María García"
        }
        
        response = client.put(
            f"/children/{sample_child['document']}", 
            json=update_data
        )
        
        assert response.status_code == 200, "Should return 200 OK"
        
        data = response.json()
        # Verify updated fields
        assert data["name"] == update_data["name"]
        assert data["age"] == update_data["age"]
        assert data["guardian"] == update_data["guardian"]
        
        # Verify document remains unchanged
        assert data["document"] == sample_child["document"]
    
    def test_update_non_existent_child(self, client):
        """
        Test update of non-existent child.
        
        Verifies:
        - Status code is 404 Not Found
        - Error message indicates child not found
        """
        update_data = {
            "name": "Updated Name"
        }
        
        response = client.put("/children/999999", json=update_data)
        
        assert response.status_code == 404, "Should return 404 Not Found"
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_update_child_no_fields(self, client, sample_child):
        """
        Test update with no fields provided.
        
        Verifies:
        - Status code is 400 Bad Request
        - Error message indicates no fields to update
        """
        # First, insert a child
        client.post("/children", json=sample_child)
        
        # Try to update with empty data
        response = client.put(
            f"/children/{sample_child['document']}", 
            json={}
        )
        
        assert response.status_code == 400, "Should return 400 for no fields"
    
    def test_update_child_invalid_data(self, client, sample_child):
        """
        Test update with invalid data.
        
        Verifies:
        - Invalid data returns 400 or 422 (validation error)
        """
        # First, insert a child
        client.post("/children", json=sample_child)
        
        # Try to update with invalid age
        update_data = {
            "age": 25  # Too old
        }
        
        response = client.put(
            f"/children/{sample_child['document']}", 
            json=update_data
        )
        
        assert response.status_code in [400, 422], "Should return 400 or 422 for invalid data"
    
    def test_update_preserves_tree_structure(self, client, multiple_children):
        """
        Test that update preserves AVL tree structure.
        
        Verifies:
        - After update, in-order traversal still returns sorted list
        - All other children remain in tree
        """
        # Insert multiple children
        for child in multiple_children:
            client.post("/children", json=child)
        
        # Update one child
        update_data = {"first_name": "Updated"}
        client.put(f"/children/{multiple_children[0]['document']}", json=update_data)
        
        # Verify tree structure is maintained
        response = client.get("/children?order=in")
        data = response.json()
        
        documents = [child["document"] for child in data["children"]]
        expected_order = sorted([c["document"] for c in multiple_children])
        assert documents == expected_order


# ============================================================================
# TEST 5: ELIMINAR UN NIÑO
# ============================================================================

class TestChildDeletion:
    """Tests for child deletion (DELETE /children/{document})."""
    
    def test_delete_child_success(self, client, sample_child):
        """
        Test successful child deletion.
        
        Verifies:
        - Status code is 200 OK
        - Success message is returned
        - Child no longer exists in tree
        - Child cannot be retrieved after deletion
        """
        # First, insert a child
        client.post("/children", json=sample_child)
        
        # Delete the child
        response = client.delete(f"/children/{sample_child['document']}")
        
        assert response.status_code == 200, "Should return 200 OK"
        
        data = response.json()
        assert "message" in data
        assert "deleted successfully" in data["message"].lower()
        
        # Verify child no longer exists
        get_response = client.get(f"/children/{sample_child['document']}")
        assert get_response.status_code == 404, "Child should not exist after deletion"
    
    def test_delete_non_existent_child(self, client):
        """
        Test deletion of non-existent child.
        
        Verifies:
        - Status code is 404 Not Found
        - Error message indicates child not found
        """
        response = client.delete("/children/999999")
        
        assert response.status_code == 404, "Should return 404 Not Found"
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_delete_child_not_in_list(self, client, multiple_children):
        """
        Test that deleted child does not appear in listings.
        
        Verifies:
        - After deletion, child is not in any traversal
        - Total count is decremented
        - Other children remain in tree
        """
        # Insert multiple children
        for child in multiple_children:
            client.post("/children", json=child)
        
        # Delete one child
        deleted_document = multiple_children[2]["document"]
        client.delete(f"/children/{deleted_document}")
        
        # Verify child is not in in-order list
        response = client.get("/children?order=in")
        data = response.json()
        
        assert data["total"] == len(multiple_children) - 1
        documents = [child["document"] for child in data["children"]]
        assert deleted_document not in documents
        
        # Verify other children are still present
        remaining_documents = [c["document"] for c in multiple_children if c["document"] != deleted_document]
        for doc in remaining_documents:
            assert doc in documents
    
    def test_delete_maintains_tree_balance(self, client, multiple_children):
        """
        Test that deletion maintains AVL tree balance.
        
        Verifies:
        - After deletion, tree remains balanced
        - In-order traversal still returns sorted list
        """
        # Insert multiple children
        for child in multiple_children:
            client.post("/children", json=child)
        
        # Delete middle child (root)
        client.delete(f"/children/{multiple_children[0]['document']}")
        
        # Verify tree is still balanced (in-order returns sorted list)
        response = client.get("/children?order=in")
        data = response.json()
        
        documents = [child["document"] for child in data["children"]]
        assert documents == sorted(documents), "Tree should maintain sorted order after deletion"
    
    def test_delete_all_children_sequentially(self, client, multiple_children):
        """
        Test deleting all children one by one.
        
        Verifies:
        - Each deletion succeeds
        - Final tree is empty
        """
        # Insert multiple children
        for child in multiple_children:
            client.post("/children", json=child)
        
        # Delete all children
        for child in multiple_children:
            response = client.delete(f"/children/{child['document']}")
            assert response.status_code == 200
        
        # Verify tree is empty
        response = client.get("/children?order=in")
        data = response.json()
        assert data["total"] == 0
        assert len(data["children"]) == 0


# ============================================================================
# TEST 6: CONSIDERACIONES GENERALES
# ============================================================================

class TestGeneralConsiderations:
    """General tests for API behavior."""
    
    def test_tree_info_endpoint(self, client, multiple_children):
        """
        Test tree info endpoint.
        
        Verifies:
        - Endpoint returns tree statistics
        - Statistics are accurate
        """
        # Insert multiple children
        for child in multiple_children:
            client.post("/children", json=child)
        
        response = client.get("/children/tree/info")
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_children"] == len(multiple_children)
        assert data["is_empty"] is False
        assert "root_document" in data
        assert "min_document" in data
        assert "max_document" in data
    
    def test_api_root_endpoint(self, client):
        """
        Test API root endpoint.
        
        Verifies:
        - Root endpoint returns API information
        """
        response = client.get("/")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
    
    def test_health_check_endpoint(self, client):
        """
        Test health check endpoint.
        
        Verifies:
        - Health endpoint returns healthy status
        """
        response = client.get("/health")
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_crud_complete_workflow(self, client):
        """
        Test complete CRUD workflow.
        
        Verifies:
        - Create → Read → Update → Delete workflow works correctly
        """
        # Create
        child_data = {
            "document": 555555,
            "name": "Test User",
            "age": 8,
            "guardian": "Test Guardian"
        }
        
        create_response = client.post("/children", json=child_data)
        assert create_response.status_code == 201
        
        # Read
        read_response = client.get("/children/555555")
        assert read_response.status_code == 200
        assert read_response.json()["name"] == "Test User"
        
        # Update
        update_response = client.put(
            "/children/555555",
            json={"name": "Updated User"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated User"
        
        # Delete
        delete_response = client.delete("/children/555555")
        assert delete_response.status_code == 200
        
        # Verify deletion
        final_response = client.get("/children/555555")
        assert final_response.status_code == 404
