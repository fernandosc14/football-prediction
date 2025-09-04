import React from "react";

const appStage = process.env.NEXT_PUBLIC_APP_STAGE || "BETA";
const appVersion = process.env.NEXT_PUBLIC_APP_VERSION || "0.9.0";

export default function Footer() {
  return (
    <footer className="w-full border-t border-gray-800 bg-gray-900 text-gray-300 py-6 mt-12">
      <div className="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="text-xs md:text-sm text-center md:text-left">
          <span className="font-semibold text-yellow-400">Notice:</span> This site uses artificial intelligence to generate predictions. It is not a betting recommendation. Use at your own risk.
        </div>
        <div className="flex items-center gap-2">
          <a
            href="https://github.com/fernandosc14/football-prediction"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center px-3 py-1 bg-gray-800 text-white rounded-full hover:bg-white/80 hover:text-gray-900 transition-colors duration-300 text-xs font-semibold"
          >
            <svg
              className="mr-2 h-4 w-4"
              fill="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                d="M12 0C5.37 0 0 5.373 0 12c0 5.303 3.438 9.8 8.205 11.387.6.113.82-.258.82-.577
                0-.285-.01-1.04-.015-2.04-3.338.726-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.09-.745.083-.729.083-.729
                1.205.085 1.84 1.237 1.84 1.237 1.07 1.834 2.807 1.304 3.492.997.108-.775.418-1.305.762-1.605-2.665-.305-5.466-1.334-5.466-5.93
                0-1.31.468-2.38 1.235-3.22-.123-.303-.535-1.523.117-3.176 0 0 1.008-.322 3.3 1.23a11.52 11.52 0 013.003-.404c1.02.005
                2.047.138 3.003.404 2.29-1.552 3.297-1.23 3.297-1.23.653 1.653.241 2.873.12 3.176.77.84 1.233 1.91 1.233 3.22
                0 4.61-2.803 5.624-5.475 5.92.43.372.823 1.102.823 2.222 0 1.606-.015 2.898-.015 3.293 0 .322.216.694.825.576C20.565
                21.796 24 17.298 24 12c0-6.627-5.373-12-12-12z"
              />
            </svg>
            GitHub
            <span className="ml-2 inline-block rounded-full px-2 py-0.5 text-xs font-semibold bg-yellow-400 text-gray-900">
              {appStage}
            </span>
            <span className="ml-2 inline-block rounded-full px-2 py-0.5 text-xs font-semibold text-white border bg-blue-700 border-blue-700">
              v{appVersion}
            </span>
          </a>
        </div>
      </div>
    </footer>
  );
}
