import {projection_Labs_api_key, accountMapping} from './config.js'
import { fileURLToPath } from 'url';
import login from './common.js';
import fetch from 'node-fetch';
import fs from 'fs';
import path from 'path';

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
    // Access the API key from environment variables
    const apiKey = process.env.PROJECTION_LABS_API_KEY;
    
    for (const accountMappingElement of accountMapping) {
        if (accountMappingElement.balance !== null) {
            console.log(`await window.projectionlabPluginAPI.updateAccount('${accountMappingElement.plAccountID}', { balance: ${accountMappingElement.balance} }, { key: '${apiKey}' });`);
        }
    }
}

function writeUpdateFunction(accountMapping) {
    const apiKey = process.env.PROJECTION_LABS_API_KEY;
    let commands = [];

    for (const accountMappingElement of accountMapping) {
        if (accountMappingElement.balance !== null) {
            commands.push(`await window.projectionlabPluginAPI.updateAccount('${accountMappingElement.plAccountID}', { balance: ${accountMappingElement.balance} }, { key: '${apiKey}' });`);
        }
    }

    const dirname = path.dirname(fileURLToPath(import.meta.url));
    fs.writeFileSync(path.join(dirname, 'commands.txt'), commands.join('\n'), 'utf8');
}

async function main() {
    console.log("Initializing")
    const token = await login();

    const options = {
        "headers": {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": token,
            "client-platform": "web",
            "content-type": "application/json",
        },
        "referrerPolicy": "no-referrer",
        "body": "{\"operationName\":\"Web_GetAccountsPage\",\"variables\":{},\"query\":\"query Web_GetAccountsPage {\\n  hasAccounts\\n  accountTypeSummaries {\\n    type {\\n      name\\n      display\\n      group\\n      __typename\\n    }\\n    accounts {\\n      id\\n      ...AccountsListFields\\n      __typename\\n    }\\n    totalDisplayBalance\\n    __typename\\n  }\\n  householdPreferences {\\n    id\\n    accountGroupOrder\\n    __typename\\n  }\\n}\\n\\nfragment AccountsListFields on Account {\\n  id\\n  syncDisabled\\n  isHidden\\n  isAsset\\n  includeInNetWorth\\n  order\\n  type {\\n    name\\n    display\\n    __typename\\n  }\\n  ...AccountListItemFields\\n  __typename\\n}\\n\\nfragment AccountListItemFields on Account {\\n  id\\n  displayName\\n  displayBalance\\n  signedBalance\\n  updatedAt\\n  syncDisabled\\n  icon\\n  isHidden\\n  isAsset\\n  includeInNetWorth\\n  includeBalanceInNetWorth\\n  displayLastUpdatedAt\\n  ...AccountMaskFields\\n  credential {\\n    id\\n    updateRequired\\n    dataProvider\\n    disconnectedFromDataProviderAt\\n    __typename\\n  }\\n  institution {\\n    id\\n    ...InstitutionStatusTooltipFields\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment AccountMaskFields on Account {\\n  id\\n  mask\\n  subtype {\\n    display\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment InstitutionStatusTooltipFields on Institution {\\n  id\\n  logo\\n  name\\n  status\\n  plaidStatus\\n  hasIssuesReported\\n  url\\n  hasIssuesReportedMessage\\n  transactionsStatus\\n  balanceStatus\\n  __typename\\n}\"}",
        "method": "POST"
    };
    console.log("Fetching Monarch data")
    await fetchAndProcessData("https://api.monarchmoney.com/graphql", options, accountMapping);
    console.log("Updating account mapping script")
    createUpdateFunction(accountMapping);
    writeUpdateFunction(accountMapping);
}

main();
