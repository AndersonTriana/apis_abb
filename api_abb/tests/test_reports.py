"""
Integration tests for the Reports API endpoints.
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


@pytest.fixture
def sample_children(client):
    """Create sample children for testing."""
    children = [
        {
            "documento": 1001,
            "nombre": "Juan Pérez",
            "edad": 10,
            "ciudad": "Bogotá",
            "genero": "Masculino"
        },
        {
            "documento": 1002,
            "nombre": "María García",
            "edad": 8,
            "ciudad": "Bogotá",
            "genero": "Femenino"
        },
        {
            "documento": 1003,
            "nombre": "Carlos López",
            "edad": 12,
            "ciudad": "Medellín",
            "genero": "Masculino"
        },
        {
            "documento": 1004,
            "nombre": "Ana Martínez",
            "edad": 7,
            "ciudad": "Medellín",
            "genero": "Femenino"
        },
        {
            "documento": 1005,
            "nombre": "Pedro Rodríguez",
            "edad": 9,
            "ciudad": "Medellín",
            "genero": "Masculino"
        },
        {
            "documento": 1006,
            "nombre": "Laura Sánchez",
            "edad": 11,
            "ciudad": "Cali",
            "genero": "Femenino"
        },
        {
            "documento": 1007,
            "nombre": "Diego Torres",
            "edad": 6,
            "ciudad": "Bogotá",
            "genero": "Masculino"
        },
        {
            "documento": 1008,
            "nombre": "Sofia Ramírez",
            "edad": 10,
            "ciudad": "Cali",
            "genero": "Femenino"
        }
    ]
    
    for child in children:
        client.post("/children", json=child)
    
    return children


class TestChildrenByCityReport:
    """Tests for GET /reports/children-by-city endpoint."""
    
    def test_report_empty_tree(self, client):
        """Test report with no children in the tree."""
        response = client.get("/reports/children-by-city")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_report_single_city_single_gender(self, client):
        """Test report with children from one city and one gender."""
        # Create children
        children = [
            {"documento": 2001, "nombre": "Child 1", "edad": 10, "ciudad": "Manizales", "genero": "Masculino"},
            {"documento": 2002, "nombre": "Child 2", "edad": 8, "ciudad": "Manizales", "genero": "Masculino"},
        ]
        
        for child in children:
            client.post("/children", json=child)
        
        response = client.get("/reports/children-by-city")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["ciudad"] == "Manizales"
        assert data[0]["masculino"] == 2
        assert data[0]["femenino"] == 0
        assert data[0]["total"] == 2
    
    def test_report_single_city_both_genders(self, client):
        """Test report with children from one city with both genders."""
        children = [
            {"documento": 3001, "nombre": "Boy 1", "edad": 10, "ciudad": "Pereira", "genero": "Masculino"},
            {"documento": 3002, "nombre": "Girl 1", "edad": 8, "ciudad": "Pereira", "genero": "Femenino"},
            {"documento": 3003, "nombre": "Boy 2", "edad": 9, "ciudad": "Pereira", "genero": "Masculino"},
        ]
        
        for child in children:
            client.post("/children", json=child)
        
        response = client.get("/reports/children-by-city")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["ciudad"] == "Pereira"
        assert data[0]["masculino"] == 2
        assert data[0]["femenino"] == 1
        assert data[0]["total"] == 3
    
    def test_report_multiple_cities(self, client, sample_children):
        """Test report with children from multiple cities."""
        response = client.get("/reports/children-by-city")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have 3 cities: Bogotá, Cali, Medellín
        assert len(data) == 3
        
        # Verify data is sorted alphabetically by city
        cities = [item["ciudad"] for item in data]
        assert cities == ["Bogotá", "Cali", "Medellín"]
        
        # Verify Bogotá stats (2 Masculino, 1 Femenino)
        bogota = next(item for item in data if item["ciudad"] == "Bogotá")
        assert bogota["masculino"] == 2
        assert bogota["femenino"] == 1
        assert bogota["total"] == 3
        
        # Verify Cali stats (0 Masculino, 2 Femenino)
        cali = next(item for item in data if item["ciudad"] == "Cali")
        assert cali["masculino"] == 0
        assert cali["femenino"] == 2
        assert cali["total"] == 2
        
        # Verify Medellín stats (2 Masculino, 1 Femenino)
        medellin = next(item for item in data if item["ciudad"] == "Medellín")
        assert medellin["masculino"] == 2
        assert medellin["femenino"] == 1
        assert medellin["total"] == 3
    
    def test_report_structure(self, client):
        """Test that report response has correct structure."""
        # Create a child
        child = {
            "documento": 4001,
            "nombre": "Test Child",
            "edad": 10,
            "ciudad": "Barranquilla",
            "genero": "Femenino"
        }
        client.post("/children", json=child)
        
        response = client.get("/reports/children-by-city")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        
        # Verify all required fields are present
        report_item = data[0]
        assert "ciudad" in report_item
        assert "masculino" in report_item
        assert "femenino" in report_item
        assert "total" in report_item
        
        # Verify field types
        assert isinstance(report_item["ciudad"], str)
        assert isinstance(report_item["masculino"], int)
        assert isinstance(report_item["femenino"], int)
        assert isinstance(report_item["total"], int)
    
    def test_report_after_deletion(self, client):
        """Test that report updates correctly after deleting children."""
        # Create children
        children = [
            {"documento": 5001, "nombre": "Child 1", "edad": 10, "ciudad": "Cartagena", "genero": "Masculino"},
            {"documento": 5002, "nombre": "Child 2", "edad": 8, "ciudad": "Cartagena", "genero": "Masculino"},
            {"documento": 5003, "nombre": "Child 3", "edad": 9, "ciudad": "Cartagena", "genero": "Femenino"},
        ]
        
        for child in children:
            client.post("/children", json=child)
        
        # Get initial report
        response = client.get("/reports/children-by-city")
        data = response.json()
        assert data[0]["total"] == 3
        assert data[0]["masculino"] == 2
        
        # Delete one masculine child
        client.delete("/children/5001")
        
        # Get updated report
        response = client.get("/reports/children-by-city")
        data = response.json()
        assert data[0]["total"] == 2
        assert data[0]["masculino"] == 1
        assert data[0]["femenino"] == 1
    
    def test_report_after_update(self, client):
        """Test that report updates correctly after updating child gender."""
        # Create a child
        child = {
            "documento": 6001,
            "nombre": "Test Child",
            "edad": 10,
            "ciudad": "Bucaramanga",
            "genero": "Masculino"
        }
        client.post("/children", json=child)
        
        # Initial report
        response = client.get("/reports/children-by-city")
        data = response.json()
        assert data[0]["masculino"] == 1
        assert data[0]["femenino"] == 0
        
        # Update gender
        client.put("/children/6001", json={"genero": "Femenino"})
        
        # Updated report
        response = client.get("/reports/children-by-city")
        data = response.json()
        assert data[0]["masculino"] == 0
        assert data[0]["femenino"] == 1
