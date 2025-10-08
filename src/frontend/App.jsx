import React from 'react'
  import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

  function App() {
    return (
      <Router>
        <div className="App">
          <header>
            <h1>PostProber</h1>
            <p>AI Agent powered Social Media Reliability Monitor</p>
          </header>
          <main>
            <Routes>
              <Route path="/" element={<Home />} />
            </Routes>
          </main>
        </div>
      </Router>
    )
  }

  function Home() {
    return (
      <div>
        <h2>Welcome to PostProber</h2>
        <p>Frontend is running! 🎉</p>
      </div>
    )
  }

  export default App