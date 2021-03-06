"""email list model added

Revision ID: 27bc8fbca63b
Revises: 0c0eb6c85a84
Create Date: 2021-04-24 15:28:46.177966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27bc8fbca63b'
down_revision = '0c0eb6c85a84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emaillists ',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('total_emails', sa.Integer(), nullable=True),
    sa.Column('total_unique_emails', sa.Integer(), nullable=True),
    sa.Column('date_uploaded', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('emaillists ')
    # ### end Alembic commands ###
