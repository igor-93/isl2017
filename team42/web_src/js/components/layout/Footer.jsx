import React from 'react';

export default class Footer extends React.Component {

    render() {
        const year = new Date().getFullYear();
        return (
            <footer id="appFooter">
                <div className="page-container">
                    Copyright © {year} Team42
                </div>
            </footer>
        );
    }

}

Footer.propTypes = {};

Footer.defaultProps = {};

Footer.displayName = 'Footer';

    
    
