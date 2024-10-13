import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/images/logo.png';

export function Header(props) {
    return (
        <nav className="bg-gray-800 text-white p-4 flex items-center">
          {/* Logo placeholder */}
          <div className="mr-6">
            <Link to="/">
             <img src={logo} alt="Logo" className="h-8 w-8" />
            </Link>
          </div>
          <ul className="flex space-x-4">
            <li>
              <Link to="/" className="hover:text-gray-300">Home</Link>
            </li>
            <li>
              <Link to="/about" className="hover:text-gray-300">About</Link>
            </li>
            <li>
              <Link to="/contact" className="hover:text-gray-300">Contact</Link>
            </li>
          </ul>
        </nav>
      );
    };

export default Header;
