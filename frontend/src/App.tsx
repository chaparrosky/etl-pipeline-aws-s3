import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import FighterSearch from './pages/FighterSearch';
import FighterProfile from './pages/FighterProfile';
import HeadToHead from './pages/HeadToHead';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<FighterSearch />} />
          <Route path="/fighter/:id" element={<FighterProfile />} />
          <Route path="/head-to-head" element={<HeadToHead />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
