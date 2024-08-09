"""empty message

Revision ID: 8c74d0b66935
Revises: 975a3fe13a35
Create Date: 2024-08-03 16:36:42.959541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c74d0b66935'
down_revision: Union[str, None] = '975a3fe13a35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'comment_auto_reply_configuration',
        sa.Column('enabled', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('auto_reply_delay', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.CheckConstraint('auto_reply_delay > 0', name='auto_reply_delay_must_be_positive'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.execute("""
        INSERT INTO comment_auto_reply_configuration (user_id, auto_reply_delay, enabled)
        SELECT "user".id, 60, FALSE FROM "user"
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_auto_reply_configuration')
    # ### end Alembic commands ###
