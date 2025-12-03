<?php

/**
 * Timeline endpoints.
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
class Timeline
{
    private $client;

    public function __construct(ClozeClient $client)
    {
        $this->client = $client;
    }

    /**
     * Create a communication timeline item.
     *
     * @param array $communication Communication data
     * @return array Creation result
     */
    public function createCommunication(array $communication): array
    {
        return $this->client->makeRequest(
            'POST',
            '/v1/timeline/communication/create',
            null,
            $communication
        );
    }

    /**
     * Create a content timeline item.
     *
     * @param array $content Content data
     * @return array Creation result
     */
    public function createContent(array $content): array
    {
        return $this->client->makeRequest(
            'POST',
            '/v1/timeline/content/create',
            null,
            $content
        );
    }

    /**
     * Create a todo timeline item.
     *
     * @param array $todo Todo data
     * @return array Creation result
     */
    public function createTodo(array $todo): array
    {
        return $this->client->makeRequest(
            'POST',
            '/v1/timeline/todo/create',
            null,
            $todo
        );
    }

    /**
     * Retrieve email opens.
     *
     * @param int|null $fromTimestamp UTC ms timestamp for first message to retrieve
     * @param string|null $user User identifier
     * @return array Message opens data
     */
    public function getMessageOpens(?int $fromTimestamp = null, ?string $user = null): array
    {
        $params = [];
        if ($fromTimestamp !== null) {
            $params['from'] = $fromTimestamp;
        }
        if ($user) {
            $params['user'] = $user;
        }

        return $this->client->makeRequest('GET', '/v1/messages/opens', $params);
    }
}

