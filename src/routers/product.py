from fastapi import APIRouter
from config.database.db_helper import db_helper
from src.models.base_model import Product
from sqlalchemy.future import select
from src.schemas.product import ProductSchema


router = APIRouter()


@router.get("/products/")
async def get_all_products():
    async with db_helper.get_db_session() as db:
        result = await db.execute(select(Product))
        products = result.scalars().all()
        return products


@router.post("/products/")
async def create_product(product: ProductSchema):
    new_product = Product(
        name=product.name,
        price=product.price,
        description=product.description
    )

    async with db_helper.get_db_session() as db:
        db.add(new_product)
        await db.commit()

    return new_product
