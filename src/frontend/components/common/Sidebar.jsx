import React from 'react'
import { Link, useLocation } from 'react-router-dom'

function Sidebar() {
  const location = useLocation()

  const menuItems = [
    {
      path: '/dashboard',
      icon: 'heroicons:home',
      label: 'Dashboard'
    },
    {
      path: '/compose',
      icon: 'heroicons:pencil-square',
      label: 'Compose Post'
    },
    {
      path: '/schedule',
      icon: 'heroicons:calendar-days',
      label: 'Schedule'
    },
    {
      path: '/analytics',
      icon: 'heroicons:chart-bar-square',
      label: 'Analytics'
    },
    {
      path: '/accounts',
      icon: 'heroicons:link',
      label: 'Accounts'
    },
    {
      path: '/settings',
      icon: 'heroicons:cog-6-tooth',
      label: 'Settings'
    }
  ]

  const isActive = (path) => location.pathname === path

  return (
    <div className="h-full bg-base-100 border-r border-base-300 transition-width flex flex-col sidebar-expanded">
      {/* Sidebar content */}
      <div className="flex-1 overflow-y-auto">
        <ul className="menu p-4 gap-2">
          {/* Navigation Items */}
          {menuItems.map((item) => (
            <li key={item.path}>
              <Link
                to={item.path}
                className={`nav-hover focus-primary group ${
                  isActive(item.path) ? 'active' : ''
                }`}
              >
                <span className="iconify" data-icon={item.icon} data-width="20"></span>
                <span className="sidebar-text font-medium">{item.label}</span>
              </Link>
            </li>
          ))}
        </ul>
      </div>

      {/* Sidebar footer */}
      <div className="p-4 border-t border-base-300">
        <div className="text-center">
          <button className="btn btn-sm btn-ghost w-full nav-hover focus-primary">
            <span className="iconify" data-icon="heroicons:question-mark-circle" data-width="16"></span>
            <span className="sidebar-text text-xs">Help &amp; Support</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default Sidebar