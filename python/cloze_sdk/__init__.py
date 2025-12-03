"""
Cloze Python SDK

A comprehensive Python SDK for the Cloze API.

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

from .client import ClozeClient
from .exceptions import ClozeAPIError, ClozeAuthenticationError, ClozeRateLimitError

__version__ = "1.0.0"
__all__ = [
    "ClozeClient",
    "ClozeAPIError",
    "ClozeAuthenticationError",
    "ClozeRateLimitError",
]
