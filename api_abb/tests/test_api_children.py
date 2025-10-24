"""
Integration tests for the Children API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from api_abb.main import app
from api_abb.service.child_service import get_child_service


@pytest.fixture(autouse=True)
def clear_service():
    """Clear the child service before each test."""
    service = get_child_service()
    service.clear_all()
    yield
    service.clear_all()


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestCreateChild:
    """Tests for POST /children endpoint."""
    
    def test_create_child_success(self, client):
        """Test creating a child successfully."""
        child_data = {
            "documento": 1234567890,
            "nombre": "Juan Pérez",
            "edad": 10,
            "ciudad": "Bogotá",
            "genero": "Masculino",
            "acudiente": "María Pérez",
            "notas": "Alérgico al maní"
        }
        
        response = client.post("/children", json=child_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["documento"] == 1234567890
        assert data["nombre"] == "Juan Pérez"
        assert data["edad"] == 10
        assert data["ciudad"] == "Bogotá"
        assert data["genero"] == "Masculino"
        assert data["acudiente"] == "María Pérez"
        assert data["notas"] == "Alérgico al maní"
    
    def test_create_child_minimal_data(self, client):
        """Test creating a child with minimal required data."""
        child_data = {
            "documento": 9876543210,
            "nombre": "Ana García",
            "edad": 5,
            "ciudad": "Medellín",
            "genero": "Femenino"
        }
        
        response = client.post("/children", json=child_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["documento"] == 9876543210
        assert data["nombre"] == "Ana García"
        assert data["edad"] == 5
        assert data["ciudad"] == "Medellín"
        assert data["genero"] == "Femenino"
        assert data["acudiente"] is None
        assert data["notas"] is None
    
    def test_create_child_duplicate_documento(self, client):
        """Test creating a child with duplicate documento."""
        child_data = {
            "documento": 1111111111,
            "nombre": "Test Child",
            "edad": 8,
            "ciudad": "Cali",
            "genero": "Masculino"
        }
        
        # First creation should succeed
        response1 = client.post("/children", json=child_data)
        assert response1.status_code == 201
        
        # Second creation with same documento should fail
        response2 = client.post("/children", json=child_data)
        assert response2.status_code == 400
        assert "Ya existe" in response2.json()["detail"]
    
    def test_create_child_invalid_edad(self, client):
        """Test creating a child with invalid age."""
        child_data = {
            "documento": 2222222222,
            "nombre": "Invalid Age",
            "edad": 25,  # Age > 18
            "ciudad": "Barranquilla",
            "genero": "Masculino"
        }
        
        response = client.post("/children", json=child_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_child_invalid_genero(self, client):
        """Test creating a child with invalid genero."""
        child_data = {
            "documento": 2222222223,
            "nombre": "Invalid Genero",
            "edad": 10,
            "ciudad": "Barranquilla",
            "genero": "Otro"  # Invalid genero value
        }
        
        response = client.post("/children", json=child_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_child_missing_required_fields(self, client):
        """Test creating a child without required fields."""
        child_data = {
            "documento": 3333333333
            # Missing nombre, edad, ciudad, and genero
        }
        
        response = client.post("/children", json=child_data)
        assert response.status_code == 422


class TestGetChild:
    """Tests for GET /children/{documento} endpoint."""
    
    def test_get_existing_child(self, client):
        """Test getting an existing child."""
        # Create a child first
        child_data = {
            "documento": 4444444444,
            "nombre": "Carlos López",
            "edad": 12,
            "ciudad": "Cartagena",
            "genero": "Masculino"
        }
        client.post("/children", json=child_data)
        
        # Get the child
        response = client.get("/children/4444444444")
        
        assert response.status_code == 200
        data = response.json()
        assert data["documento"] == 4444444444
        assert data["nombre"] == "Carlos López"
        assert data["edad"] == 12
        assert data["ciudad"] == "Cartagena"
        assert data["genero"] == "Masculino"
    
    def test_get_non_existing_child(self, client):
        """Test getting a non-existing child."""
        response = client.get("/children/9999999999")
        
        assert response.status_code == 404
        assert "No se encontró" in response.json()["detail"]


class TestGetAllChildren:
    """Tests for GET /children endpoint."""
    
    def test_get_all_children_empty(self, client):
        """Test getting all children when tree is empty."""
        response = client.get("/children")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_children_inorder(self, client):
        """Test getting all children in inorder (sorted by documento)."""
        # Create multiple children
        children = [
            {"documento": 5000, "nombre": "Child 5000", "edad": 10, "ciudad": "Bogotá", "genero": "Masculino"},
            {"documento": 3000, "nombre": "Child 3000", "edad": 8, "ciudad": "Medellín", "genero": "Femenino"},
            {"documento": 7000, "nombre": "Child 7000", "edad": 12, "ciudad": "Cali", "genero": "Masculino"},
            {"documento": 2000, "nombre": "Child 2000", "edad": 6, "ciudad": "Barranquilla", "genero": "Femenino"},
            {"documento": 4000, "nombre": "Child 4000", "edad": 9, "ciudad": "Cartagena", "genero": "Masculino"},
        ]
        
        for child in children:
            client.post("/children", json=child)
        
        # Get all children in inorder (default)
        response = client.get("/children?order=in")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        
        # Should be sorted by documento
        documentos = [child["documento"] for child in data]
        assert documentos == [2000, 3000, 4000, 5000, 7000]
    
    def test_get_all_children_preorder(self, client):
        """Test getting all children in preorder."""
        children = [
            {"documento": 5000, "nombre": "Child 5000", "edad": 10, "ciudad": "Bogotá", "genero": "Masculino"},
            {"documento": 3000, "nombre": "Child 3000", "edad": 8, "ciudad": "Medellín", "genero": "Femenino"},
            {"documento": 7000, "nombre": "Child 7000", "edad": 12, "ciudad": "Cali", "genero": "Masculino"},
        ]
        
        for child in children:
            client.post("/children", json=child)
        
        response = client.get("/children?order=pre")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Preorder: root, left, right
        documentos = [child["documento"] for child in data]
        assert documentos == [5000, 3000, 7000]
    
    def test_get_all_children_postorder(self, client):
        """Test getting all children in postorder."""
        children = [
            {"documento": 5000, "nombre": "Child 5000", "edad": 10, "ciudad": "Bogotá", "genero": "Masculino"},
            {"documento": 3000, "nombre": "Child 3000", "edad": 8, "ciudad": "Medellín", "genero": "Femenino"},
            {"documento": 7000, "nombre": "Child 7000", "edad": 12, "ciudad": "Cali", "genero": "Masculino"},
        ]
        
        for child in children:
            client.post("/children", json=child)
        
        response = client.get("/children?order=post")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Postorder: left, right, root
        documentos = [child["documento"] for child in data]
        assert documentos == [3000, 7000, 5000]
    
    def test_get_all_children_invalid_order(self, client):
        """Test getting all children with invalid order parameter."""
        response = client.get("/children?order=invalid")
        
        assert response.status_code == 422  # Validation error


class TestUpdateChild:
    """Tests for PUT /children/{documento} endpoint."""
    
    def test_update_child_all_fields(self, client):
        """Test updating all fields of a child."""
        # Create a child
        child_data = {
            "documento": 6000,
            "nombre": "Original Name",
            "edad": 10,
            "ciudad": "Bogotá",
            "genero": "Masculino",
            "acudiente": "Original Acudiente"
        }
        client.post("/children", json=child_data)
        
        # Update the child
        update_data = {
            "nombre": "Updated Name",
            "edad": 11,
            "ciudad": "Medellín",
            "genero": "Femenino",
            "acudiente": "Updated Acudiente",
            "notas": "New notes"
        }
        response = client.put("/children/6000", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["documento"] == 6000  # Documento unchanged
        assert data["nombre"] == "Updated Name"
        assert data["edad"] == 11
        assert data["ciudad"] == "Medellín"
        assert data["genero"] == "Femenino"
        assert data["acudiente"] == "Updated Acudiente"
        assert data["notas"] == "New notes"
    
    def test_update_child_partial_fields(self, client):
        """Test updating only some fields of a child."""
        # Create a child
        child_data = {
            "documento": 7000,
            "nombre": "Original Name",
            "edad": 10,
            "ciudad": "Cali",
            "genero": "Masculino",
            "acudiente": "Original Acudiente"
        }
        client.post("/children", json=child_data)
        
        # Update only edad
        update_data = {
            "edad": 11
        }
        response = client.put("/children/7000", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Original Name"  # Unchanged
        assert data["edad"] == 11  # Updated
        assert data["ciudad"] == "Cali"  # Unchanged
        assert data["genero"] == "Masculino"  # Unchanged
        assert data["acudiente"] == "Original Acudiente"  # Unchanged
    
    def test_update_non_existing_child(self, client):
        """Test updating a non-existing child."""
        update_data = {
            "nombre": "New Name",
            "edad": 10
        }
        response = client.put("/children/9999999999", json=update_data)
        
        assert response.status_code == 404
        assert "No se encontró" in response.json()["detail"]


class TestDeleteChild:
    """Tests for DELETE /children/{documento} endpoint."""
    
    def test_delete_existing_child(self, client):
        """Test deleting an existing child."""
        # Create a child
        child_data = {
            "documento": 8000,
            "nombre": "To Delete",
            "edad": 10,
            "ciudad": "Pereira",
            "genero": "Femenino"
        }
        client.post("/children", json=child_data)
        
        # Delete the child
        response = client.delete("/children/8000")
        
        assert response.status_code == 200
        assert "eliminado exitosamente" in response.json()["message"]
        
        # Verify child is deleted
        get_response = client.get("/children/8000")
        assert get_response.status_code == 404
    
    def test_delete_non_existing_child(self, client):
        """Test deleting a non-existing child."""
        response = client.delete("/children/9999999999")
        
        assert response.status_code == 404
        assert "No se encontró" in response.json()["detail"]


class TestIntegrationScenarios:
    """Integration tests for complex scenarios."""
    
    def test_full_crud_workflow(self, client):
        """Test complete CRUD workflow."""
        # Create
        child_data = {
            "documento": 1000,
            "nombre": "Test Child",
            "edad": 10,
            "ciudad": "Bucaramanga",
            "genero": "Masculino"
        }
        create_response = client.post("/children", json=child_data)
        assert create_response.status_code == 201
        
        # Read
        get_response = client.get("/children/1000")
        assert get_response.status_code == 200
        assert get_response.json()["nombre"] == "Test Child"
        
        # Update
        update_data = {"nombre": "Updated Child"}
        update_response = client.put("/children/1000", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["nombre"] == "Updated Child"
        
        # Delete
        delete_response = client.delete("/children/1000")
        assert delete_response.status_code == 200
        
        # Verify deletion
        final_get = client.get("/children/1000")
        assert final_get.status_code == 404
    
    def test_multiple_children_operations(self, client):
        """Test operations with multiple children."""
        # Create multiple children
        children = [
            {"documento": 100, "nombre": "Child 100", "edad": 5, "ciudad": "Bogotá", "genero": "Masculino"},
            {"documento": 200, "nombre": "Child 200", "edad": 10, "ciudad": "Medellín", "genero": "Femenino"},
            {"documento": 150, "nombre": "Child 150", "edad": 7, "ciudad": "Cali", "genero": "Masculino"},
            {"documento": 50, "nombre": "Child 50", "edad": 3, "ciudad": "Barranquilla", "genero": "Femenino"},
        ]
        
        for child in children:
            response = client.post("/children", json=child)
            assert response.status_code == 201
        
        # Get all in order
        all_response = client.get("/children?order=in")
        assert all_response.status_code == 200
        all_children = all_response.json()
        assert len(all_children) == 4
        
        # Verify sorted order
        documentos = [c["documento"] for c in all_children]
        assert documentos == [50, 100, 150, 200]
        
        # Delete one
        client.delete("/children/150")
        
        # Verify count
        remaining = client.get("/children")
        assert len(remaining.json()) == 3
