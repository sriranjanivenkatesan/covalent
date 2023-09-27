# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the Apache License 2.0 (the "License"). A copy of the
# License may be obtained with this software package or at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Use of this file is prohibited except in compliance with the License.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""v11

Revision ID: 9b9d58f02985
Revises: b60c5ecdf927
Create Date: 2022-08-01 17:57:39.385604

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
# pragma: allowlist nextline secret
revision = "9b9d58f02985"
# pragma: allowlist nextline secret
down_revision = "b60c5ecdf927"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("electrons", schema=None) as batch_op:
        batch_op.add_column(sa.Column("executor", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("executor_data_filename", sa.Text(), nullable=True))
        batch_op.drop_column("key_filename")
        batch_op.drop_column("executor_filename")
        batch_op.drop_column("attribute_name")

    with op.batch_alter_table("lattices", schema=None) as batch_op:
        batch_op.add_column(sa.Column("executor", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("executor_data_filename", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("workflow_executor", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("workflow_executor_data_filename", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("named_args_filename", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("named_kwargs_filename", sa.Text(), nullable=True))
        batch_op.drop_column("executor_filename")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("lattices", schema=None) as batch_op:
        batch_op.add_column(sa.Column("executor_filename", sa.TEXT(), nullable=True))
        batch_op.drop_column("named_kwargs_filename")
        batch_op.drop_column("named_args_filename")
        batch_op.drop_column("workflow_executor_data_filename")
        batch_op.drop_column("workflow_executor")
        batch_op.drop_column("executor_data_filename")
        batch_op.drop_column("executor")

    with op.batch_alter_table("electrons", schema=None) as batch_op:
        batch_op.add_column(sa.Column("attribute_name", sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column("executor_filename", sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column("key_filename", sa.TEXT(), nullable=True))
        batch_op.drop_column("executor_data_filename")
        batch_op.drop_column("executor")

    # ### end Alembic commands ###
