"""Create ClientFamily table

Revision ID: fad5fed89588
Revises: ac7eab643e37
Create Date: 2021-02-24 15:40:11.884817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fad5fed89588'
down_revision = 'ac7eab643e37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client_family',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_family_name', sa.String(), nullable=True),
    sa.Column('client_family_phone', sa.Integer(), nullable=True),
    sa.Column('client_family_birthday', sa.String(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_client_family_client_family_birthday'), 'client_family', ['client_family_birthday'], unique=False)
    op.create_index(op.f('ix_client_family_client_family_name'), 'client_family', ['client_family_name'], unique=False)
    op.create_index(op.f('ix_client_family_client_family_phone'), 'client_family', ['client_family_phone'], unique=True)
    op.add_column('client', sa.Column('client_registration', sa.DateTime(), nullable=True))
    op.drop_index('ix_client_client_birthday', table_name='client')
    op.create_index(op.f('ix_client_client_birthday'), 'client', ['client_birthday'], unique=False)
    op.drop_index('ix_client_client_name', table_name='client')
    op.create_index(op.f('ix_client_client_name'), 'client', ['client_name'], unique=False)
    op.create_index(op.f('ix_client_client_registration'), 'client', ['client_registration'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_client_client_registration'), table_name='client')
    op.drop_index(op.f('ix_client_client_name'), table_name='client')
    op.create_index('ix_client_client_name', 'client', ['client_name'], unique=1)
    op.drop_index(op.f('ix_client_client_birthday'), table_name='client')
    op.create_index('ix_client_client_birthday', 'client', ['client_birthday'], unique=1)
    op.drop_column('client', 'client_registration')
    op.drop_index(op.f('ix_client_family_client_family_phone'), table_name='client_family')
    op.drop_index(op.f('ix_client_family_client_family_name'), table_name='client_family')
    op.drop_index(op.f('ix_client_family_client_family_birthday'), table_name='client_family')
    op.drop_table('client_family')
    # ### end Alembic commands ###