"""empty message

Revision ID: f621f3586bee
Revises: 9fc4a26a11db
Create Date: 2022-10-08 14:45:24.589354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f621f3586bee'
down_revision = '9fc4a26a11db'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('topic_info', sa.Column('for_accountant', sa.Boolean(), nullable=True))
    op.add_column('topic_info', sa.Column('for_businessman', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('topic_info', 'for_businessman')
    op.drop_column('topic_info', 'for_accountant')
    # ### end Alembic commands ###
