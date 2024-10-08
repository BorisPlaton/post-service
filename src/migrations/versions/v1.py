"""empty message

Revision ID: 975a3fe13a35
Revises: 8ea8f70df2dc
Create Date: 2024-07-14 10:41:13.418246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '975a3fe13a35'
down_revision: Union[str, None] = '8ea8f70df2dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'post',
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('content', sa.String(length=4096), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('blocked', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'post_comment',
        sa.Column('content', sa.String(length=4096), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('blocked', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['post_id'], ['post.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_comment')
    op.drop_table('post')
    # ### end Alembic commands ###
