





import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="max-w-3xl w-full mx-auto text-center space-y-8">

        <h1 className="text-5xl font-bold text-green-700">Welcome to Seed to Chef</h1>

        <p className="text-xl text-gray-600">
          The vertically-integrated platform connecting automated farms with distributed chefs.
        </p>

        <div className="space-y-4">
          <Link href="/browse" className="bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-8 rounded-full shadow-lg transition duration-200 ease-in-out transform hover:-translate-y-1">
            Browse Dishes
          </Link>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-xl mx-auto">
            <Link href="/about" className="block bg-white border border-gray-300 rounded-lg p-6 shadow-sm hover:shadow-md transition duration-200 ease-in-out text-left">
              <h2 className="text-2xl font-semibold text-green-700">About Us</h2>
              <p className="mt-2 text-gray-600">Learn about our mission and technology.</p>
            </Link>

            <Link href="/how-it-works" className="block bg-white border border-gray-300 rounded-lg p-6 shadow-sm hover:shadow-md transition duration-200 ease-in-out text-left">
              <h2 className="text-2xl font-semibold text-green-700">How It Works</h2>
              <p className="mt-2 text-gray-600">From farm to table in one seamless experience.</p>
            </Link>
          </div>

        </div>

      </div>
    </main>
  );
}




