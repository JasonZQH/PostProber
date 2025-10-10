import React from 'react'
import { Link, useLocation } from 'react-router-dom'

function Sidebar() {
  const location = useLocation()

  const mainMenuItems = [
    {
      path: '/compose',
      icon: 'heroicons:pencil-square',
      label: 'Compose'
    },
    {
      path: '/schedule',
      icon: 'heroicons:calendar-days',
      label: 'Schedule'
    }
  ]

  const analyticsMenuItems = [
    {
      path: '/analytics',
      icon: 'heroicons:chart-bar-square',
      label: 'Analytics'
    },
    {
      path: '/health',
      icon: 'heroicons:heart',
      label: 'Health Check'
    }
  ]

  const settingsMenuItems = [
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

  const renderMenuSection = (items, sectionTitle = null) => (
    <div className="mb-6">
      {sectionTitle && (
        <div className="px-4 mb-3">
          <h3 className="text-xs font-semibold text-base-content opacity-60 uppercase tracking-wider">
            {sectionTitle}
          </h3>
        </div>
      )}
      <ul className="space-y-1">
        {items.map((item) => (
          <li key={item.path}>
            <Link
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium nav-hover group ${
                isActive(item.path)
                  ? 'bg-primary bg-opacity-10 font-semibold'
                  : 'text-base-content hover:bg-base-200'
              }`}
              style={isActive(item.path) ? { color: '#1e40af' } : {}}
            >
              <span
                className={`iconify ${
                  isActive(item.path) ? '' : 'text-base-content opacity-70 group-hover:opacity-100'
                }`}
                style={isActive(item.path) ? { color: '#1e40af' } : {}}
                data-icon={item.icon}
                data-width="20"
              ></span>
              <span
                className={`sidebar-text ${isActive(item.path) ? 'font-semibold' : ''} ${item.path === '/dashboard' ? 'flex-1 text-center' : ''}`}
                style={isActive(item.path) ? { color: '#1e40af' } : {}}
              >
                {item.label}
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )

  return (
    <div className="h-full bg-base-100 flex flex-col sidebar-expanded">
      {/* Sidebar content */}
      <div className="flex-1 overflow-y-auto pt-6 px-2">
        {renderMenuSection(mainMenuItems)}
        {renderMenuSection(analyticsMenuItems, 'Analytics')}
        {renderMenuSection(settingsMenuItems, 'Settings')}
      </div>

      {/* Sidebar footer */}
      <div className="p-4 border-t border-base-300">
        <button className="btn btn-ghost w-full justify-start gap-3 nav-hover focus-primary">
          <span className="iconify text-base-content opacity-70" data-icon="heroicons:question-mark-circle" data-width="20"></span>
          <span className="sidebar-text">Help & Support</span>
        </button>

        <div className="mt-3 p-3 bg-base-200 rounded-lg">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-2 h-2 bg-success rounded-full"></div>
            <span className="text-xs font-medium text-base-content">All Systems Operational</span>
          </div>
          <p className="text-xs text-base-content opacity-60">Last check: 2 min ago</p>
        </div>
      </div>
    </div>
  )
}

export default Sidebar