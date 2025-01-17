"""Initial revision

Revision ID: 4e66d442ce2c
Revises: 
Create Date: 2024-08-21 20:28:45.919177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Table, MetaData


# revision identifiers, used by Alembic.
revision: str = '4e66d442ce2c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def insert_default_categories() -> None:
    metadata = MetaData()
    product_category_table = Table('product_category', metadata, autoload_with=op.get_bind())

    # Вставка начальных данных в таблицу product_category
    op.bulk_insert(
        product_category_table,  # Передаем объект Table
        [
            {'id': 1, 'name': 'Electronics', 'description': 'Electronic devices'},
            {'id': 2, 'name': 'Clothing', 'description': 'Apparel and accessories'},
            {'id': 3, 'name': 'Books', 'description': 'Books and literature'}
        ]
    )


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['product_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    insert_default_categories()


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    op.drop_table('users')
    op.drop_table('product_category')
    # ### end Alembic commands ###
