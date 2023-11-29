import React from 'react';

export default function Card(props: React.ComponentProps<'div'>) {
  return (
    <div className="container mx-auto rounded-2xl bg-white shadow-lg my-8">
      <div {...props}>{props.children}</div>
    </div>
  );
}
