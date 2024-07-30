import { BrowserRouter, Route, Routes } from "react-router-dom"
import { Signup } from "./pages/Signup"
import { Dashboard } from "./pages/Dashboard"
import { Signin } from "./pages/Signin"
import { SendMoney } from "./pages/SendMoney"
import { LandingPage } from "./pages/LandingPage"
import {TransferDone} from './pages/TransferDone'


function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/signin" element={<Signin />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/send" element={<SendMoney />} />
          <Route path="/transferdone" element={<TransferDone/>}/>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
