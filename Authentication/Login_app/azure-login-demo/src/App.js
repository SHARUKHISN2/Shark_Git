import logo from './logo.svg';
import './App.css';
import React, { useState } from "react";
import Login from "./Login";
import { useMsal, useAccount } from "@azure/msal-react";
import { loginRequest } from "./authConfig";

 // abab26c2-99bd-4b99-a072-5ed02a7d8892 - clientId
 // 0ad13a08-5c87-4706-9c4a-0c03e70c051b - tenantId

function App() {
  // return (
  //   <div className="App">
  //     <header className="App-header">
  //       <img src={logo} className="App-logo" alt="logo" />
  //       <p>
  //         Edit <code>src/App.js</code> and save to reload.
  //       </p>
  //       <a
  //         className="App-link"
  //         href="https://reactjs.org"
  //         target="_blank"
  //         rel="noopener noreferrer"
  //       >
  //         Learn React
  //       </a>
  //     </header>
  //   </div>
  // );

  // const [user, setUser] = useState(null);

  // return (
  //   <div>
  //     {user ? (
  //       <h1>Welcome, {user}!</h1>
  //     ) : (
  //       <Login onLogin={(username) => setUser(username)} />
  //     )}
  //   </div>
  // );

  const { instance, accounts } = useMsal();
  const account = accounts[0];

  const handleLogin = () => {
    instance.loginPopup(loginRequest).catch(e => console.error(e));
  };

  const handleLogout = () => {
    instance.logoutPopup().catch(e => console.error(e));
  };

  return (
    <div style={{ padding: 20 }}>
      {account ? (
        <>
          <h1>Welcome {account.username}</h1>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <button onClick={handleLogin}>Login with Microsoft</button>
      )}
    </div>
  );
}

export default App;
