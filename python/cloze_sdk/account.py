"""
Account endpoints for the Cloze API.

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

from typing import Dict, Any, Optional


class Account:
    """Account endpoints."""

    def __init__(self, client):
        self.client = client

    def get_fields(self, relationtype: Optional[str] = None) -> Dict[str, Any]:
        """
        Get custom fields.

        Args:
            relationtype: Optional filter - 'person', 'project', or 'company' (or empty for all)

        Returns:
            List of custom fields
        """
        params = {}
        if relationtype:
            params["relationtype"] = relationtype

        return self.client._make_request("GET", "/v1/user/fields", params=params)

    def get_profile(self) -> Dict[str, Any]:
        """
        Get user profile.

        Returns:
            User profile information
        """
        return self.client._make_request("GET", "/v1/user/profile")

    def get_segments_people(self) -> Dict[str, Any]:
        """
        Get people contact segments.

        Returns:
            List of people segments
        """
        return self.client._make_request("GET", "/v1/user/segments/people")

    def get_segments_projects(self) -> Dict[str, Any]:
        """
        Get project segments.

        Returns:
            List of project segments
        """
        return self.client._make_request("GET", "/v1/user/segments/projects")

    def get_stages_people(self) -> Dict[str, Any]:
        """
        Get people contact stages.

        Returns:
            List of people stages
        """
        return self.client._make_request("GET", "/v1/user/stages/people")

    def get_stages_projects(self) -> Dict[str, Any]:
        """
        Get project stages.

        Returns:
            List of project stages
        """
        return self.client._make_request("GET", "/v1/user/stages/projects")

    def get_steps(self) -> Dict[str, Any]:
        """
        Get steps.

        Returns:
            List of steps
        """
        return self.client._make_request("GET", "/v1/user/steps")

    def get_views(self) -> Dict[str, Any]:
        """
        Get views and audiences.

        Returns:
            List of views and audiences
        """
        return self.client._make_request("GET", "/v1/user/views")
