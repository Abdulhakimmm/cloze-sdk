<?php

/**
 * Team endpoints.
 *
 * Copyright (C) 2025 Cloze SDK Contributors
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

namespace Cloze\SDK;
class Team
{
    private $client;

    public function __construct(ClozeClient $client)
    {
        $this->client = $client;
    }

    /**
     * List team members.
     *
     * @return array List of team members
     */
    public function listMembers(): array
    {
        return $this->client->makeRequest('GET', '/v1/team/members/list');
    }

    /**
     * Update team members.
     *
     * @param array $members List of team member updates
     * @return array Update result
     */
    public function updateMembers(array $members): array
    {
        return $this->client->makeRequest(
            'POST',
            '/v1/team/members/update',
            null,
            ['members' => $members]
        );
    }

    /**
     * Get team organizational nodes.
     *
     * @return array Team nodes structure
     */
    public function getNodes(): array
    {
        return $this->client->makeRequest('GET', '/v1/team/nodes');
    }

    /**
     * Get team roles.
     *
     * @return array List of team roles with names and IDs
     */
    public function getRoles(): array
    {
        return $this->client->makeRequest('GET', '/v1/team/roles');
    }
}

