"""Added has_sent table

Revision ID: a9a78904c117
Revises: 10cd95ce2498
Create Date: 2024-01-31 00:34:06.906250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9a78904c117'
down_revision = '10cd95ce2498'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('mail', sa.String(length=50), nullable=True),
    sa.Column('gender', sa.String(length=1), nullable=False),
    sa.Column('has_pair', sa.Boolean(), nullable=False),
    sa.Column('like', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('has_sent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pairings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('giver_id', sa.Integer(), nullable=False),
    sa.Column('receiver_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['giver_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pairings')
    op.drop_table('has_sent')
    op.drop_table('users')
    # ### end Alembic commands ###
