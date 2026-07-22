# SPDX-FileCopyrightText: (C) 2026 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from http import HTTPStatus
from unittest.mock import MagicMock

import pytest

from src.rest_api.endpoints import Endpoints
from src.server.pipeline import ElementPropertyRollbackError, PipelineNotRunningError


def test_update_element_properties_endpoint(mocker):
    request = MagicMock(is_json=True)
    request.get_json.return_value = {"properties": {"zoom": 2.0}}
    mocker.patch("src.rest_api.endpoints.connexion.request", request)
    manager = MagicMock()
    manager.update_element_properties.return_value = {
        "id": "instance_123",
        "element": "renderer",
        "properties": {"zoom": 2.0},
    }
    mocker.patch.object(Endpoints, "pipeline_server_manager", manager)

    result = Endpoints.pipelines_instance_id_elements_element_name_properties_patch(
        "instance_123", "renderer"
    )

    assert result == {
        "id": "instance_123",
        "element": "renderer",
        "properties": {"zoom": 2.0},
    }
    manager.update_element_properties.assert_called_once_with(
        "instance_123", "renderer", {"zoom": 2.0}
    )


@pytest.mark.parametrize(
    "error, expected_status",
    [
        (KeyError("missing"), HTTPStatus.NOT_FOUND),
        (ValueError("invalid"), HTTPStatus.BAD_REQUEST),
        (PipelineNotRunningError("stopped"), HTTPStatus.CONFLICT),
        (
            ElementPropertyRollbackError("rollback"),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
        (TimeoutError("timeout"), HTTPStatus.GATEWAY_TIMEOUT),
    ],
)
def test_update_element_properties_endpoint_error_status(
    mocker, error, expected_status
):
    request = MagicMock(is_json=True)
    request.get_json.return_value = {"properties": {"zoom": 2.0}}
    mocker.patch("src.rest_api.endpoints.connexion.request", request)
    manager = MagicMock()
    manager.update_element_properties.side_effect = error
    mocker.patch.object(Endpoints, "pipeline_server_manager", manager)

    _, status = Endpoints.pipelines_instance_id_elements_element_name_properties_patch(
        "instance_123", "renderer"
    )

    assert status == expected_status