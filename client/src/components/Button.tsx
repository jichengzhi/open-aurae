import React from 'react';

export default function Button(props: React.ComponentProps<'button'>) {
  return (
    <button
      className="bg-transparent hover:bg-[#38a89d] hover:text-white font-semibold py-2 px-4 border border-gray-200 rounded"
      {...props}
    >
      {props.children}
    </button>
  );
}
