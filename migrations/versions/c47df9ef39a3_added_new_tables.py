"""added new tables

Revision ID: c47df9ef39a3
Revises: 27bc8fbca63b
Create Date: 2021-04-27 16:19:35.979201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c47df9ef39a3'
down_revision = '27bc8fbca63b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emaillists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('total_emails', sa.Integer(), nullable=True),
    sa.Column('total_unique_emails', sa.Integer(), nullable=True),
    sa.Column('date_uploaded', sa.DateTime(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('date_verified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('validationresults',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_address', sa.String(), nullable=True),
    sa.Column('email_list_id', sa.Integer(), nullable=True),
    sa.Column('is_free', sa.Boolean(), nullable=True),
    sa.Column('is_syntax', sa.Boolean(), nullable=True),
    sa.Column('is_domain', sa.Boolean(), nullable=True),
    sa.Column('is_smtp', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('is_server_down', sa.Boolean(), nullable=True),
    sa.Column('is_greylisted', sa.Boolean(), nullable=True),
    sa.Column('is_disposable', sa.Boolean(), nullable=True),
    sa.Column('is_suppressed', sa.Boolean(), nullable=True),
    sa.Column('is_role', sa.Boolean(), nullable=True),
    sa.Column('is_high_risk', sa.Boolean(), nullable=True),
    sa.Column('is_catchall', sa.Boolean(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('mailboxvalidator_score', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['email_list_id'], ['emaillists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('emaillists ')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emaillists ',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('file_name', sa.VARCHAR(), nullable=False),
    sa.Column('owner_id', sa.INTEGER(), nullable=True),
    sa.Column('total_emails', sa.INTEGER(), nullable=True),
    sa.Column('total_unique_emails', sa.INTEGER(), nullable=True),
    sa.Column('date_uploaded', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('validationresults')
    op.drop_table('emaillists')
    # ### end Alembic commands ###
