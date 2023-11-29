import { Outlet } from 'react-router-dom';
import Navbar from './components/Navbar.tsx';

export default function RootLayout() {
  return (
    <>
      <Navbar />
      <main className="bg-gray-100 min-h-screen font-sans pb-24">
        <Outlet />
      </main>
    </>
  );
}
