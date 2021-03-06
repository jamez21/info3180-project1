"""empty message

Revision ID: 07b8969ff79e
Revises: 6cd501786127
Create Date: 2017-03-13 05:06:23.830505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07b8969ff79e'
down_revision = '6cd501786127'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'gender')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('gender', sa.VARCHAR(length=1), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
