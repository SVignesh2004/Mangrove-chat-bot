import { Link, Outlet } from "react-router-dom";

function App() {
  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      {/* 🔹 Navigation Bar */}
      <nav className="bg-green-700 text-white flex justify-between items-center px-6 py-4 shadow-md">
        <div className="text-xl font-bold tracking-wide">🌿 Mangrove Explorer</div>
        <ul className="flex gap-6 text-lg font-medium">
          <li><Link to="/" className="hover:text-yellow-300">Home</Link></li>
          <li><Link to="/about" className="hover:text-yellow-300">About Us</Link></li>
          <li><Link to="/project-insight" className="hover:text-yellow-300">Project Insight</Link></li>
        </ul>
      </nav>

      {/* 🔹 Page Content */}
      <main className="flex-1">
        <Outlet /> {/* Renders the selected page */}
      </main>
    </div>
  );
}

export default App;
