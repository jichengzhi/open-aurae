import { Toaster } from '@/components/ui/toaster.tsx';
import { Outlet } from 'react-router-dom';
import Navbar from './components/Navbar.tsx';

export default function RootLayout() {
  return (
    <>
      <Navbar />
      <Outlet />
      <Toaster />
    </>
  );
}
