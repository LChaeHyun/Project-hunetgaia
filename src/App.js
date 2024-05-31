import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./pages/Home";
import Feeds from "./pages/Feeds";
import Profile from "./pages/Profile";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/all",
    element: <Feeds />,
  },
  {
    path: "/profile",
    element: <Profile />,
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
