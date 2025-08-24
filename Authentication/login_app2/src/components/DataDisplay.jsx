import { Table } from 'react-bootstrap';
import { createClaimsTable } from '../utils/claimUtils';

import '../styles/App.css';

export const IdTokenData = (props) => {
    const tokenClaims = props.idTokenClaims;

    return (
        <>
            <div className="data-area-div">
                <p>
                    See below the claims in your <strong> ID token </strong>. For more information, visit:{' '}
                    <span>
                        <a href="https://docs.microsoft.com/en-us/azure/active-directory/develop/id-tokens#claims-in-an-id-token">
                            docs.microsoft.com
                        </a>
                    </span>
                </p>
                <div className="data-area-div">
                    <Table responsive striped bordered hover>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>E-Mail</th>
                                {/* <th>Description</th> */}
                            </tr>
                        </thead>
                        <tbody>
                            {console.log(tokenClaims)}
                            <td>{tokenClaims.name}</td>
                            <td>{tokenClaims.preferred_username}</td>
                            {/* {createClaimsTable(tokenClaims)} */}
                        </tbody>
                    </Table>
                </div>
            </div>
        </>
    );
};