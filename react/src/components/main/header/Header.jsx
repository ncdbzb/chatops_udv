import { Link } from 'react-router-dom';
import './header.css'
import {LogoutComponent} from '../../../scripts/logOut'
import {RequestUserInformation } from '../../../scripts/userInformation';

function Header(){
    RequestUserInformation()
    // const {isLoggedIn} = RequestUserInformation()
    return (
        <header class="page-header">
            <nav class="main-nav">
                <ul class="site-navigation">
                    <li class="site-navigation-item">    
                        <a href="/" class="nav-gigaShad"> UDV LLM </a>
                    </li>
                    <li class="site-navigation-item">    
                        <a href="#aboutProject-text" class="nav-about-project"> О проекте</a>
                    </li>
                    <li>
                        <div class="button">
                            <Link to="/request" class="btn-request" className="button"> <p>Задать тест</p> </Link>
                            <Link to="/test" class="btn-test" className="button"> <p>Задать вопрос</p> </Link>
                            {(<Link to="/signUp" class="btn-signUp"  className="button">
                                 <p>Sign Up</p>
                            </Link>)}
                            <Link to="/logIn" class="btn-signIp"  className="button">
                                 <p>Log In</p>
                            </Link>
                            <Link to="/" class="btn-logOut" onClick={LogoutComponent}  className="button">
                                 <p>Log out</p>
                            </Link>
                        </div>
                    </li>
                </ul>
            </nav>
        </header>
    );
}
export default Header;