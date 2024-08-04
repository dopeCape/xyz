import { useEffect, useState } from 'react';
import axios from 'axios';

export function Balance() {
    const [balance, setBalance] = useState(null);

    useEffect(() => {
        axios.get('http://localhost:3000/api/v1/account/balance', {
            headers: {
                Authorization: "Bearer " + localStorage.getItem("token")
            }
        })
        .then(response => {
            setBalance(response.data.balance);
        })
        .catch(error => {
            console.error('Error fetching balance:', error);
        });
    }, []);

    return (
        <div className="flex">
            <div className="font-bold text-lg">
                Your balance
            </div>
            <div className="font-semibold text-lg ml-4">
                Rs {balance !== null ? balance : 'Loading...'}
            </div>
        </div>
    );
}
