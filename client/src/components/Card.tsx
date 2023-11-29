import React from 'react';

export default function Card(props: React.ComponentProps<'div'>) {
  return (
    <div className="container p-4 mx-auto ">
      <div
        className="rounded bg-white text-grey-darkest shadow-lg my-8"
        {...props}
      >
        {props.children}
      </div>
    </div>
  );
}
