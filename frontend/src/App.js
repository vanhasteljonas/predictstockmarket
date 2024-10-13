import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./styles/index.css";

import Header from './components/Header';

import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ContactPage from './pages/ContactPage';


export default function App() {
  return (
    <>
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} /> 
        </Routes>
      </BrowserRouter>
    </>
  );
}
