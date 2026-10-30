import './App.css'

import Chat from './components/Chat';
import CanvasInfo from './components/demo/CanvasInfo';
import DBInterface from './components/demo/DBInterface';
import canvyLogoFull from './assets/canvy_logo_full.png'

function App() {
  return (
    <>
      <div className="flex flex-col items-center justify-start isolate bg-linear-to-br from-white via-white to-gray-100 p-6 sm:py-10 lg:px-30">
        <div
          aria-hidden="true"
          className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80"
        >
          <div
            style={{
              clipPath:
                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
            }}
            className="relative left-1/2 -z-10 aspect-1155/678 w-144.5 max-w-none -translate-x-1/2 rotate-30 bg-linear-to-tr from-gray-200 to-gray-400 opacity-30 sm:left-[calc(50%-40rem)] sm:w-288.75"
          />
        </div>

        <img
          src={canvyLogoFull}
          alt="Canvy Logo Full"
          className="w-48 max-w-full sm:w-56"
        />

        <Chat />

        {/* Demo/testing components */}
        <CanvasInfo />
        <DBInterface />

      </div>
    </>
  )
}

export default App
