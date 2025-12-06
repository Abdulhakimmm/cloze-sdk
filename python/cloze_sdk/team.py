"""
Team endpoints for the Cloze API.

Copyright (C) 2025 Cloze SDK Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Any, Dict, List


class Team:
    """Team endpoints."""

    def __init__(self, client):
        self.client = client

    def list_members(self) -> Dict[str, Any]:
        """
        List team members.

        Returns:
            List of team members
        """
        return self.client._make_request("GET", "/v1/team/members/list")

    def update_members(self, members: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update team members.

        Args:
            members: List of team member updates.

        Returns:
            Update result
        """
        return self.client._make_request(
            "POST", "/v1/team/members/update", json_data={"members": members}
        )

    def get_nodes(self) -> Dict[str, Any]:
        """
        Get team organizational nodes.

        Returns:
            Team nodes structure
        """
        return self.client._make_request("GET", "/v1/team/nodes")

    def get_roles(self) -> Dict[str, Any]:
        """
        Get team roles.

        Returns:
            List of team roles with names and IDs
        """
        return self.client._make_request("GET", "/v1/team/roles")
