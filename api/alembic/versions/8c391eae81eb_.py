"""empty message

Revision ID: 8c391eae81eb
Revises: 99615f987cda
Create Date: 2022-10-07 14:50:20.634168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c391eae81eb'
down_revision = '99615f987cda'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('publications', sa.Column('image_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('publications', 'image_url')
    # ### end Alembic commands ###
