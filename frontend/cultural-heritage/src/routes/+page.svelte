<!-- <script lang="ts">
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
</div> -->

<script lang="ts">
    import { onMount } from "svelte";

    type Location = {
        id: string;
        name: string;
        street?: string;
        city: string;
        zip_code?: string;
        latitude: number;
        longitude: number;
    };

    const API = "http://localhost:5000";

    // form inputs
    let name = "";
    let street = "";
    let city = "";
    let zip_code = "";
    let latitude = "";
    let longitude = "";

    // app state
    let rows: Location[] = [];
    let loading = true;
    let msg = "";

    function banner(text: string, type: "ok" | "err" = "ok") {
        msg = text;
        const el = document.querySelector<HTMLDivElement>("#banner");
        if (el) el.dataset.type = type;
        setTimeout(() => (msg = ""), 2500);
    }

    async function load() {
        loading = true;
        try {
            const r = await fetch(`${API}/location`);
            if (!r.ok) throw new Error(await r.text());
            rows = await r.json();
        } catch (e: any) {
            banner(e?.message ?? "Failed to load", "err");
        } finally {
            loading = false;
        }
    }

    async function addLocation() {
        if (!name || !city || !latitude || !longitude) {
            banner("Please fill Name, City, Latitude, Longitude.", "err");
            return;
        }
        try {
            const body = {
                name,
                street: street || null,
                city,
                zip_code: zip_code || null,
                latitude: Number(latitude),
                longitude: Number(longitude),
            };
            const r = await fetch(`${API}/location`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });
            if (!r.ok) throw new Error(await r.text());
            name = street = city = zip_code = "";
            latitude = longitude = "";
            await load();
            banner("Location added.");
        } catch (e: any) {
            banner(e?.message ?? "Add failed", "err");
        }
    }

    async function remove(name: string) {
        if (!confirm("Delete this location?")) return;
        try {
            const r = await fetch(
                `${API}/location/${encodeURIComponent(name)}`,
                {
                    method: "DELETE",
                },
            );
            if (!r.ok) throw new Error(await r.text());
            await load();
            banner("Location deleted.");
        } catch (e: any) {
            banner(e?.message ?? "Delete failed", "err");
        }
    }

    onMount(load);
</script>

<div class="page">
    <div class="card">
        <h1>New Location</h1>

        {#if msg}
            <div id="banner" class="banner" data-type="ok">{msg}</div>
        {/if}

        <form class="form" on:submit|preventDefault={addLocation}>
            <label>
                <span>Name:</span>
                <input
                    bind:value={name}
                    placeholder="Giza Necropolis"
                    required
                />
            </label>
            <label>
                <span>Street:</span>
                <input bind:value={street} placeholder="Al-Haram" />
            </label>
            <label>
                <span>City:</span>
                <input bind:value={city} placeholder="Giza" required />
            </label>
            <label>
                <span>Zip Code:</span>
                <input bind:value={zip_code} placeholder="12556" />
            </label>
            <label>
                <span>Latitude:</span>
                <input
                    type="number"
                    step="any"
                    bind:value={latitude}
                    placeholder="29.9792"
                    required
                />
            </label>
            <label>
                <span>Longitude:</span>
                <input
                    type="number"
                    step="any"
                    bind:value={longitude}
                    placeholder="31.1342"
                    required
                />
            </label>

            <div class="actions">
                <button
                    type="button"
                    class="btn cancel"
                    on:click={() => {
                        name = street = city = zip_code = "";
                        latitude = longitude = "";
                    }}>✖ Cancel</button
                >
                <button type="submit" class="btn add">➕ Add</button>
            </div>
        </form>
    </div>

    <div class="list">
        <h2>Locations</h2>
        {#if loading}
            <p>Loading…</p>
        {:else if rows.length === 0}
            <p>No locations yet.</p>
        {:else}
            <table>
                <thead>
                    <tr
                        ><th>Name</th><th>Street</th><th>City</th><th>Zip</th
                        ><th>Lat</th><th>Lng</th><th></th></tr
                    >
                </thead>
                <tbody>
                    {#each rows as r}
                        <tr>
                            <td>{r.name}</td>
                            <td>{r.street}</td>
                            <td>{r.city}</td>
                            <td>{r.zip_code}</td>
                            <td>{r.latitude}</td>
                            <td>{r.longitude}</td>
                            <td
                                ><button
                                    class="btn del"
                                    on:click={() => remove(r.name)}
                                    >Delete</button
                                ></td
                            >
                        </tr>
                    {/each}
                </tbody>
            </table>
        {/if}
    </div>
</div>

<style>
    :global(body) {
        margin: 0;
        font-family:
            system-ui,
            -apple-system,
            Segoe UI,
            Roboto,
            Arial,
            sans-serif;
        background: #fffaf8;
    }

    .page {
        display: grid;
        gap: 24px;
        padding: 24px;
        grid-template-columns: minmax(300px, 420px) 1fr;
        align-items: start;
    }

    .card {
        background: #63003110;
        border: 2px solid #630031;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(99, 0, 49, 0.2);
    }

    h1,
    h2 {
        color: #630031;
    }

    .banner {
        margin: 8px 6px;
        padding: 8px 10px;
        border-radius: 8px;
        font-size: 14px;
        border: 1px solid #cf4420;
        background: #cf442020;
        color: #630031;
    }

    .form {
        display: grid;
        gap: 10px;
        padding: 8px;
    }

    label {
        display: grid;
        grid-template-columns: 120px 1fr;
        align-items: center;
        gap: 10px;
    }

    input {
        height: 34px;
        border: 1px solid #63003170;
        border-radius: 8px;
        padding: 0 10px;
        background: #fff;
    }

    .actions {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        margin-top: 6px;
    }

    .btn {
        border: none;
        border-radius: 10px;
        height: 36px;
        padding: 0 14px;
        cursor: pointer;
        font-weight: 600;
    }

    .btn.cancel {
        background: #cf442020;
        border: 1px solid #cf4420;
        color: #630031;
    }

    .btn.add {
        background: #cf4420;
        color: #fff;
    }

    .btn.add:hover {
        background: #a83510;
    }

    .btn.del {
        background: #630031;
        color: #fff;
    }

    .btn.del:hover {
        background: #4b0024;
    }

    .list {
        background: #fff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
    }

    table {
        width: 100%;
        border-collapse: collapse;
        background: #fff;
    }

    th,
    td {
        padding: 8px 10px;
        border-bottom: 1px solid #eee;
        text-align: left;
    }

    td:last-child {
        width: 1%;
        white-space: nowrap;
    }
</style>
