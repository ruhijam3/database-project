<script lang="ts">
    import { onMount } from "svelte";

    interface Location {
        name: string;
    }

    const API_URL = "http://localhost:5000";

    let connected = false;
    let message = "checking....";
    let locations: Location[] = [];

    async function checkConnection() {
        try {
            const response = await fetch(`${API_URL}/location`);

            if (response.ok) {
                const data = await response.json();
                locations = data;
                connected = true;
                message = "database is connected";
            } else {
                message = "connection failed";
            }
        } catch (err) {
            message = "Error: " + err;
        }
    }

    onMount(() => {
        checkConnection();
    });
</script>

<div>
    <h1>Database Connection Test</h1>
    <p>{message}</p>
    {#if connected}
        <p>SUCCESSFULLY CONNECTED TO DATABASE</p>

        <h2>Locations:</h2>
        <ul>
            {#each locations as location}
                <li>
                    <strong>{location.name}</strong>
                </li>
            {/each}
        </ul>
    {/if}
</div>
