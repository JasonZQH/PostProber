import React from 'react'

function Header() {
  return (
    <div className="navbar bg-base-100 shadow-soft border-b border-base-300 header-height px-6">
      {/* Left section: Menu toggle and Logo */}
      <div className="navbar-start">
        <button className="btn btn-ghost btn-circle focus-primary" aria-label="Toggle sidebar">
          <span className="iconify" data-icon="heroicons:bars-3" data-width="24"></span>
        </button>
        <div className="flex items-center ml-4">
          <img alt="Social Media Manager Logo" className="w-10 h-10 rounded-lg" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='8' fill='%233B82F6'/%3E%3Ctext x='20' y='26' text-anchor='middle' fill='white' font-family='sans-serif' font-size='16' font-weight='bold'%3ESM%3C/text%3E%3C/svg%3E" />
          <span className="ml-3 text-xl font-semibold text-primary hidden lg:block">Social Hub</span>
        </div>
      </div>

      {/* Center section: Main navigation */}
      <div className="navbar-center hidden xl:flex">
        <ul className="menu menu-horizontal px-1 gap-2">
          <li><a className="nav-hover focus-primary" href="/dashboard">Dashboard</a></li>
          <li><a className="nav-hover focus-primary" href="/compose">Compose</a></li>
          <li><a className="nav-hover focus-primary" href="/schedule">Schedule</a></li>
          <li><a className="nav-hover focus-primary" href="/analytics">Analytics</a></li>
          <li><a className="nav-hover focus-primary" href="/accounts">Accounts</a></li>
        </ul>
      </div>

      {/* Right section: Search and notifications */}
      <div className="navbar-end">
        {/* Global search */}
        <div className="form-control hidden md:block mr-4">
          <div className="join">
            <input type="text" placeholder="Search posts..." className="input input-bordered input-sm join-item w-48 focus-primary" />
            <button className="btn btn-sm join-item btn-primary" aria-label="Search">
              <span className="iconify" data-icon="heroicons:magnifying-glass" data-width="16"></span>
            </button>
          </div>
        </div>

        {/* Search icon for mobile */}
        <button className="btn btn-ghost btn-circle md:hidden focus-primary" aria-label="Search">
          <span className="iconify" data-icon="heroicons:magnifying-glass" data-width="20"></span>
        </button>

        {/* Notifications */}
        <div className="indicator mr-2">
          <span className="indicator-item badge badge-accent badge-sm">3</span>
          <button className="btn btn-ghost btn-circle focus-primary" aria-label="Notifications">
            <span className="iconify" data-icon="heroicons:bell" data-width="20"></span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default Header