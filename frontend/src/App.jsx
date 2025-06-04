import './App.css';
import {Routes, Route} from 'react-router-dom';
import Home from './pages/Home';
import Navbar from './components/Navbar';
import Comparison from './pages/Comparison';
import Login from './pages/Login';

function App() {
  

  return (
    <div>
        <Navbar />
        <Routes>
          <Route path="/comparison" element={<Comparison/>}/>
          <Route path="/login" element={<Login/>}/>
          <Route path="/" element={<Home />} />
        </Routes>

      
    </div>
  );
}

export default App;