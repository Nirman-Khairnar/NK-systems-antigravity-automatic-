const https = require('https');
const fs = require('fs');
const path = require('path');

// Helper to read .env manually
function getEnv(key) {
    try {
        const envPath = path.resolve(__dirname, '../../.env');
        if (fs.existsSync(envPath)) {
            const content = fs.readFileSync(envPath, 'utf8');
            const lines = content.split('\n');
            for (const line of lines) {
                if (line.startsWith(key + '=')) {
                    return line.substring(key.length + 1).trim();
                }
            }
        }
    } catch (e) {
        console.error("Error reading .env", e);
    }
    return process.env[key];
}

const NOTION_API_KEY = getEnv("NOTION_API_KEY");
const ROOT_PAGE_ID = "2dd50cd5-29b6-81b9-a5ab-ec329792fdf4";

if (!NOTION_API_KEY) {
    console.error("Missing NOTION_API_KEY in .env");
    process.exit(1);
}

function request(path, method = 'GET') {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'api.notion.com',
            path: '/v1' + path,
            method: method,
            headers: {
                'Authorization': `Bearer ${NOTION_API_KEY}`,
                'Notion-Version': '2022-06-28',
                'Content-Type': 'application/json'
            }
        };

        const req = https.request(options, res => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    if (res.statusCode >= 200 && res.statusCode < 300) {
                        resolve(json);
                    } else {
                        reject(json);
                    }
                } catch (e) {
                    reject(e);
                }
            });
        });

        req.on('error', error => reject(error));
        req.end();
    });
}

async function explore(blockId, depth = 0) {
    try {
        const response = await request(`/blocks/${blockId}/children`);
        const results = response.results || [];
        const indent = "  ".repeat(depth);

        for (const block of results) {
            const type = block.type;
            let title = "";
            let shouldRecurse = false;

            if (type === 'child_page') {
                title = block.child_page.title;
                console.log(`${indent}[PAGE] ${title} (${block.id})`);
                shouldRecurse = true;
            } else if (type === 'child_database') {
                title = block.child_database.title;
                console.log(`${indent}[DB] ${title} (${block.id})`);
                // Databases usually don't have block children in the same way, but their pages do.
            } else if (type === 'column_list' || type === 'column') {
                shouldRecurse = true;
            }

            if (shouldRecurse) {
                await explore(block.id, depth + 1);
            }
        }
    } catch (e) {
        console.error(`Error exploring block ${blockId}:`, e.message || e);
    }
}

console.log(`Starting scan of Page: ${ROOT_PAGE_ID}`);
explore(ROOT_PAGE_ID);
