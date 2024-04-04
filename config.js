const projection_Labs_api_key = process.env.PROJECTION_LABS_API_KEY;

const monarchCredentials = {
    monarch_email: process.env.MONARCH_EMAIL,
    monarch_password: process.env.MONARCH_PASSWORD,
    monarch_mfa: process.env.MONARCH_MFA
};

// Comment out after getting account mapping locally
// let accountMapping = [
//     {
//         plAccountID: "PROJECTION_LABS_ACCOUNT_ID_GOES_HERE",
//         monarchAccountID: "MONARCH_ACCOUNT_ID_GOES_HERE",
//         balance: null
//     },
//     {
//         plAccountID: "PROJECTION_LABS_ACCOUNT_ID_GOES_HERE",
//         monarchAccountID: "MONARCH_ACCOUNT_ID_GOES_HERE",
//         balance: null
//     }
// ];

let accountMapping = JSON.parse(process.env.ACCOUNT_MAPPING);

export { projection_Labs_api_key, monarchCredentials, accountMapping };
