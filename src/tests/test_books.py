import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.main import app
from src.services.books import SellerService
from src.schemas.seller import SellerCreate

@pytest.mark.asyncio
async def test_create_seller(async_client: AsyncClient, db_session: AsyncSession):
    response = await async_client.post("/api/v1/seller", json={
        "first_name": "Test",
        "last_name": "User",
        "e_mail": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"
    assert data["e_mail"] == "test@example.com"
    assert "id" in data
    assert "password" not in data

@pytest.mark.asyncio
async def test_create_seller_duplicate_email(async_client: AsyncClient, db_session: AsyncSession):
    # Create first seller
    await async_client.post("/api/v1/seller", json={
        "first_name": "Test",
        "last_name": "User",
        "e_mail": "duplicate@example.com",
        "password": "testpass123"
    })
    
    # Try to create another with same email
    response = await async_client.post("/api/v1/seller", json={
        "first_name": "Another",
        "last_name": "User",
        "e_mail": "duplicate@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_get_sellers(async_client: AsyncClient, db_session: AsyncSession):
    # Create test sellers
    await async_client.post("/api/v1/seller", json={
        "first_name": "User1",
        "last_name": "Test",
        "e_mail": "user1@example.com",
        "password": "pass123"
    })
    await async_client.post("/api/v1/seller", json={
        "first_name": "User2",
        "last_name": "Test",
        "e_mail": "user2@example.com",
        "password": "pass123"
    })
    
    response = await async_client.get("/api/v1/seller")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "password" not in data[0]

@pytest.mark.asyncio
async def test_get_seller_by_id(async_client: AsyncClient, db_session: AsyncSession):
    # Create seller
    create_resp = await async_client.post("/api/v1/seller", json={
        "first_name": "Specific",
        "last_name": "User",
        "e_mail": "specific@example.com",
        "password": "pass123"
    })
    seller_id = create_resp.json()["id"]
    
    # Get seller by ID
    response = await async_client.get(f"/api/v1/seller/{seller_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Specific"
    assert data["last_name"] == "User"
    assert data["e_mail"] == "specific@example.com"
    assert "books" in data
    assert "password" not in data

@pytest.mark.asyncio
async def test_login_and_create_book(async_client: AsyncClient, db_session: AsyncSession):
    # Create seller
    seller_resp = await async_client.post("/api/v1/seller", json={
        "first_name": "Auth",
        "last_name": "User",
        "e_mail": "auth@example.com",
        "password": "authpass123"
    })
    seller_id = seller_resp.json()["id"]
    
    # Login to get token
    login_resp = await async_client.post("/api/v1/token", data={
        "username": "auth@example.com",
        "password": "authpass123"
    })
    assert login_resp.status_code == 200
    token_data = login_resp.json()
    assert "access_token" in token_data
    token = token_data["access_token"]
    
    # Create book with token
    book_resp = await async_client.post("/api/v1/books", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Authored Book",
            "author": "Famous Author",
            "year": 2023,
            "price": 39.99,
            "seller_id": seller_id
        }
    )
    assert book_resp.status_code == 201
    book_data = book_resp.json()
    assert book_data["title"] == "Authored Book"
    assert book_data["seller_id"] == seller_id

@pytest.mark.asyncio
async def test_update_seller_authorized(async_client: AsyncClient, db_session: AsyncSession):
    # Create seller
    seller_resp = await async_client.post("/api/v1/seller", json={
        "first_name": "Update",
        "last_name": "Auth",
        "e_mail": "update.auth@example.com",
        "password": "pass123"
    })
    seller_id = seller_resp.json()["id"]
    
    # Login
    login_resp = await async_client.post("/api/v1/token", data={
        "username": "update.auth@example.com",
        "password": "pass123"
    })
    token = login_resp.json()["access_token"]
    
    # Update seller
    response = await async_client.put(f"/api/v1/seller/{seller_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "first_name": "Updated Successfully",
            "last_name": "Changed"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated Successfully"
    assert data["last_name"] == "Changed"
    assert data["e_mail"] == "update.auth@example.com"

@pytest.mark.asyncio
async def test_delete_seller(async_client: AsyncClient, db_session: AsyncSession):
    # Create seller
    seller_resp = await async_client.post("/api/v1/seller", json={
        "first_name": "Delete",
        "last_name": "Me",
        "e_mail": "delete@example.com",
        "password": "pass123"
    })
    seller_id = seller_resp.json()["id"]
    
    # Login
    login_resp = await async_client.post("/api/v1/token", data={
        "username": "delete@example.com",
        "password": "pass123"
    })
    token = login_resp.json()["access_token"]
    
    # Delete seller
    response = await async_client.delete(f"/api/v1/seller/{seller_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
    
    # Verify seller is gone
    get_resp = await async_client.get(f"/api/v1/seller/{seller_id}")
    assert get_resp.status_code == 404