import LoginRegisterForm from "../components/LoginRegisterForm"

function Login() {
    return <LoginRegisterForm route="/api/token/" method="login"/>
}

export default Login