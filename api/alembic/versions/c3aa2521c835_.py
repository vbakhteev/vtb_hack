"""empty message

Revision ID: c3aa2521c835
Revises: 04ba491e2337
Create Date: 2022-10-08 13:41:38.483111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3aa2521c835'
down_revision = '04ba491e2337'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('topic_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_topic_info_id'), 'topic_info', ['id'], unique=False)
    op.add_column('publications', sa.Column('topic_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'publications', 'topic_info', ['topic_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'publications', type_='foreignkey')
    op.drop_column('publications', 'topic_id')
    op.drop_index(op.f('ix_topic_info_id'), table_name='topic_info')
    op.drop_table('topic_info')
    # ### end Alembic commands ###
