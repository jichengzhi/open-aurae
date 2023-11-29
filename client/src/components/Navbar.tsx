import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from '@/components/ui/navigation-menu';
import { User, useAuth0 } from '@auth0/auth0-react';
import {
  HoverCard,
  HoverCardArrow,
  HoverCardContent,
  HoverCardTrigger,
} from '@radix-ui/react-hover-card';

import { Card, CardDescription, CardTitle } from '@/components/ui/card.tsx';
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
    <NavigationMenuLink asChild>
      <Link to={props.to} className="no-underline">
        <NavTitle>{props.children}</NavTitle>
      </Link>
    </NavigationMenuLink>
  );
}

function NavLoginButton(): React.JSX.Element {
  const { loginWithRedirect } = useAuth0();

  return <NavTitle onClick={() => loginWithRedirect()}>Log In</NavTitle>;
}

function NavLogoutButton(): React.JSX.Element {
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
function Logo(): React.JSX.Element {
  return (
    <h1 className="text-gray-700 text-4xl">
      <span className="font-bold">OpenAurae</span>
      <span className="font-thin hidden md:inline">Dashboard</span>
    </h1>
  );
}

function ProfileCard({ user }: { user: User }) {
  return (
    <Card className="p-4">
      <CardTitle className="font-normal text-base">{user.name}</CardTitle>
      <CardDescription>{user.email}</CardDescription>
    </Card>
  );
}

export default function Navbar(): React.JSX.Element {
  const { user, isAuthenticated } = useAuth0();

  return (
    <NavigationMenu className="flex-col sm:flex-row min-w-[90%] m-auto justify-between h-24 font-sans">
      <NavLink to="/">
        <Logo />
      </NavLink>

      <NavigationMenuList
        id="foo"
        className="min-w-full justify-between content-center gap-5 lg:gap-20"
      >
        <NavigationMenuItem>
          <NavLink to="/admin">Admin</NavLink>
        </NavigationMenuItem>

        <NavigationMenu>
          {/* https://github.com/shadcn-ui/ui/issues/418#issuecomment-1728277834 */}
          <NavigationMenuItem>
            <NavigationMenuTrigger>
              <NavTitle>Projects</NavTitle>
            </NavigationMenuTrigger>
            <NavigationMenuContent className="w-full p-4">
              <ul className="w-[180px] flex flex-col justify-around gap-8">
                <li>
                  <NavLink to="/building658">Building 658</NavLink>
                </li>

                <li>
                  <NavLink to="/building87">Building 87</NavLink>
                </li>

                <li>
                  <NavLink to="/monash">Monash Campus</NavLink>
                </li>
              </ul>
            </NavigationMenuContent>
          </NavigationMenuItem>
        </NavigationMenu>

        {isAuthenticated && user ? (
          <>
            <NavigationMenuItem>
              <NavLogoutButton />
            </NavigationMenuItem>

            <HoverCard>
              <HoverCardTrigger>
                <Avatar className="block bg-white">
                  <AvatarImage src={user.picture} />
                  <AvatarFallback>{user.name}</AvatarFallback>
                </Avatar>
              </HoverCardTrigger>
              <HoverCardContent>
                <HoverCardArrow className="fill-white" />
                <ProfileCard user={user} />
              </HoverCardContent>
            </HoverCard>
          </>
        ) : (
          <NavigationMenuItem>
            <NavLoginButton />
          </NavigationMenuItem>
        )}
      </NavigationMenuList>
    </NavigationMenu>
  );
}
