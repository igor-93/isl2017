import React from 'react';

export default class Main extends React.Component {

    render() {
        return (
            <main id="appMain">
                <div className="page-container app-content">
                    {this.props.children}
                </div>
            </main>
        );
    }

}

Main.propTypes = {
    children: React.PropTypes.node
};

Main.defaultProps = {};

Main.displayName = 'Main';

    
    
