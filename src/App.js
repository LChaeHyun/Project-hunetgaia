import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./pages/Home";
import Feeds from "./pages/Feeds";
import Profile from "./pages/Profile";
import Error from "./pages/Error";
import Signup from "./pages/Signup";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
    errorElement: <Error />,
  },
  {
    path: "/all",
    element: <Feeds />,
    errorElement: <Error />,
  },
  {
    path: "/profile",
    element: <Profile />,
    errorElement: <Error />,
  },
  {
    path: "/signup",
    element: <Signup />,
    errorElement: <Error />,
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
