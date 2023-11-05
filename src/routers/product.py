from fastapi import APIRouter, HTTPException
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


@router.get("/products/{product_id}", response_model=ProductSchema)
async def get_product_by_id(product_id: int):
    async with db_helper.get_db_session() as db:
        product = await db.get(Product, product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product


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


@router.put("/products/{product_id}", response_model=ProductSchema)
async def update_product(product_id: int, updated_product: ProductSchema):
    async with db_helper.get_db_session() as db:
        product = await db.get(Product, product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        for field, value in updated_product.dict().items():
            setattr(product, field, value)

        await db.commit()

    return product


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    try:
        async with db_helper.get_db_session() as db:
            product = await db.get(Product, product_id)
            if product is None:
                raise HTTPException(status_code=404, detail="Product not found")

            await db.delete(product)
            await db.commit()

        return {"message": "Product successfully deleted"}
    except Exception as e:
        return {"error": str(e)}
