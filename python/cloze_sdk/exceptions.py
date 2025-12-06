"""
Custom exceptions for the Cloze SDK.

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


class ClozeAPIError(Exception):
    """Base exception for all Cloze API errors."""

    def __init__(self, message, errorcode=None, response=None):
        super().__init__(message)
        self.errorcode = errorcode
        self.response = response


class ClozeAuthenticationError(ClozeAPIError):
    """Raised when authentication fails."""

    pass


class ClozeRateLimitError(ClozeAPIError):
    """Raised when rate limit is exceeded."""

    pass


class ClozeValidationError(ClozeAPIError):
    """Raised when request validation fails."""

    pass
