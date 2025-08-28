import Link from 'next/link';

export default function AdminHome() {
  return (
    <main className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="max-w-3xl w-full mx-auto text-center space-y-8">

        <h1 className="text-5xl font-bold text-green-700">Admin Dashboard</h1>

        <p className="text-xl text-gray-600">
          Manage jurisdictions, permits, and compliance rules.
        </p>

        <div className="space-y-4">
          <Link href="/admin/jurisdictions" className="bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-8 rounded-full shadow-lg transition duration-200 ease-in-out transform hover:-translate-y-1">
            Manage Jurisdictions
          </Link>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-xl mx-auto">
            <Link href="/admin/permits" className="block bg-white border border-gray-300 rounded-lg p-6 shadow-sm hover:shadow-md transition duration-200 ease-in-out text-left">
              <h2 className="text-2xl font-semibold text-green-700">Permit Review</h2>
              <p className="mt-2 text-gray-600">Review and approve kitchen permits.</p>
            </Link>

            <Link href="/admin/compliance" className="block bg-white border border-gray-300 rounded-lg p-6 shadow-sm hover:shadow-md transition duration-200 ease-in-out text-left">
              <h2 className="text-2xl font-semibold text-green-700">Compliance Rules</h2>
              <p className="mt-2 text-gray-600">Manage locality-specific regulations.</p>
            </Link>

            <Link href="/admin/traceability" className="block bg-white border border-gray-300 rounded-lg p-6 shadow-sm hover:shadow-md transition duration-200 ease-in-out text-left">
              <h2 className="text-2xl font-semibold text-green-700">Lot Backtrace</h2>
              <p className="mt-2 text-gray-600">View complete traceability graphs.</p>
            </Link>

            <Link href="/admin/chefs" className="block bg-white border border-gray-300 rounded-lg p-6 shadow-sm hover:shadow-md transition duration-200 ease-in-out text-left">
              <h2 className="text-2xl font-semibold text-green-700">Chef Management</h2>
              <p className="mt-2 text-gray-600">Monitor chef performance and compliance.</p>
            </Link>
          </div>

        </div>

      </div>
    </main>
  );
}
