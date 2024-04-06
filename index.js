import {projection_Labs_api_key, accountMapping} from './config.js'
import login from './common.js';
import fetch from 'node-fetch';
import fs from 'fs';

async function fetchAndProcessData(url, options, accountMapping) {
    const response = await fetch(url, options);
    const data = await response.json();
    const accountTypeSummaries = data.data.accountTypeSummaries;

    for (const accountTypeSummary of accountTypeSummaries) {
        for (const account of accountTypeSummary.accounts) {
            const mappedAccount = accountMapping.find(accountMap => accountMap.monarchAccountID === account.id);
            if (mappedAccount) {
                mappedAccount.balance = account.displayBalance;
            }
        }
    }
}

function createUpdateFunction(accountMapping) {
    const apiKey = process.env.PROJECTION_LABS_API_KEY;
    let commands = [];  // Array to hold commands
    
    for (const accountMappingElement of accountMapping) {
        if (accountMappingElement.balance !== null) {
            commands.push(`await window.projectionlabPluginAPI.updateAccount('${accountMappingElement.plAccountID}', { balance: ${accountMappingElement.balance} }, { key: '${apiKey}' });`);
        }
    }

    // Write commands to a file
    fs.writeFileSync(path.join(__dirname, 'commands.txt'), commands.join('\n'), 'utf8');
}

async function main() {
    console.log("Initializing");
    const token = await login();

    const options = {
        headers: {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": token,
            "client-platform": "web",
            "content-type": "application/json",
        },
        referrerPolicy: "no-referrer",
        body: "{\"operationName\":\"Web_GetAccountsPage\",\"variables\":{},\"query\":\"...\"}",
        method: "POST"
    };
    
    console.log("Fetching data...");
    await fetchAndProcessData("https://api.monarchmoney.com/graphql", options, accountMapping);
    console.log("Processing updates...");
    createUpdateFunction(accountMapping);
    console.log("Process completed.");
}

main();
