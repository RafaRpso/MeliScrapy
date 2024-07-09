// Navbar.js

import React from 'react';
import { Link } from 'react-router-dom';


function Navbar() {
    return (
        <nav>
            <ul>
                <li><Link to="/">Oferta do dia </Link></li>
                <li><Link to="/avaliacao">Avaliações</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;
