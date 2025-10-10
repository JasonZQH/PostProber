import React from 'react'
import Header from './Header'
import Sidebar from './Sidebar'

function Layout({ children }) {
  return (
    <div className="bg-base-200 min-h-screen flex flex-col font-sans">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 p-6 md:p-8 bg-base-200 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  )
}

export default Layout