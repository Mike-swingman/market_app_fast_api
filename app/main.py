from fastapi import FastAPI
from app.users.routers import router as auth_router
from app.products.routers import router as market_router

app = FastAPI(
    title='Market',
    description='An API for market operations, including user authentication and product management.',
    version='0.0.1'
)

app.include_router(auth_router)
app.include_router(market_router)
