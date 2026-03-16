import pytest

class TestThresholdsService:
    """Unit tests for Thresholds Service"""
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Thresholds Service API"
        assert response.json()["version"] == "1.0.0"
    
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """Test health check endpoint"""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_create_threshold(self, client):
        """Test threshold creation"""
        threshold_data = {
            "threshold_type": "temperature",
            "level": "medium",
            "min_value": 10.0,
            "max_value": 50.0
        }
        response = await client.post("/api/v1/thresholds/", json=threshold_data)
        assert response.status_code == 201
        data = response.json()
        assert data["threshold_id"] == 1
        assert data["threshold_type"] == "temperature"
        assert data["level"] == "medium"
        assert float(data["min_value"]) == 10.0
        assert float(data["max_value"]) == 50.0
    
    @pytest.mark.asyncio
    async def test_create_threshold_invalid_values(self, client):
        """Test creating threshold with invalid values"""
        threshold_data = {
            "threshold_type": "temperature",
            "level": "medium",
            "min_value": 100.0,  # max_value보다 큼
            "max_value": 50.0
        }
        response = await client.post("/api/v1/thresholds/", json=threshold_data)
        assert response.status_code == 422  # Pydantic validation error
        assert "max_value must be greater than min_value" in response.json()["detail"][0]["msg"]
    
    @pytest.mark.asyncio
    async def test_get_thresholds_empty(self, client):
        """Test getting thresholds when list is empty"""
        response = await client.get("/api/v1/thresholds/")
        assert response.status_code == 200
        assert response.json() == []
    
    @pytest.mark.asyncio
    async def test_get_thresholds_with_data(self, client):
        """Test getting thresholds when data exists"""
        # Create test data
        threshold_data = {
            "threshold_type": "temperature",
            "level": "medium",
            "min_value": 10.0,
            "max_value": 50.0
        }
        await client.post("/api/v1/thresholds/", json=threshold_data)
        
        response = await client.get("/api/v1/thresholds/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["threshold_type"] == "temperature"
    
    @pytest.mark.asyncio
    async def test_get_threshold_by_id(self, client):
        """Test getting threshold by id"""
        # Create test data
        threshold_data = {
            "threshold_type": "temperature",
            "level": "medium",
            "min_value": 10.0,
            "max_value": 50.0
        }
        create_response = await client.post("/api/v1/thresholds/", json=threshold_data)
        threshold_id = create_response.json()["threshold_id"]
        
        response = await client.get(f"/api/v1/thresholds/{threshold_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["threshold_id"] == threshold_id
        assert data["threshold_type"] == "temperature"
    
    @pytest.mark.asyncio
    async def test_get_threshold_by_id_not_found(self, client):
        """Test getting threshold by non-existent id"""
        response = await client.get("/api/v1/thresholds/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Threshold not found"
    
    @pytest.mark.asyncio
    async def test_update_threshold(self, client):
        """Test updating threshold"""
        # Create test data
        threshold_data = {
            "threshold_type": "temperature",
            "level": "medium",
            "min_value": 10.0,
            "max_value": 50.0
        }
        create_response = await client.post("/api/v1/thresholds/", json=threshold_data)
        threshold_id = create_response.json()["threshold_id"]
        
        # Data to update
        update_data = {
            "min_value": 15.0,
            "max_value": 60.0,
            "level": "high"
        }
        
        response = await client.put(f"/api/v1/thresholds/{threshold_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["threshold_id"] == threshold_id
        assert float(data["min_value"]) == 15.0
        assert float(data["max_value"]) == 60.0
        assert data["level"] == "high"
    
    @pytest.mark.asyncio
    async def test_update_threshold_not_found(self, client):
        """Test updating non-existent threshold"""
        update_data = {
            "min_value": 15.0,
            "max_value": 60.0
        }
        
        response = await client.put("/api/v1/thresholds/999", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Threshold not found"
    
    @pytest.mark.asyncio
    async def test_delete_threshold(self, client):
        """Test deleting threshold"""
        # Create test data
        threshold_data = {
            "threshold_type": "temperature",
            "level": "medium",
            "min_value": 10.0,
            "max_value": 50.0
        }
        create_response = await client.post("/api/v1/thresholds/", json=threshold_data)
        threshold_id = create_response.json()["threshold_id"]
        
        response = await client.delete(f"/api/v1/thresholds/{threshold_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Threshold {threshold_id} deleted"
        assert data["deleted"]["threshold_id"] == threshold_id
        
        # Verify deletion
        get_response = await client.get(f"/api/v1/thresholds/{threshold_id}")
        assert get_response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_delete_threshold_not_found(self, client):
        """Test deleting non-existent threshold"""
        response = await client.delete("/api/v1/thresholds/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Threshold not found"
    
    @pytest.mark.asyncio
    async def test_get_thresholds_by_type(self, client):
        """Test getting thresholds filtered by type"""
        # Create test data
        threshold_data_1 = {
            "threshold_type": "temperature",
            "level": "medium",
            "min_value": 10.0,
            "max_value": 50.0
        }
        threshold_data_2 = {
            "threshold_type": "temperature",
            "level": "high",
            "min_value": 20.0,
            "max_value": 60.0
        }
        threshold_data_3 = {
            "threshold_type": "humidity",
            "level": "low",
            "min_value": 5.0,
            "max_value": 30.0
        }
        
        await client.post("/api/v1/thresholds/", json=threshold_data_1)
        await client.post("/api/v1/thresholds/", json=threshold_data_2)
        await client.post("/api/v1/thresholds/", json=threshold_data_3)
        
        response = await client.get("/api/v1/thresholds/type/temperature")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(t["threshold_type"] == "temperature" for t in data)
    
    @pytest.mark.asyncio
    async def test_get_thresholds_by_type_empty(self, client):
        """Test getting thresholds by type when result is empty"""
        response = await client.get("/api/v1/thresholds/type/nonexistent_type")
        assert response.status_code == 200
        assert response.json() == []
    
    @pytest.mark.asyncio
    async def test_threshold_type_validation(self, client):
        """Test threshold_type validation"""
        # Valid threshold_type values (as defined in Enum)
        valid_types = ["temperature", "humidity", "pcv_temperature"]
        
        for threshold_type in valid_types:
            threshold_data = {
                "threshold_type": threshold_type,
                "level": "medium",
                "min_value": 10.0,
                "max_value": 50.0
            }
            response = await client.post("/api/v1/thresholds/", json=threshold_data)
            assert response.status_code == 201
            assert response.json()["threshold_type"] == threshold_type