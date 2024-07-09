import React from 'react';
import HelloWorld from './helloworld';
import "./App.css"
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import OfertaDoDia from './pages/ofertaDoDia';
import MyAvaliacao from './pages/avaliacao';
import "./global.css"
const Home = () => <h2>Home</h2>;
const About = () => <h2>About</h2>;
const Contact = () => <h2>Contact</h2>;

const App = () => {

  return (
    <Router>
    <div className="navbar-container">
      <nav>
        <ul className="nav-list">
          <li className="nav-item">
            <Link to="/oferta-do-dia">Oferta do Dia</Link>
          </li>
          <li className="nav-item">
            <Link to="/avaliacao">Avaliação</Link>
          </li>
          <li className="nav-item">
            <Link to="/analise-empresarial">Análise Empresarial</Link>
          </li>
          
          <li className="nav-item">
            <Link to="/analise-empresarial">(LAB) Dashboard customizável</Link>
          </li>
        </ul>
      </nav>

        <Routes>
          <Route path="/" element={<OfertaDoDia />} />
          <Route path="/helloworld" element={<HelloWorld />} />
          <Route path="/oferta-do-dia" element={<OfertaDoDia />} />
          <Route path="/avaliacao" element={<MyAvaliacao />} />
          
        </Routes>
      </div>
    </Router>
  );
}

export default App;
