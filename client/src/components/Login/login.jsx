import "./login.css";

function Login() {
    return (
        <div className="Login">
            <div className="Login_container">
                <div className="Login_containerTitle">
                    <h1>Welcome to the chat system!</h1>
                </div>
                <form className="Login_containerForm">
                    <div className="Login_containerFormAlignInputs">
                        <label className="Login_containerFormLabel">Phone Number:</label>
                        <input className="Login_containerFormInput"/>
                    </div>
                    <div className="Login_containerFormAlignInputs">
                        <label className="Login_containerFormLabel">Password:</label>
                        <input className="Login_containerFormInput"/>
                    </div>
                    <div className="Login_containerFormAlignInputs">
                        <button className="Login_containerFormButton">Send</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export { Login };
