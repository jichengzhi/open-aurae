import Card from './components/Card.tsx';

export default function Home() {
  return (
    <>
      <div className="container mx-auto pl-2 py-5 sm:px-6 lg:py-10">
        <h1 className="text-5xl text-grey-darkest">Live Air Quality</h1>
      </div>

      <Card>
        <h1>Map of devices</h1>
      </Card>
    </>
  );
}
