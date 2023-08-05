#   Copyright 2020 Intentionet
#
#   Licensed under the proprietary License included with this package;
#   you may not use this file except in compliance with the License.
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""Contains internal functions for interacting with the Batfish Enterprise service."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union  # noqa: F401

from pybatfish.client.consts import CoordConsts
from pybatfish.client.options import Options
from pybatfish.datamodel.answer import Answer  # noqa: F401
from pybatfish.util import get_uuid

from . import resthelper, restv2helper, workhelper

if TYPE_CHECKING:
    from pybfe.client.session import Session  # noqa: F401


def _bf_answer_obj(
    session: "Session",
    question_str: str,
    question_name: str,
    background: bool,
    snapshot: str,
    reference_snapshot: Optional[str],
    extra_args: Optional[Dict[str, Any]],
) -> Union[Answer, str]:
    if not question_name:
        question_name = Options.default_question_prefix + "_" + get_uuid()

    # Upload the question
    json_data = workhelper.get_data_upload_question(
        session, question_name, question_str
    )
    resthelper.get_json_response(
        session,
        CoordConsts.SVC_RSC_UPLOAD_QUESTION,
        json_data,
        CoordConsts.SVC_KEY_FILE,
    )

    # Answer the question
    work_item = workhelper.get_workitem_answer(
        session, question_name, snapshot, reference_snapshot
    )
    workhelper.execute(work_item, session, background, extra_args)

    if background:
        return work_item.id

    # get the answer
    return session.get_answer(question_name, snapshot, reference_snapshot)


def _bf_get_question_templates(session: "Session", verbose: bool = False) -> Dict:
    return restv2helper.get_question_templates(session, verbose)
