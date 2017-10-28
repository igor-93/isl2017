import React from 'react';

import {SmartUserSearch}  from "../pages/targets/UserSearch";
import Icon from "../icons/Icon";

export default class Header extends React.Component {

    render() {
        return (
            <header id="appHeader">
                <div id="appHeaderContent" className="page-container">
                    <div className="container-left">
                        <a href="/dandli/">
                            <div className="app-logo">
                                <Icon svgClass={'app-icon'} name={Icon.ICONS.DANDLI}/>
                                <span className="app-name">Dandli</span>
                            </div>
                        </a>
                        <a href="/dandli/about" className="header-button">
                            About
                        </a>
                    </div>
                    <div className="container-right">
                        <a className="header-button" id="logoutLink" href="/dandli/logout/">Logout</a>
                    </div>
                </div>
            </header>
        );
    }

}

Header.propTypes = {};

Header.defaultProps = {};

Header.displayName = 'Header';

    
    
