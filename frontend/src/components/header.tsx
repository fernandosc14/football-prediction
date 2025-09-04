"use client";

import React from 'react';

import { Icon } from 'lucide-react';
import { soccerBall } from '@lucide/lab';
import { Menu } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';

const Header = () => {
  const navItems = [
    { name: 'Home', href: '/' },
    { name: 'Predictions', href: '/predictions' },
    { name: 'Statistics', href: '/stats' },
    { name: 'About', href: '/about' },
  ];


  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-800 bg-gray-900">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-green-500">
            <Icon iconNode={soccerBall} className="h-6 w-6 text-white" />
          </div>
          <span className="text-xl font-bold text-white">Football Predictions</span>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-2">
          {navItems.map((item) => (
            <a
              key={item.name}
              href={item.href}
              className="font-semibold text-base text-gray-200 px-3 py-1 rounded-md transition-colors duration-200 hover:bg-green-500/10 hover:text-green-400 focus:bg-green-500/20 focus:text-green-500"
            >
              {item.name}
            </a>
          ))}
        </nav>

        {/* Desktop Github/Badge Button */}
        <div className="hidden md:flex items-center space-x-4">
          <a
            href="https://github.com/fernandosc14/football-prediction"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center px-3 py-2 bg-gray-800 text-white rounded-full hover:bg-green-500 hover:text-gray-900 transition-colors"
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
            <span className="ml-3 inline-block rounded-full px-2 py-0.5 text-xs font-semibold bg-yellow-400 text-gray-900">
              {process.env.NEXT_PUBLIC_APP_STAGE?.toUpperCase()}
            </span>
            <span className="ml-2 inline-block rounded-full px-2 py-0.5 text-xs font-semibold text-white border bg-blue-700 border-blue-700">
              v{process.env.NEXT_PUBLIC_APP_VERSION}
            </span>
          </a>
        </div>

        {/* Mobile Menu */}
        <Sheet>
          <SheetTrigger asChild className="md:hidden">
            <Button variant="ghost" size="icon" className="text-gray-200 hover:text-green-400">
              <Menu className="h-6 w-6" />
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="bg-gray-900 border-l border-gray-800 p-0">
            <div className="flex flex-col space-y-4 mt-8 px-6">
              {navItems.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-gray-200 hover:text-green-400 transition-colors duration-200 font-medium py-2 text-lg"
                >
                  {item.name}
                </a>
              ))}
              <a
                href="https://github.com/fernandosc14/football-prediction"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center px-3 py-2 rounded-md border border-gray-700 text-gray-200 hover:bg-green-500 hover:text-gray-900 transition-colors mt-4"
              >
                <svg
                  className="mr-2 h-5 w-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path d="M12 0C5.37 0 0 5.373 0 12c0 5.303 3.438 9.8 8.205 11.387.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.726-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.09-.745.083-.729.083-.729 1.205.085 1.84 1.237 1.84 1.237 1.07 1.834 2.807 1.304 3.492.997.108-.775.418-1.305.762-1.605-2.665-.305-5.466-1.334-5.466-5.93 0-1.31.468-2.38 1.235-3.22-.123-.303-.535-1.523.117-3.176 0 0 1.008-.322 3.3 1.23a11.52 11.52 0 013.003-.404c1.02.005 2.047.138 3.003.404 2.29-1.552 3.297-1.23 3.297-1.23.653 1.653.241 2.873.12 3.176.77.84 1.233 1.91 1.233 3.22 0 4.61-2.803 5.624-5.475 5.92.43.372.823 1.102.823 2.222 0 1.606-.015 2.898-.015 3.293 0 .322.216.694.825.576C20.565 21.796 24 17.298 24 12c0-6.627-5.373-12-12-12z" />
                </svg>
                GitHub
              </a>
              <div className="flex justify-center items-center mt-6 space-x-2">
                <span className="inline-block rounded-full bg-yellow-400 px-3 py-1 text-sm font-semibold text-gray-900">
                  {process.env.NEXT_PUBLIC_APP_STAGE?.toUpperCase()}
                </span>
                <span className="inline-block rounded-full bg-blue-700 px-3 py-1 text-sm font-semibold text-white border border-blue-700">
                  v{process.env.NEXT_PUBLIC_APP_VERSION}
                </span>
              </div>
            </div>
          </SheetContent>
        </Sheet>
    </div>
    </header>
  );
};

export default Header;
