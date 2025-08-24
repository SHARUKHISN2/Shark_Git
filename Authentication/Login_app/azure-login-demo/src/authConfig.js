 // abab26c2-99bd-4b99-a072-5ed02a7d8892 - clientId
 // 0ad13a08-5c87-4706-9c4a-0c03e70c051b - tenantId

export const msalConfig = {
  auth: {
    clientId: "abab26c2-99bd-4b99-a072-5ed02a7d8892", // from Azure
    authority: "https://login.microsoftonline.com/0ad13a08-5c87-4706-9c4a-0c03e70c051b", 
    redirectUri: "http://localhost:3000/"
  }
};

export const loginRequest = {
  scopes: ["User.Read"] // what you want to access
};
