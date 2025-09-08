export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
        <div className="bg-blue-700 rounded-full shadow-lg p-6 mb-6">
        <svg width="64" height="64" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="text-gray">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        </div>
        <h1 className="text-5xl font-extrabold text-blue-700 mb-2">404</h1>
        <h2 className="text-2xl font-semibold text-white mb-4">Page Not Found</h2>
        <p className="text-gray-400 mb-8 text-center max-w-md">Sorry, the page you are looking for does not exist or has been moved.</p>
        <a
            href="/"
            className="self-center px-6 py-2 bg-blue-600 text-white rounded-full shadow hover:bg-blue-700 transition"
        >
            Go back home
        </a>
    </div>
  );
}
