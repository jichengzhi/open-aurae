import { useAuth0 } from '@auth0/auth0-react';
import React from 'react';
import { Link } from 'react-router-dom';

function NavTitle(props: React.ComponentProps<'div'>): React.JSX.Element {
  return (
    <div
      {...props}
      className="text-xl font-bold text-gray-500 no-underline hover:text-gray-800 cursor-pointer"
    >
      {props.children}
    </div>
  );
}

function NavLink(
  props: React.ComponentProps<typeof NavTitle> & { to: string }
): React.JSX.Element {
  return (
    <Link to={props.to} className="no-underline px-4">
      <NavTitle>{props.children}</NavTitle>
    </Link>
  );
}

function NavLoginLink(): React.JSX.Element {
  const { loginWithRedirect } = useAuth0();

  return <NavTitle onClick={() => loginWithRedirect()}>Log In</NavTitle>;
}

function NavLogoutLink(): React.JSX.Element {
  const { logout } = useAuth0();

  return (
    <NavTitle
      onClick={() =>
        logout({ logoutParams: { returnTo: window.location.origin } })
      }
    >
      Log Out
    </NavTitle>
  );
}

function NavLogLink(): React.JSX.Element {
  const { user, isAuthenticated } = useAuth0();

  if (isAuthenticated) {
    return (
      <>
        <NavLogoutLink />
        <img
          aria-description="user avatar"
          src={user!.picture}
          alt={user!.name}
          className="w-10 h-10 rounded-full"
        />
      </>
    );
  } else {
    return <NavLoginLink />;
  }
}

function Logo(): React.JSX.Element {
  return (
    <h1 className="text-gray-700 text-4xl">
      <span className="font-bold">OpenAurae</span>
      <span className="font-thin hidden md:inline">Dashboard</span>
    </h1>
  );
}

export default function Navbar(): React.JSX.Element {
  return (
    <nav className="container flex items-center justify-between mx-auto font-sans h-24">
      <NavLink to="/" className="justify-self-start">
        <Logo />
      </NavLink>

      <NavLink to="/admin">Admin</NavLink>

      <div className="dropdown group block relative">
        <NavTitle>Projects</NavTitle>
        <div className="dropdown-menu group-hover:block hidden absolute -left-1/2 w-56 px-5 pb-5 h-auto bg-gray-100 shadow-lg rounded-xl">
          <NavLink to="/building658">Building 658</NavLink>

          <NavLink to="/building87">Building 87</NavLink>

          <NavLink to="/monash">Monash Campus</NavLink>
        </div>
      </div>

      <NavLogLink />
    </nav>
  );
}
